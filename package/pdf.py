import datetime
import io, barcode, os
from decimal import *
from barcode.writer import ImageWriter

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

from scripts.settings import BASE_DIR
from scripts.utils import convertBinaryToBase64String

pdf_config = {
    'msyh_path': os.path.join(BASE_DIR, 'resource', 'pdf', 'template', 'msyh.ttf'),
    'sf_tw': {
        "work_dir": os.path.join(BASE_DIR, 'resource', 'pdf', 'work'),
        "template_path": os.path.join(BASE_DIR, 'resource', 'template', 'pdf', 'shunfeng_tw.pdf'),

        "barcode_no_1": {"x": 2.6, "y": 12.4, "fontsize": 11, "type": 2, "width": 5.5, "height": 1.2},
        "des_code": {"x": 0.7, "y": 11.4, "fontsize": 7, "type": 0},
        "sender_name": {"x": 0.7, "y": 2.6, "fontsize": 7, "type": 0},
        "sender_tel": {"x": 0.7, "y": 2.2, "fontsize": 7, "type": 0},
        "sender_address": {"x": 0.7, "y": 1.8, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 30},
        "receiver_name": {"x": 0.7, "y": 2.6, "fontsize": 7, "type": 0},
        "receiver_tel": {"x": 0.7, "y": 2.2, "fontsize": 7, "type": 0},
        "receiver_address": {"x": 0.7, "y": 1.8, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 30},

        "sf_monthcard_no": {"x": 0.1, "y": 9, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 16},
        "customer_no": {"x": -0.2, "y": 5.8, "fontsize": 11, "type": 2, "width": 5.5, "height": 1.2},

        "goods_desc": {"x": 0.7, "y": 4.8, "fontsize": 7, "type": 0},

        "barcode_no_2": {"x": 2.6, "y": 12.4, "fontsize": 11, "type": 2, "width": 5.5, "height": 1.2},

        "sender_name_2": {"x": 0.7, "y": 2.6, "fontsize": 7, "type": 0},
        "sender_tel_2": {"x": 0.7, "y": 2.2, "fontsize": 7, "type": 0},
        "sender_address_2": {"x": 0.7, "y": 1.8, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 30},
        "receiver_name_2": {"x": 0.7, "y": 2.6, "fontsize": 7, "type": 0},
        "receiver_tel_2": {"x": 0.7, "y": 2.2, "fontsize": 7, "type": 0},
        "receiver_address_2": {"x": 0.7, "y": 1.8, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 30},

        "goods_desc_2": {"x": 0.7, "y": 2.6, "fontsize": 7, "type": 0},
        "goods_num": {"x": 0.7, "y": 2.2, "fontsize": 7, "type": 0}
    }

}

class PdfGenerator():

    def __init__(self, config, x=10, y=15):
        self.config = config
        self.x = x
        self.y = y
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        pdfmetrics.registerFont(TTFont('msyh', config['msyh_path']))

    def generate(self, content_array):
        # generate content pdf
        page_size = (self.x * cm, self.y * cm)

        output = PdfFileWriter()
        for content in content_array:
            now = datetime.datetime.now()

            cf = self.config[content['logistic_category']].copy()
            work_dir = cf['work_dir']
            template_path = cf['template_path']
            del cf['work_dir']
            del cf['template_path']
            temp_file_name = work_dir + "/" + now.strftime("%Y%m%d%H%M%S%f") + ".pdf"

            contentpdf = canvas.Canvas(temp_file_name, pagesize=page_size)
            contentpdf.translate(cm, cm)

            for (k, v) in content.items():
                if k in cf:
                    fontsize = cf[k]["fontsize"]
                    x = cf[k]["x"]
                    y = cf[k]["y"]
                    tp = cf[k]["type"]
                    text = v

                    # set font size and draw text
                    #contentpdf.setFont('STSong-Light', fontsize)
                    contentpdf.setFont('msyh', fontsize)
                    if tp == 0:
                        contentpdf.drawString(x * cm, y * cm, text)
                    elif tp == 1:
                        lineheight = cf[k]["lineheight"]
                        linemaxcharacter = cf[k]["linemaxcharacter"]
                        text_length = len(text)
                        lines = Decimal(text_length / linemaxcharacter).quantize(Decimal('1.'), rounding=ROUND_UP)
                        i = 1
                        while i <= lines:
                            contentpdf.drawString(x * cm, (y - (i - 1) * lineheight) * cm, text[linemaxcharacter * (i - 1):(linemaxcharacter * i)])
                            i += 1
                    elif tp == 2:
                        ean = barcode.get('code128', text, writer=ImageWriter())
                        ean.default_writer_options['write_text'] = False
                        temp_bar_png_file_name = ean.save(work_dir + "/" + text)
                        width = cf[k]["width"]
                        height = cf[k]["height"]
                        contentpdf.drawImage(temp_bar_png_file_name, x * cm, y * cm, width * cm, height * cm)
                        os.remove(temp_bar_png_file_name)
                        contentpdf.drawString((x+1) * cm, (y-0.35) * cm, text)

            contentpdf.save()

            # open template
            input1 = PdfFileReader(open(template_path, "rb"))
            page1 = input1.getPage(0)

            # merge content and template
            input2 = PdfFileReader(open(temp_file_name, "rb"))
            page1.mergePage(input2.getPage(0))

            output.addPage(page1)

            # remove temp
            #os.remove(temp_file_name)
        tmp = io.BytesIO()
        output.write(tmp)
        return tmp.getvalue()


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
