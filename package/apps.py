from django.apps import AppConfig
from django.db import transaction
from django.forms.models import model_to_dict

from .models import *
from scripts.utils import *
from .excel import *

class PackageConfig(AppConfig):
    name = 'package'

def upload_handle(jsonbody):
    excel = convertexcelbase64(jsonbody['excel'])

    try:
        packages = readPackageDataFromXlsx(BytesIO(excel))

        if len(packages) == 0:
            return getresponsemsg(204, '未检测到任何包裹信息')

        for i in range(len(packages)):
            try:
                inland_code = packages[i]['inland_code']
                with transaction.atomic():
                    create_and_edit_pack(packages[i])
            except Exception as e:
                raise Exception(inland_code+'__'+str(e))

        response = getresponsemsg(200)
    except Exception as e:
        getLogger().error('upload_handle:'+str(e))
        response = getresponsemsg(500, str(e))

    return response

def getPackageCount():
    return Package.objects.all().count()


def create_and_edit_pack(pack):
    inland_code = pack.get('inland_code','')
    sender = pack.get('sender','')
    sender_addr = pack.get('sender_addr','')
    sender_tel = pack.get('sender_tel','')
    receiver = pack.get('receiver','')
    receiver_addr = pack.get('receiver_addr','')
    receiver_tel = pack.get('receiver_tel','')
    goods_descr = pack.get('goods_descr','')
    goods_quantity = pack.get('goods_quantity','')
    des_code = pack.get('des_code','')
    sf_monthcard_no = pack.get('sf_monthcard_no','')
    logistic_product = pack.get('logistic_product','')
    comment = pack.get('comment','')

    package = Package.objects.filter(inland_code=inland_code).first()
    if package is None:
        package = Package.objects.create(package_no = getPackageNo(), inland_code=inland_code, sender=sender,
                                         sender_addr=sender_addr,sender_tel=sender_tel,receiver=receiver,receiver_addr=receiver_addr,
                                         receiver_tel=receiver_tel,goods_descr=goods_descr,goods_quantity=goods_quantity,des_code=des_code,
                                         sf_monthcard_no=sf_monthcard_no, logistic_product=logistic_product,comment=comment)
    else:
        package.sender=sender
        package.sender_addr=sender_addr
        package.sender_tel=sender_tel
        package.receiver=receiver
        package.receiver_addr=receiver_addr
        package.receiver_tel=receiver_tel
        package.goods_descr=goods_descr
        package.goods_quantity=goods_quantity
        package.des_code=des_code
        package.sf_monthcard_no=sf_monthcard_no
        package.logistic_product=logistic_product
        package.comment=comment
        package.save()

    return package

def packagelist_handle(offset, limit):
    total = Package.objects.all().count()
    end_num = offset+limit

    packages = Package.objects.all().order_by('-id')[offset:end_num]
    packages_array = []
    for p in packages:
        packages_array.append(model_to_dict(p))

    return {"total": total,"rows": packages_array}


def getPackageByID(pid):
    package = Package.objects.get(id=pid)
    return package


def genPdf(user, orders):
    pdf_generator = PdfGenerator(pdf_config)
    content_array = []
    #origin_country = getUserCountry(user)
    origin_country = 'DE'
    for o in orders:
        if o['status_no'] == '10' or o['status_no'] == '120':
            continue

        if o.get('trans_code_backup', '') and len(o.get('trans_code_backup', '')) > 0:
            o['inland_code'] = o['trans_code_backup']

        receiver_name = o['receiver_name']
        receiver_tel = o['receiver_tel']

        receiver_address = o['receiver_province']+o['receiver_city']+o['receiver_district']+o['receiver_street']

        barcode_no = o['inland_code']
        sender_name = o['sender_name']
        sender_tel = o['sender_tel']
        sender_address = o['sender_street'] +' '+ o['sender_hausnr']+ ','+o['sender_postcode']+' '+ o['sender_city']
        goods_content, goods_count = getPackageGoods(o['id'])
        if len(goods_content) > 100:
            goods_content = goods_content[:100]

        goods_real_weight = o['package_real_weight']
        goods_value = str(o['fee'])
        logistic_category = getLogisticCategory(o['logistic_category_cagte_label'])

        if o['customer_reference_no']:
            ref_no = o['customer_reference_no']
        else:
            ref_no = o['order_no']

        if logistic_category is not None:
            custom_name = logistic_category.custom_name
        else:
            continue

        if logistic_category.cagte_label == 'CCW':
            content = {
                'logistic_category': logistic_category.cagte_label,

                "barcode_no": barcode_no,
                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,
                "goods_desc": goods_content,

                "barcode_no_1": barcode_no,
                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,
                "order_no": ref_no,
                "custom_name": custom_name,
                "origin_country": origin_country,
            }
        elif logistic_category.cagte_label == 'DE-EMSNL-BCNF':
            content = {
                'logistic_category': logistic_category.cagte_label,

                "barcode_no": barcode_no,
                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,

                "client_code": '',
                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,

                "receiver_postcode": o['receiver_postcode'],

                "goods_name": goods_content[0:8],
                "goods_count": str(goods_count),
                "goods_real_weight": str(goods_real_weight),
                "goods_value": goods_value,

                "barcode_no_1": barcode_no,
                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "order_no_1": ref_no,
                "sender_name_1": sender_name,
                "sender_tel_1": sender_tel,
                "sender_address_1": sender_address,

                "comment": o['comment'],
            }
        elif logistic_category.cagte_label == 'CCL':
            content = {
                'logistic_category': logistic_category.cagte_label,

                "barcode": barcode_no,
                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,

                "order_no": o['order_no'],
                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,

                "goods_desc": goods_content,

                "weight": str(goods_real_weight),
                "tiji_weight": str(goods_real_weight),

                "length": '',
                "width": '',
                "height": '',

                "goods_value": '',
                "origin_country": origin_country,

                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "sender_name_1": sender_name,
                "sender_tel_1": sender_tel,
                "sender_address_1": sender_address,

                "ref_no": ref_no,
                "origin_send_from": origin_country,

                "custom_name": custom_name,
                "barcode_1": barcode_no
            }
        elif logistic_category.cagte_label in['zqbc' , 'sh_yto_bc_wine']:
            if o['customer_reference_no']:
                customer_reference_no = o['customer_reference_no']
            else:
                customer_reference_no= o['order_no']

            content = {
                'logistic_category': 'zqbc',

                "barcode": barcode_no,
                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,
                "goods_desc": goods_content,

                "barcode_1": barcode_no,
                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,
                "order_no": o['order_no'],
                "customer_reference_no": customer_reference_no,
            }
        elif logistic_category.postcode_type == '3s':
            image_name = os.path.join(BASE_DIR, 'resource/pdf/3dmiandan/' + o['inland_code'] + '.' + 'jpg')
            content = {
                "work_dir": os.path.join(BASE_DIR, 'resource', 'pdf', 'work'),
                'logistic_category': logistic_category.postcode_type,
                'image_name': image_name
            }
        elif logistic_category.cagte_label =='P_DG_EMS_A_1':
            if o['customer_reference_no']:
                customer_reference_no = o['customer_reference_no']
            else:
                customer_reference_no= o['order_no']

            content = {
                'logistic_category': 'P_DG_EMS_A_1',

                "barcode": barcode_no,

                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,

                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,

                "fenjiancode": o['reserved4'],

                "weight": str(goods_real_weight),
                "goods_count": str(goods_count),
                "origin_country": 'DE',

                "goods_desc": goods_content,
                "customer_reference_no": customer_reference_no,

                "sender_name_1": sender_name,
                "sender_tel_1": sender_tel,
                "sender_address_1": sender_address,

                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "barcode_1": barcode_no,
                "special_tag":'**'
            }

        elif logistic_category.cagte_label in ['hhbczw', 'fs_yto_milk', 'fs_yto_zw', 'cd_yto_bc_milk', 'sh_yto_bc_milk']:
            if o['customer_reference_no']:
                customer_reference_no = o['customer_reference_no']
            else:
                customer_reference_no= o['order_no']

            content = {
                'logistic_category': logistic_category.cagte_label,
                "distribution_code": o['reserved4'],
                "barcode": barcode_no,
                "receiver_name": receiver_name,
                "receiver_tel": receiver_tel,
                "receiver_address": receiver_address,

                "sender_name": sender_name,
                "sender_tel": sender_tel,
                "sender_address": sender_address,

                "barcode_1": barcode_no,
                "receiver_name_1": receiver_name,
                "receiver_tel_1": receiver_tel,
                "receiver_address_1": receiver_address,

                "goods_desc": goods_content,
                "goods_count": str(goods_count),

                "customer_reference_no": customer_reference_no,
                "cagte_label": logistic_category.cagte_label
            }
        else:
            continue

        content_array.append(content)

    data = pdf_generator.generate(content_array)
    if data:
        return convertBinaryToBase64String(data)
    else:
        return ""
