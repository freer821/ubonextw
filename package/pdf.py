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
    'msyh_path': os.path.join(BASE_DIR, 'resource', 'template', 'pdf', 'msyh.ttf'),
    'sf_tw': {
        "work_dir": os.path.join(BASE_DIR, 'resource', 'tmp', 'pdf'),
        "template_path": os.path.join(BASE_DIR, 'resource', 'template', 'pdf', 'sf_tw.pdf'),

        "barcode_no": {"x": -0.34, "y": 11.3, "fontsize": 7, "type": 2, "width": 5.6, "height": 0.7},
        "des_code": {"x": 0.35, "y": 10.05, "fontsize": 15, "type": 0},
        "sender_name": {"x": 0.25, "y": 9.25, "fontsize": 7, "type": 0},
        "sender_tel": {"x": 2.25, "y": 9.25, "fontsize": 7, "type": 0},
        "sender_address": {"x": 0.25, "y": 8.85, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 40},
        "receiver_name": {"x": 0.25, "y": 8.05, "fontsize": 7, "type": 0},
        "receiver_tel": {"x": 2.25, "y": 8.05, "fontsize": 7, "type": 0},
        "receiver_address": {"x": 0.25, "y": 7.65, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 40},

        "sf_monthcard_no": {"x": 0.7, "y": 6.85, "fontsize": 7, "type": 0},
        "customer_no": {"x": 3.9, "y": 6.85, "fontsize": 7, "type": 0},

        "goods_desc": {"x": 0.25, "y": 6.4, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 40},

        "barcode_no_1": {"x": 2.25, "y": 5.06, "fontsize": 7, "type": 2, "width": 5.6, "height": 0.7},

        "sender_name_1": {"x": 0.25, "y": 4.22, "fontsize": 7, "type": 0},
        "sender_tel_1": {"x": 2.25, "y": 4.22, "fontsize": 7, "type": 0},
        "sender_address_1": {"x": 0.25, "y": 3.9, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 40},
        "receiver_name_1": {"x": 0.25, "y": 3.1, "fontsize": 7, "type": 0},
        "receiver_tel_1": {"x": 2.25, "y": 3.1, "fontsize": 7, "type": 0},
        "receiver_address_1": {"x": 0.25, "y": 2.77, "fontsize": 7, "type": 1, "lineheight": 0.35, "linemaxcharacter": 40},
        "goods_num": {"x": -0.68, "y": 1, "fontsize": 7, "type": 0},
        "goods_desc_1": {"x": 0.25, "y": 1.4, "fontsize": 7,"type": 1, "lineheight": 0.35, "linemaxcharacter": 30}
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
                    # contentpdf.setFont('STSong-Light', fontsize)
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
                            contentpdf.drawString(x * cm, (y - (i - 1) * lineheight) * cm,
                                                  text[linemaxcharacter * (i - 1):(linemaxcharacter * i)])
                            i += 1
                    elif tp == 2:
                        ean = barcode.get('code128', text, writer=ImageWriter())
                        ean.default_writer_options['write_text'] = False
                        temp_bar_png_file_name = ean.save(work_dir + "/" + text)
                        width = cf[k]["width"]
                        height = cf[k]["height"]
                        contentpdf.drawImage(temp_bar_png_file_name, x * cm, y * cm, width * cm, height * cm)
                        os.remove(temp_bar_png_file_name)
                        contentpdf.drawString((x + 1) * cm, (y - 0.35) * cm, text)

            contentpdf.save()

            # open template
            input1 = PdfFileReader(open(template_path, "rb"))
            page1 = input1.getPage(0)

            # merge content and template
            input2 = PdfFileReader(open(temp_file_name, "rb"))
            page1.mergePage(input2.getPage(0))

            output.addPage(page1)

            # remove temp
            # os.remove(temp_file_name)
        tmp = io.BytesIO()
        output.write(tmp)
        return tmp.getvalue()


def genPdfBase64(packages_array):
    pdf_generator = PdfGenerator(pdf_config)
    data = pdf_generator.generate(packages_array)
    if data:
        return convertBinaryToBase64String(data)
    else:
        return ""
