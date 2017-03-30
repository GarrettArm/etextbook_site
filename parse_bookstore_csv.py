#! /usr/bin/env python3

import io

import pandas as pd


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ('------', 'Dept/Course', 'Publisher', 'Page:', 'User:', 'End,of Report', ',,,S,,,', ',,Rc,T,,,'):
        if exclude in line:
            return True
    return False


def cleanup_bookstore_file(filepath):
    headers = ('Dept/Course', 'Section', 'unnamed1', 'Professor', 'Author', 'Title', 'ISBN', 'Publisher', 'RcCd', 'STS')

    with open(filepath, 'r', encoding='cp1252') as f:
        lines = f.readlines()

    file_text = ', '.join(i for i in headers)
    # original data is split into two lines -- this hack concatinates each pair of split lines
    first_line = True
    for line in lines:
        if exclude_line(line):
            continue
        if first_line:
            full_line = line.replace('\n', '')
            first_line = False
            continue
        else:
            full_line = '{}{}'.format(full_line, line.replace('\n', ''))
            first_line = True
            file_text = "{}\n{}".format(file_text, full_line)
    return file_text


def parse_bookstore_files(text):
    headers = ('Dept/Course', 'Section', 'unnamed1', 'Professor', 'Author', 'Title', 'ISBN', 'Publisher', 'RcCd', 'STS')
    return pd.read_csv(io.StringIO(file_text), delimiter=',', names=headers)


if __name__ == '__main__':
    filepath = input('what is the path to your bookstorelist source csv?')
    file_text = cleanup_bookstore_file(filepath)
    df = parse_bookstore_files(file_text)
