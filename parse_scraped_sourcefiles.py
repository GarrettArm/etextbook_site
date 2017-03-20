#! /usr/bin/env python3

import os

import openpyxl


def read_workbook(filepath):
    return openpyxl.load_workbook(filepath)


def find_parse_all_xlsx():
    output_folders = [os.path.abspath(i)
                      for i in os.list('.')
                      if os.path.isdir(os.path.abspath(i)) and '_output' in i]
    print(output_folders)
