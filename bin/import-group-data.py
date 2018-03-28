#!/usr/bin/env python3

from openpyxl import load_workbook
from sys import argv


class HomeChurch(object):
    def __init__(self, id, covering, sector, name):
        self.id = id
        self.covering = covering
        self.sector = sector
        self.name = name

    def __unicode__(self):
        return "<HomeChurch {} {}>".format(self.id, self.name)


workbook = load_workbook(filename=argv[1])
print(workbook.sheetnames)

for worksheet in workbook:
    print(worksheet.title)
    for column in worksheet[3]:
        print(column['F'])
        print(column.row, column.col_idx, column.value)


