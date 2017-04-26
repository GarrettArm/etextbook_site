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
    csv_list = cleanup_original_text(sourcefile)
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
