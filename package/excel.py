from openpyxl import load_workbook
from collections import defaultdict

from scripts.utils import checkItem

def move_next_row(i,sheet):
    if sheet['A'+str(i+1)].value:
        return True
    else:
        return False

def readPackageDataFromXlsx_SF(file):
    wb = load_workbook(filename=file, data_only=True)
    sheet = wb.worksheets[0]

    packs = []
    goods=defaultdict(list)
    i = 2  # 第一行为提示， 第二行为标题，从第三行开始读取
    while move_next_row(i, sheet):
        #
        i += 1
        express_code = checkItem(sheet['A' + str(i)].value, True, '顺丰单号未填写，请检查录入')

        # goods 货物
        good_ean_code = checkItem(sheet['K' + str(i)].value)
        good_counts = checkItem(sheet['M' + str(i)].value, True, '商品数量未录入！请检查录入')
        good_cn_name = checkItem(sheet['L' + str(i)].value, True, '商品名称未录入！请检查录入')

        if express_code in goods:
            goods[express_code].append({'ean_code': good_ean_code, 'cn_name': good_cn_name, 'num': good_counts})
        else:
            goods.setdefault(express_code, []).append({'ean_code': good_ean_code,'cn_name': good_cn_name, 'num': good_counts})
            # receiver
            receiver_name = sheet['B' + str(i)].value
            receiver_province = sheet['C' + str(i)].value
            receiver_city = sheet['D' + str(i)].value
            receiver_district = sheet['E' + str(i)].value
            receiver_street = sheet['F' + str(i)].value
            receiver_tel = sheet['G' + str(i)].value
            receiver_identity = sheet['H' + str(i)].value
            receiver_postcode = sheet['I' + str(i)].value

            package_weight = sheet['J' + str(i)].value

            # sender
            sender_name = sheet['N' + str(i)].value
            sender_tel = sheet['O' + str(i)].value
            sender_street = sheet['P' + str(i)].value
            sender_postcode = sheet['Q' + str(i)].value
            sender_city = sheet['R' + str(i)].value
            # 备注
            comment = sheet['S' + str(i)].value

            # 额外服务
            insurance = sheet['T' + str(i)].value
            service = sheet['U' + str(i)].value

            sf_month_card = sheet['V' + str(i)].value
            destination_code = sheet['W' + str(i)].value

            packs.append({
                'express_code': express_code,
                'extra_services': {
                    'service': checkItem(service),
                    'insurance':checkItem(insurance)
                },
                'package_weight': checkItem(package_weight),
                'comment': checkItem(comment),

                'receiver_name': checkItem(receiver_name, True, '收件人姓名未填写，请检查录入'),
                'receiver_province': checkItem(receiver_province, True, '收件人省份未填写，请检查录入'),
                'receiver_city': checkItem(receiver_city, True, '收件人城市未填写，请检查录入'),
                'receiver_district': checkItem(receiver_district, True, '收件人城区未填写，请检查录入'),
                'receiver_street': checkItem(receiver_street, True, '收件人街道未填写，请检查录入'),
                'receiver_tel': checkItem(receiver_tel, True, '收件人手机未填写，请检查录入'),
                'receiver_identity': checkItem(receiver_identity),
                'receiver_postcode': checkItem(receiver_postcode, True, '收件人邮编未填写，请检查录入'),

                'sender_name': checkItem(sender_name, True, '发件人姓名未填写，请检查录入'),
                'sender_tel': checkItem(sender_tel),
                'sender_street': checkItem(sender_street, True, '发件人地址未填写，请检查录入'),
                'sender_postcode': checkItem(sender_postcode),
                'sender_city': checkItem(sender_city, True, '发件人城市未填写，请检查录入'),

                'express_extra': {
                    'sf_month_card': checkItem(sf_month_card),
                    'destination_code': checkItem(destination_code, True, '目的地代码未填写，请检查录入')
                }

            })

    return packs, goods

