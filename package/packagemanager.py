import json
from scripts.utils import formatTime

class PackageManager:

    def __init__(self, package):
        self._package = package

    def getPackageJson(self):
        goods_descr = ''
        goods = json.loads(self._package.package_goods)
        for g in goods:
            goods_descr +=g.get('cn_name','') + ':'+g.get('num','')+','

        express_extra = json.loads(self._package.express_extra)
        extra_services = json.loads(self._package.extra_services)
        package_json = {
            'id': self._package.id,
            'package_no':self._package.package_no,
            'express_code':self._package.express_code,
            'logistic_product': self._package.logistic_product,
            'customer_reference_no': self._package.customer_reference_no,

            'receiver_name': self._package.receiver_name,
            'receiver_tel': self._package.receiver_tel,
            'receiver_addr': self._package.receiver_province+self._package.receiver_city+self._package.receiver_district+self._package.receiver_street,
            'receiver_province': self._package.receiver_province,
            'receiver_city': self._package.receiver_city,
            'receiver_district': self._package.receiver_district,
            'receiver_street': self._package.receiver_street,
            'receiver_identity': self._package.receiver_identity,
            'receiver_postcode': self._package.receiver_postcode,

            'sender_name': self._package.sender_name,
            'sender_tel': self._package.sender_tel,
            'sender_street': self._package.sender_street,
            'sender_postcode': self._package.sender_postcode,
            'sender_city': self._package.sender_city,
            'sender_hausnr': self._package.sender_hausnr,

            'package_weight': self._package.package_weight,
            'createdtime': formatTime(self._package.createdtime),
            'updatedtime': formatTime(self._package.updatedtime),

            'express_extra': express_extra,
            'extra_services':extra_services,
            'goods_descr': goods_descr,
            'goods': goods,

        }

        return package_json
