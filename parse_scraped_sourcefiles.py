#! /usr/bin/env python3

import os

import pandas as pd


output_folders = [i for i in os.listdir('.')
                  if os.path.isdir(os.path.abspath(i)) and '_output' in i]

xl_files = [os.path.join(folder, file)
            for folder in output_folders
            for file in os.listdir(folder)
            if os.path.splitext(file)[1] in ('.xlsx', '.xls')]


def find_headers_row(file, sheet):
    headers_row = 0
    while True:
        with pd.ExcelFile(file) as xl:
            df = xl.parse(sheet, header=headers_row)
            width, height = df.shape
            for heading in df.columns:
                if 'ISBN' in str(heading):
                    return headers_row
            else:
                headers_row += 1
        if headers_row > height:
            break
    return None


def create_nested_dict(dictionary, key, subkey, value):
    if not dictionary:
        dictionary = dict()
    if key in dictionary:
        if subkey in key:
            if dictionary[key][subkey] == value:
                pass
            else:
                print('we never expected {}[{}][{}] to already have a value'.format(dictionary, key, subkey))
                dictionary[key][subkey] = value
        else:
            dictionary[key][subkey] == value
    else:
        dictionary[key] = {subkey: value}
    return dictionary


def parse_and_nest_data(all_df_dict, file):
    with pd.ExcelFile(file) as xl:
        for sheet in xl.sheet_names:
            headers_row = find_headers_row(file, sheet)
            if headers_row:
                df = xl.parse(sheet, header=headers_row)
                all_df_dict = create_nested_dict(all_df_dict, file, sheet, df)
    return all_df_dict


if __name__ == '__main__':
    all_df_dict = dict()
    for file in xl_files:
        all_df_dict = parse_and_nest_data(all_df_dict, file)
