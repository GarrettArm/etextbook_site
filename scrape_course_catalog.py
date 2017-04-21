#! /usr/bin/env python3

import os
import itertools
import re

from bs4 import BeautifulSoup
import requests


season_dept_pattern = re.compile(r'(First|Second|)(Winter|Summer|Spring|Fall)'
                                 '(Module|)(\d{4})(Intersession|)([\S]+)')


def make_a_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers, params=None)
    response.raise_for_status()
    return response


def make_a_soup(url):
    response = make_a_request(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def lookup_all_course_urls():
    courses_urls = dict()
    for i in itertools.count():
        page_number = (i * 29) + 1
        url_template = 'http://appl101.lsu.edu/BOOKLET2.nsf/' \
                       '513bc0fb715ec04e862565c20057c604?OpenView&Start={}'
        url = url_template.format(page_number)
        soup = make_a_soup(url)
        if "No documents found" in soup.find('h2'):
            break
        for table in soup.find_all('table'):
            if table.get('border'):
                for a_href in table.find_all('a'):
                    courses_urls[a_href.text] = a_href.get('href')
    return courses_urls


def scrape_write_all_course_listings(courses_urls):
    os.makedirs('course_listings', exist_ok=True)
    all_course_files = [file
                        for root, dirs, files in os.walk('course_listings')
                        for file in files
                        if os.path.isfile(os.path.join(root, file))]
    for course, url_ending in courses_urls.items():
        if '{}.txt'.format(course) in all_course_files:
            continue
        url = 'http://appl101.lsu.edu{}'.format(url_ending)
        soup = make_a_soup(url)
        text = soup.find('pre')
        pre, season, post, year, modulator, dept = find_season_dept_in_last_line(text.text)
        target_dir = os.path.join('course_listings',
                                  year,
                                  '_'.join(i for i in (pre, season, post, year, modulator) if i)
                                  )
        os.makedirs(target_dir, exist_ok=True)
        target_filepath = os.path.join(target_dir, '{}.txt'.format(course))
        with open(target_filepath, 'w') as f:
            f.write(text.text)


def find_season_dept_in_last_line(text):
    for line in text.split('\n'):
        if not exclude_line(line):
            last_line = line
    return season_dept_pattern.findall(last_line.replace(' ', ''))[0]


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ("CROSS-LISTED", "----------", "ENRL", "BEGIN-END"):
        if exclude in line:
            return True
    return False


if __name__ == '__main__':
    all_course_urls = lookup_all_course_urls()
    scrape_write_all_course_listings(all_course_urls)
