#! /usr/bin/env python3

import re
import os
import cleanup_bookstore_csv as Bookstore
import ebsco_discovery_functions as Discovery
import sys
import json

ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


def parse_isbsn_from_csvdata(data):
    bookstore_isbns = set()
    for row in data:
        for cell in row:
            stringified_cell = str(cell)
            if ISBNregex.match(stringified_cell):
                bookstore_isbns.add(stringified_cell)
    return bookstore_isbns


def return_any_hits(response_json):
    for database in response_json["SearchResult"]["Statistics"]["Databases"]:
        if database["Hits"]:
            return database

def get_discovery_result_for(isbn):
    response = Discovery.main(isbn)
    response_json = json.loads(response)
    return response_json


def is_file_in_holdings(discovery_json):
    all_copy_locations = []
    records_list = discovery_json['SearchResult']['Data']['Records']
    for record in records_list:
        holdings_list = record.get('Holdings')
        if not holdings_list:
            continue
        for holdings_info in holdings_list:
            try:
                copy_info_list = holdings_info['HoldingSimple']['CopyInformationList']
            except KeyError:
                continue
            for copy_info in copy_info_list:
                all_copy_locations.append(copy_info)
    return all_copy_locations


def loop_all_isbns_to_if_holdings(isbns_set):
    isbn_holdings = dict()
    for isbn in isbns_set:
        discovery_json = get_discovery_result_for(isbn)
        if not return_any_hits(discovery_json):
            continue
        all_copy_locations = is_file_in_holdings(discovery_json)
        if all_copy_locations:
            isbn_holdings[isbn] = all_copy_locations
    return isbn_holdings


if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
    except IndexError:
        print('\nChange to: "python Discovery_do_we_hold.py $path/to/raw_bookstore_csv"\n')
        quit()

    if not os.path.isfile(filepath):
        print("\nthat bookstore csv filepath didn't work, maybe it was misspelled?\n")
        exit()

    path, filename = os.path.split(filepath)
    bookstore_csv_items = Bookstore.cleanup_original_text(filepath)
    fixed_ISBN_cells_csv_items = Bookstore.reformat_ISBN_cells(bookstore_csv_items)
    isbns_set = parse_isbsn_from_csvdata(fixed_ISBN_cells_csv_items)
    isbns_holdings = loop_all_isbns_to_if_holdings(isbns_set)
    for k, v in isbns_holdings.items():
        print(k, v)
