from openpyxl import load_workbook
from io import BytesIO

def move_next_row(i,sheet):
    if sheet['B'+str(i+1)].value:
        return True
    else:
        return False


def readPackageDataFromXlsx(file):
    wb = load_workbook(filename=file, data_only=True)
    sheet = wb.worksheets[0]

    packs = []
    i = 2  # 第一行为提示， 第二行为标题，从第三行开始读取
    while move_next_row(i, sheet):
        #
        i += 1
        inland_code= sheet['B' + str(i)].value
        if inland_code is None or len(inland_code) == 0:
            continue

        sender = sheet['G' + str(i)].value
        sender_addr = sheet['F' + str(i)].value
        sender_tel = sheet['H' + str(i)].value
        receiver = sheet['J' + str(i)].value
        receiver_addr = sheet['I' + str(i)].value
        receiver_tel = sheet['K' + str(i)].value
        goods_descr = sheet['C' + str(i)].value
        goods_quantity = sheet['D' + str(i)].value
        des_code = sheet['E' + str(i)].value
        sf_monthcard_no = sheet['L' + str(i)].value
        logistic_product = sheet['M' + str(i)].value
        comment = sheet['N' + str(i)].value

        packs.append({
            'inland_code': str(inland_code).strip(),
            'sender': str(sender).strip(),
            'sender_addr': str(sender_addr).strip(),
            'sender_tel': str(sender_tel).strip(),
            'receiver': str(receiver).strip(),
            'receiver_addr': str(receiver_addr).strip(),
            'receiver_tel': str(receiver_tel).strip(),
            'goods_descr': str(goods_descr).strip(),
            'goods_quantity': str(goods_quantity).strip(),
            'des_code': str(des_code).strip(),
            'sf_monthcard_no': str(sf_monthcard_no).strip(),
            'logistic_product': str(logistic_product).strip(),
            'comment': str(comment).strip()
        })

    return packs

