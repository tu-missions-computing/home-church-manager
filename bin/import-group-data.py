#!/usr/bin/env python3

from openpyxl import load_workbook
from sys import argv

wb2 = load_workbook(argv[1])
print(wb2.sheetnames)