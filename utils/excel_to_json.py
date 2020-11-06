import json

from openpyxl import load_workbook


def is_odd(num):
    return num % 2 != 0


def get_parent_id(sheet, key):
    for i in sheet['A']:
        if i.value == key:
            return sheet['P%d' % i.row].value


def main():
    file_name = '../config/xuetou.xlsx'
    sheet_name = 'Sheet2'
    sheet = '实验室检验信息'
    work_book = load_workbook(file_name)
    work_sheet = work_book[sheet_name]
    other_sheet = work_book[sheet]
    json_data = {}
    for row in work_sheet.values:
        if row[3]:
            source = list(filter(lambda x: x and is_odd(row.index(x)), row))
            json_data.update(
                {row[0]: {
                    "id": row[0],
                    "label": source.pop(0),
                    "parent_id": get_parent_id(other_sheet, row[0]),
                    "date_key": row[0][:-2] + '01',
                    "source": source,
                    "unit": row[2]
                }}
            )
            # print(json_data)

    with open("../config/jianyan_field.json", "w", encoding='GBK') as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    main()
