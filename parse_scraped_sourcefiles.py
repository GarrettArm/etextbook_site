#! /usr/bin/env python3

import os

import pandas as pd


def main():
    all_df_dict = dict()
    xl_files, csv_files = lookup_all_xl_csv_files()
    for file in xl_files:
        all_df_dict = parse_and_nest_xl(all_df_dict, file)
    for file in csv_files:
        all_df_dict = parse_and_nest_csv(all_df_dict, file)
    return all_df_dict


def lookup_all_xl_csv_files():
    xl_files = []
    csv_files = []
    for root, dirs, files in os.walk('PublisherFiles'):
        for file in files:
            fullpath = os.path.join(root, file)
            if os.path.splitext(file)[1] in ('.xlsx', '.xls'):
                xl_files.append(fullpath)
            if os.path.splitext(file)[1] == '.csv':
                csv_files.append(fullpath)
    return xl_files, csv_files


def parse_and_nest_xl(all_df_dict, file):
    with pd.ExcelFile(file) as xl:
        for sheet in xl.sheet_names:
            headers_row = find_headers_row(file, sheet)
            if headers_row:
                df = xl.parse(sheet, header=headers_row)
                all_df_dict = create_nested_dict(all_df_dict, file, sheet, df)
    return all_df_dict


def parse_and_nest_csv(all_df_dict, file):
    df = pd.read_csv(file)
    all_df_dict[file] = {'default': df}
    return all_df_dict


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
    if key not in dictionary:
        dictionary[key] = {subkey: value}
    else:
        dictionary[key][subkey] = value
    return dictionary


if __name__ == '__main__':
    all_columns = ''
    all_string = ""
    all_df_dict = main()
    for k, v in all_df_dict.items():
        all_string = "{}\n\n{}".format(all_string, k)
        all_columns = "{}\n\n{}".format(all_columns, k)
        for name, df in v.items():
            all_string = "{}\n{}\n{}".format(all_string, name, df.to_string(max_rows=5, index=False, index_names=False))
            all_columns = "{}\n\{}{}".format(all_columns, name, df.columns)
    os.makedirs('output', exist_ok=True)
    with open(os.path.join('output', 'publisher_files.txt'), 'w') as f:
        f.write(all_columns)
