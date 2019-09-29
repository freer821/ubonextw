from openpyxl import load_workbook
from collections import defaultdict

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
        exporess_code= sheet['A' + str(i)].value
        if exporess_code is None or len(exporess_code) == 0:
            raise Exception('包裹未填写单号！请检查录入')

        # goods 货物
        good_ean_code = str(sheet['K' + str(i)].value).strip()
        good_counts = str(sheet['M' + str(i)].value).strip()
        good_cn_name = str(sheet['L' + str(i)].value).strip()

        if exporess_code in goods:
            goods[exporess_code].append({'ean_code': good_ean_code, 'cn_name': good_cn_name, 'num': good_counts})
        else:
            goods.setdefault(exporess_code, []).append({'ean_code': good_ean_code,'cn_name': good_cn_name, 'num': good_counts})
            # receiver
            receiver_name = str(sheet['B' + str(i)].value).strip()
            receiver_province = str(sheet['C' + str(i)].value).strip()
            receiver_city = str(sheet['D' + str(i)].value).strip()
            receiver_district = str(sheet['E' + str(i)].value).strip()
            receiver_street = str(sheet['F' + str(i)].value).strip()
            receiver_tel = str(sheet['G' + str(i)].value).strip()
            receiver_identity = str(sheet['H' + str(i)].value).strip()
            receiver_postcode = str(sheet['I' + str(i)].value).strip()

            package_weight = str(sheet['J' + str(i)].value).strip()

            # sender
            sender_name = str(sheet['P' + str(i)].value).strip()
            sender_tel = str(sheet['Q' + str(i)].value).strip()
            sender_street = str(sheet['R' + str(i)].value).strip()
            sender_postcode = str(sheet['S' + str(i)].value).strip()
            sender_city = str(sheet['T' + str(i)].value).strip()
            # 备注
            comment = str(sheet['U' + str(i)].value).strip()

            # 额外服务
            insurance = str(sheet['T' + str(i)].value).strip()
            service = str(sheet['U' + str(i)].value).strip()

            sf_month_card = str(sheet['V' + str(i)].value).strip()
            destination_code = str(sheet['W' + str(i)].value).strip()

            packs.append({
                'exporess_code': exporess_code,
                'extra_services': {
                    'services': service,
                    'insurance':insurance
                },
                'package_weight': package_weight,
                'comment': comment,

                'receiver_name': receiver_name.strip(),
                'receiver_province': receiver_province,
                'receiver_city': receiver_city,
                'receiver_district': receiver_district,
                'receiver_street': receiver_street,
                'receiver_tel': receiver_tel.strip(),
                'receiver_identity': receiver_identity.strip(),
                'receiver_postcode': receiver_postcode,

                'sender_name': sender_name,
                'sender_tel': sender_tel,
                'sender_street': sender_street,
                'sender_postcode': sender_postcode,
                'sender_city': sender_city,

                'express_extra': {
                    'sf_month_card': sf_month_card,
                    'destination_code': destination_code
                }

            })

    return packs, goods

