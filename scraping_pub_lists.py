#! /usr/bin/env python3

import os

import requests
from bs4 import BeautifulSoup


# Project MUSE

def make_soup(url):
    response = fetch_url_content(url)
    soup = BeautifulSoup(response, 'html.parser')
    return soup


def fetch_url_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def write_binary_to_file(binary, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'bw') as f:
        f.write(binary)


def fetch_unless_present(list_of_binary_urls):
    output_folder = 'muse_output'
    for partial_url in list_of_binary_urls:
        filename = os.path.split(partial_url)[1]
        if filename not in os.listdir(output_folder):
            muse_xls_url = 'https://muse.jhu.edu/{}'.format(partial_url)
            binary = fetch_url_content(muse_xls_url)
            write_binary_to_file(binary, output_folder, filename)


def scrape_muse():
    muse_soup = make_soup('https://muse.jhu.edu/cgi-bin/book_title_list_html.cgi')
    muse_xls_links = [text
                      for elem in muse_soup.find_all('a')
                      if elem.text == 'Download'
                      for attr, text in elem.attrs.items()
                      if attr == 'href']
    fetch_unless_present(muse_xls_links)


if __name__ == '__main__':
    answer = input('are you sure you want to hit their website for again? (y/n):')
    if answer.lower() == 'y':
        scrape_muse()
    else:
        quit()
