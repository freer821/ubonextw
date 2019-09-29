from django.core.exceptions import ValidationError
from django.core import mail
from django.core.files.base import ContentFile

from scripts.settings import BASE_DIR, EMAIL_HOST_USER
import logging, os, base64, hashlib, uuid, datetime
from hmac import compare_digest
from logging.handlers import TimedRotatingFileHandler

def sign(cookie):
    h = hashlib.blake2b(digest_size=16, key=b'ubonextw')
    h.update(cookie.encode())
    return h.hexdigest().encode('utf-8')

def verify(cookie, sig):
    good_sig = sign(cookie)
    return compare_digest(good_sig, sig.encode())


def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(('%(value)s is not an integer or a float  number'), params={'value': value})


pakcage_status = {
    "10": "订单信息已收录",
    "20": "已支付",
    "30": "客户包裹预报",
    "31": "包裹已出客户仓",
    "40": "仓库入库",
    "41": "仓库复重-成功",
    "42": "仓库复重-失败",
    "43": "客户补款 - 成功",
    "50": "仓库已出库",
    "60": "送达机场",
    "80": "航班起飞",
    "90": "中国口岸航班落地",
    "100": "中国口岸清关-开始",
    "101": "中国口岸清关-成功",
    "102": "中国口岸清关-失败",
    "110": "国内快递已揽收",
    "120": "包裹取消"

}

def getresponsemsg(status, msg='', err=''):
    return {
        'status': status,
        'msg': msg,
        'err': err
    }

def formatTime(t):
    return t.strftime("%Y-%m-%d %H:%M")

def getParameter(parm):
    if parm is None:
        return ""
    else:
        return parm

def sendEmail(subject, html_content, to_email):
    with mail.get_connection() as connection:
        msg = mail.EmailMessage(
            subject, html_content, EMAIL_HOST_USER, [to_email],
            connection=connection,
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

def convertexcelbase64(data):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    return base64.b64decode(imgstr)

def convertBinaryToBase64String(data):
    return base64.b64encode(data).decode('ascii')

def getRandomNo():
    no = uuid.uuid4().hex[:11].upper()
    return no

def getTimeString():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def getPackageNo():
    return 'UB' + uuid.uuid4().hex[:8].upper() + 'TW'

def getLogger():
    # setting log
    log_file = os.path.join(BASE_DIR, 'resource/logs/ubonextw.log')
    logger = logging.getLogger('rotating_log_application')
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(log_file,
                                       when="D",
                                       interval=1,
                                       backupCount=30)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def getFachLogger():
    # setting log
    log_file = os.path.join(BASE_DIR, 'resource/logs/ubonextw_fach.log')
    logger = logging.getLogger('rotating_fach_log_application')
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(log_file,
                                       when="D",
                                       interval=1,
                                       backupCount=30)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger