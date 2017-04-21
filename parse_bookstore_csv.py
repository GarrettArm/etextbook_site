#! /usr/bin/env python3

import os
import csv


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ('------', 'Dept/Course', 'Publisher', 'Page:', 'User:', 'End,of Report', ',,,S,,,', ',,Rc,T,,,'):
        if exclude in line:
            return True
    return False


def cleanup_original_text(filepath):
    headers = ('Dept/Course', 'Section', 'empty1', 'Professor',
               'Author', 'Title', 'empty2', 'ISBN', 'Publisher', 'RcCd', 'STS')

    with open(filepath, 'r', encoding='cp1252') as f:
        lines = f.readlines()
    usable_lines = [line for line in lines if not exclude_line(line)]

    spamreader = csv.reader(usable_lines, delimiter=',', quotechar='"')

    all_lines = [headers, ]
    for num, line in enumerate(spamreader):
        if num % 2 == 0:
            combined_line = [i.replace('\n', '') for i in line]
        elif num % 2 == 1:
            combined_line.extend(i. replace('\n', '') for i in line)
            all_lines.append(combined_line)
    return all_lines


def write_csv(data, dest_path):
    os.makedirs(os.path.split(dest_path)[0], exist_ok=True)
    with open(dest_path, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for line in data:
            writer.writerow(line)


def main(sourcefile, dest_path):
    csv_list = cleanup_original_text('BookstoreFiles/fallbooklist.csv')
    write_csv(csv_list, 'output/bookstore.csv')


if __name__ == '__main__':
    print('Do you trust the csv the Bookstore provided (with books required for upcoming classes) is up-to-date?')

    sourcefile = 'BookstoreFiles/fallbooklist.csv'
    dest_path = 'output/bookstore.csv'

    main(sourcefile, dest_path)
