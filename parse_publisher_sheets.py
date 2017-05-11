#! /usr/bin/env python3

import os
import re

import pandas as pd

ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


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
            if headers_row is None:
                print('{}: {} doesnt seem to have a headers row'.format(file, sheet))
            else:
                df = xl.parse(sheet, header=headers_row)
                df_as_dict = df.T.to_dict()
                all_df_dict = create_nested_dict(all_df_dict, file, sheet, df_as_dict)
    return all_df_dict


def parse_and_nest_csv(all_df_dict, file):
    df = pd.read_csv(file)
    all_df_dict[file] = {'default': df.T.to_dict()}
    return all_df_dict


def find_headers_row(file, sheet):
    headers_row = 0
    while True:
        with pd.ExcelFile(file) as xl:
            df = xl.parse(sheet, header=headers_row)
            width, height = df.shape
            for heading in df.columns:
                if 'isbn' in str(heading).lower():
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


def make_set_all_isbns(all_pub_dict):
    all_isbns = dict()

    for sourcefile, sheets_dict in all_pub_dict.items():
        for sheet, rows_dict in sheets_dict.items():
            for row, item_dict in rows_dict.items():
                for header, value in item_dict.items():
                    if 'isbn' in header.lower():
                        flat_string = str(value).replace('-', '').replace('.0', '')
                        if ISBNregex.match(flat_string):
                            if all_isbns.get(flat_string):
                                all_isbns[flat_string].append((sourcefile, sheet, item_dict))
                            else:
                                all_isbns[flat_string] = [(sourcefile, sheet, item_dict), ]
    return all_isbns


if __name__ == '__main__':
    all_pub_dict = main()
    all_isbns_set = make_set_all_isbns(all_pub_dict)

    with open('publisher_lists_isbns.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_isbns_set))
