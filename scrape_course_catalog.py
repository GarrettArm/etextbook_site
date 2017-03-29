#! /usr/bin/env python3

import os
from collections import namedtuple
import itertools

from bs4 import BeautifulSoup
import requests


def make_a_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
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
        url_template = 'http://appl101.lsu.edu/BOOKLET2.nsf/513bc0fb715ec04e862565c20057c604?OpenView&Start={}'
        url = url_template.format(page_number)
        soup = make_a_soup(url)
        if "No documents found" in soup.find('h2'):
            break
        for table in soup.find_all('table'):
            if table.get('border'):
                for a_href in table.find_all('a'):
                    courses_urls[a_href.text] = a_href.get('href')
    return courses_urls


def scrape_write_all_course_listing(courses_urls):
    for course, url_ending in courses_urls.items():
        os.makedirs('course_listings', exist_ok=True)
        filepath = os.path.join('course_listings', '{}.txt'.format(course))
        if os.path.isfile(filepath):
            continue
        url = 'http://appl101.lsu.edu{}'.format(url_ending)
        soup = make_a_soup(url)
        text = soup.find('pre')
        with open(filepath, 'w') as f:
            f.write(text.text)


def parse_course_listing_texts(filepath):
    course_nts = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if exclude_line(line):
            continue
        course_nts.append(build_namedtuple(line))

        if line:        # this finds the footer line (season & dept)
            season_dept = line.replace('\n', '')
    course_nts.pop()    # this remove the footer line from the main data list
    return course_nts, season_dept


def exclude_line(line):
    if not line.strip():
        return True
    for exclude in ("CROSS-LISTED", "----------", "ENRL", "BEGIN-END"):
        if exclude in line:
            return True
    return False


CourseItem = namedtuple("CourseItem", ["available", "enrollment_count", "abbr_num", "type", "sec_num",
                                       "course_title", "credit_hours", "begin_end", "days", "room",
                                       "building", "special_enrollment", "instructor"])


def build_namedtuple(line):
    return CourseItem(line[:4].strip(), line[4:10].strip(), line[10:21].strip(), line[21:28].strip(), line[28:31].strip(),
                      line[31:55].strip(), line[55:59].strip(), line[59:70].strip(), line[70:79].strip(), line[79:84].strip(),
                      line[85:99].strip(), line[100:117].strip(), line[117:].strip())


if __name__ == '__main__':
    all_course_urls = lookup_all_course_urls()
    scrape_write_all_course_listing(all_course_urls)
    # courseNT_seasonDept = parse_course_listing_texts(filepath_to_scraped_course.txt)
