from django.apps import AppConfig
from django.db import transaction
from django.forms.models import model_to_dict

from .models import *
from scripts.utils import *
from .excel import *
from .pdf import genPdfBase64

class PackageConfig(AppConfig):
    name = 'package'

def upload_handle(jsonbody):
    excel = convertexcelbase64(jsonbody['excel'])

    try:
        packages = readPackageDataFromXlsx(BytesIO(excel))

        if len(packages) == 0:
            return getresponsemsg(204, '未检测到任何包裹信息')

        err_info = []
        for i in range(len(packages)):
            try:
                with transaction.atomic():
                    create_and_edit_pack(packages[i])
            except Exception as e:
                err_info.append(str(e))
        if len(err_info) == 0:
            response = getresponsemsg(200)
        else:
            response = getresponsemsg(400, str(err_info))
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
        raise Exception(inland_code+':单号已存在！')

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

def scancode_to_miandan_handle(code):
    package = Package.objects.filter(inland_code=code).first()
    if package is None:
        return getresponsemsg(400, '单号未找到，请核对单号是否正确！')
    else:
        package_dict = model_to_dict(package)
        return genPdf([package_dict])


def genPdf(packages):
    content_array = []
    for p in packages:
        goods_descr = p.get('goods_descr','') + ' *'+p.get('goods_quantity','')+', '

        content = {
            'logistic_category': 'sf_tw',

            "barcode_no": p.get('inland_code',''),
            "des_code": p.get('des_code',''),
            "sender_name": p.get('sender',''),
            "sender_tel": p.get('sender_tel',''),
            "sender_address": p.get('sender_addr',''),
            "receiver_name": p.get('receiver',''),
            "receiver_tel": p.get('receiver_tel',''),
            "receiver_address": p.get('receiver_addr',''),

            "sf_monthcard_no": p.get('sf_monthcard_no',''),
            "customer_no": p.get('sf_monthcard_no',''),

            "goods_desc": goods_descr,
            "barcode_no_1": p.get('inland_code',''),

            "sender_name_1": p.get('sender',''),
            "sender_tel_1": p.get('sender_tel',''),
            "sender_address_1": p.get('sender_addr',''),
            "receiver_name_1": p.get('receiver',''),
            "receiver_tel_1": p.get('receiver_tel',''),
            "receiver_address_1": p.get('receiver_addr',''),

            "goods_desc_1": goods_descr,
            "goods_num": p.get('goods_quantity','')
        }

        content_array.append(content)

    pdfs_base64 = genPdfBase64(content_array)

    return getresponsemsg(200, pdfs_base64)


def delPackages(packages):
    for p in packages:
        package_in_db = Package.objects.filter(inland_code=p.get('inland_code','')).first()
        if package_in_db is not None:
            package_in_db.delete()

    return getresponsemsg(200)
