# coding=utf-8
import webbrowser

import xlrd

a = 0
num = 1
while a < 100:
    ExcelFile = xlrd.open_workbook(r'../open_webPage/query_hive_47730.xlsx')
    sm_id = str(int(ExcelFile.sheet_by_index(0).row_values(num)[0]))
    path = "https://om.ushow.media/#/premium-detail?id=" + sm_id
    webbrowser.open(path)
    a += 1
    num += 1


if __name__ == '__main__':
    pass
