#! /usr/bin/env python3

import os
import csv
import sys


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ('------', 'Dept/Course', 'Publisher', 'Page:', 'User:',
                    'End,of Report', ',,,S,,,', ',,Rc,', 'End of Report'):
        if exclude in line:
            return True
    return False


def read_csv_file(filepath):
    with open(filepath, 'r', encoding='cp1252') as f:
        lines = f.readlines()
        print(lines)
        print('\t', lines)
    return lines


def byte_to_str(item, encoding='cp1252'):
    if isinstance(item, bytes):
        item = item.decode(encoding)
    return item


def cleanup_original_text(csv_source_list):
    headers = ('Dept/Course', 'Section', 'empty1', 'Professor',
               'Author', 'Title', 'empty2', 'ISBN', 'Publisher', 'RcCd', 'STS')
    usable_lines = [byte_to_str(line)
                    for line in csv_source_list
                    if not exclude_line(byte_to_str(line))]
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


def main(sourcefile, dest_path):
    csv_source_list = read_csv_file(sourcefile)
    csv_list = cleanup_original_text(csv_source_list)
    write_csv(csv_list, dest_path)


if __name__ == '__main__':
    try:
        sourcefile = sys.argv[1]
        dest_path = sys.argv[2]
    except IndexError:
        print('')
        print('Change to: "python parse_bookstore_csv.py path_to_sourcefile path_for_dest_file"')
        print('')
        quit()

    main(sourcefile, dest_path)
