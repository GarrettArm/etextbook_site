#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests


def find_all_options(year):
    url = "http://appl101.lsu.edu/BOOKLET2.nsf/Selector2?OpenForm"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers, params=None)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    all_semesters = soup.find_all('option')
    this_years_choices = [i.attrs for i in all_semesters if 'value' in i.attrs and '2017' in i['value']]
    return this_years_choices

