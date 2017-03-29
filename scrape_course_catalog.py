#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests


def make_main_page_soup():
    url = "http://appl101.lsu.edu/BOOKLET2.nsf/Selector2?OpenForm"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers, params=None)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def find_all_depts(soup):
    url = "http://appl101.lsu.edu/BOOKLET2.nsf/Selector2?OpenForm"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers, params=None)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    dept_elem = [i for i in soup.find_all('select') if i.attrs['name'] == 'Department'][0]
    dept_elem_subtext = [i for i in dept_elem.text.split('\n') if i]
    return dept_elem_subtext


def find_all_semesters(soup):
    all_choices = [i.attrs for i in soup.find_all('option') if 'value' in i.attrs]
    return all_choices


def get_dept_semester_listing(dept, semester):
    pass


if __name__ == '__main__':
    main_page_soup = make_main_page_soup()
    semester_options = [v for item in find_all_semesters(main_page_soup) for k, v in item.items()]
    selected_year = input('which year would you like? [yyyy]: ')
    semesters_in_year = [i for i in semester_options if selected_year in i]
    print('these are the available options in that year: {}'.format(semesters_in_year))
    while True:
        selected_semester = input('which of the above semesters would you like? ')
        if selected_semester in semester_options:
            break
    print(selected_semester)
    all_depts = find_all_depts(main_page_soup)
