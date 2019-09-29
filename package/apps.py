from io import BytesIO
import json

from django.apps import AppConfig
from django.db import transaction
from django.forms.models import model_to_dict

from .models import *
from scripts.utils import *
from .excel import *
from .pdf import genPdfBase64
from .packagemanager import PackageManager
class PackageConfig(AppConfig):
    name = 'package'

def upload_handle(jsonbody):
    excel = convertexcelbase64(jsonbody['excel'])

    try:
        packages, goods = readPackageDataFromXlsx_SF(BytesIO(excel))

        if len(packages) == 0:
            return getresponsemsg(204, '未检测到任何包裹信息')

        err_info = []
        for i in range(len(packages)):
            try:
                with transaction.atomic():
                    package = packages[i]
                    express_code = package.get('express_code')
                    create_pack_sf(package, goods[express_code])
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


def create_pack_sf(pack, goods):

    receiver_identity = pack['receiver_identity']
    receiver_name = pack['receiver_name']
    receiver_tel =  pack['receiver_tel']
    receiver_postcode = pack['receiver_postcode']
    receiver_province = pack['receiver_province']
    receiver_city = pack['receiver_city']
    receiver_district = pack['receiver_district']
    receiver_street = pack['receiver_street']
    sender_name = pack['sender_name']
    sender_tel = pack['sender_tel']
    sender_postcode = pack['sender_postcode']
    sender_city = pack['sender_city']
    sender_street = pack['sender_street']
    sender_hausnr = pack.get('sender_hausnr', '')
    comment = pack.get('comment','')

    extra_services = json.dumps(pack.get('extra_services', ''))
    express_extra = json.dumps(pack.get('express_extra', ''))

    express_code = pack.get('express_code', '')
    goods = json.dumps(goods)

    package = Package.objects.filter(express_code=express_code).first()
    if package is None:
        package = Package.objects.create(package_no = getPackageNo(), logistic_product= 'shunfeng', express_code = express_code, package_goods=goods,
                                         receiver_identity=receiver_identity, receiver_name=receiver_name, receiver_postcode= receiver_postcode,
                                         receiver_tel=receiver_tel, receiver_province=receiver_province,
                                         receiver_city=receiver_city, receiver_district=receiver_district, receiver_street=receiver_street,
                                         sender_name=sender_name, sender_tel=sender_tel, sender_postcode=sender_postcode, sender_city=sender_city,
                                         sender_street=sender_street, sender_hausnr=sender_hausnr,
                                         extra_services=extra_services, express_extra=express_extra, comment=comment)
    else:
        raise Exception(express_code+':单号已存在！')

    return package

def packagelist_handle(offset, limit):
    total = Package.objects.all().count()
    end_num = offset+limit

    packages = Package.objects.all().order_by('-id')[offset:end_num]
    packages_array = []
    for p in packages:
        packmanager = PackageManager(p)
        packages_array.append(packmanager.getPackageJson())

    return {"total": total,"rows": packages_array}


def getPackageByID(pid):
    package = Package.objects.get(id=pid)
    packmanager = PackageManager(package)
    return packmanager.getPackageJson()

def scancode_to_miandan_handle(code):
    package = Package.objects.filter(package_no=code).first()
    if package is None:
        return getresponsemsg(400, '单号未找到，请核对单号是否正确！')
    else:
        package_dict = model_to_dict(package)
        return genPdf([package_dict])


def genPdf(packages):
    content_array = []
    for p in packages:
        package = Package.objects.get(id=p.get('id', ''))
        pm = PackageManager(package)
        content_array.append(pm.getPDFContent())

    pdfs_base64 = genPdfBase64(content_array)

    return getresponsemsg(200, pdfs_base64)


def delPackages(packages):
    for p in packages:
        package_in_db = Package.objects.filter(express_code=p.get('express_code','')).first()
        if package_in_db is not None:
            package_in_db.delete()

    return getresponsemsg(200)
