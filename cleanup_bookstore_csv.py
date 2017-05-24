#! /usr/bin/env python3

import os
import csv
import re
import sys

import parse_bookstore_csv as Bookstore
from collections import namedtuple

ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


def parse_isbsn_from_csvdata(data):
    bookstore_isbns_nts = dict()

    for num, row in enumerate(bookstore_csv_items):
        if num == 0:
            headers = row
            BookstoreItemNT = namedtuple('BookstoreItemNT', [i.replace('/', '') for i in headers])
            continue
        isbn = row[7].replace('-', '')
        bookstore_isbns_nts[isbn] = BookstoreItemNT(*row[:11])
    return bookstore_isbns_nts


def write_csv(data, dest_path):
    os.makedirs(os.path.split(dest_path)[0], exist_ok=True)
    with open(dest_path,
              "w",
              newline='',
              encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_ALL)
        for line in data:
            writer.writerow(line)


if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
    except IndexError:
        print('\nChange to: "python cleanup_bookstore_csv.py $path/to/raw_bookstore_csv"\n')
        quit()

    if not os.path.isfile(filepath):
        print("\nthat bookstore csv filepath didn't work, maybe it was misspelled?\n")
        exit()

    path, filename = os.path.split(filepath)
    bookstore_csv_items = Bookstore.cleanup_original_text(filepath)
    dest_path = os.path.join(path, 'cleaned_{}'.format(filename))
    write_csv(bookstore_csv_items, dest_path)
    print('\nlook for a "cleaned_{}" in the same folder as the raw bookstore csv\n'.format(filename))
