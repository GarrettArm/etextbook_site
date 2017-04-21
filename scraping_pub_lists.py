#! /usr/bin/env python3

import os
import zipfile

import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Scrape_Booklist:
    def __init__(self, url, folder, payload=None):
        self.payload = payload
        self.url = url
        self.folder = folder

    def make_soup(self):
        response = self.fetch_url_content()
        soup = BeautifulSoup(response, 'html.parser')
        return soup

    def fetch_unless_present(self, url=None, override_ext=None):
        if not url:
            url = self.url
        os.makedirs(self.folder, exist_ok=True)
        if override_ext:
            filename = '{}.{}'.format(os.path.split(url)[1], override_ext)
        else:
            filename = os.path.split(url)[1]
        if filename not in os.listdir(self.folder):
            binary = self.fetch_url_content(url)
            self.write_binary_to_file(binary, filename)

    def fetch_url_content(self, url=None):
        if not url:
            url = self.url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/41.0.2228.0 Safari/537.36', }
        response = requests.get(url, headers=headers, params=self.payload)
        response.raise_for_status()
        return response.content

    def write_binary_to_file(self, binary, filename):
        filepath = os.path.join(self.folder, filename)
        with open(filepath, 'bw') as f:
            f.write(binary)


def scrape_muse():
    folder = 'PublisherFiles/muse_output'
    url = 'https://muse.jhu.edu/cgi-bin/book_title_list_html.cgi'
    MuseScraping = Scrape_Booklist(url, folder)
    partial_urls = [text
                    for elem in MuseScraping.make_soup().find_all('a')
                    if elem.text == 'Download'
                    for attr, text in elem.attrs.items()
                    if attr == 'href']
    for partial_url in partial_urls:
        full_url = 'https://muse.jhu.edu/{}'.format(partial_url)
        MuseScraping.fetch_unless_present(url=full_url)


def scrape_wiley():
    folder = 'PublisherFiles/wiley_output'
    url = 'http://media.wiley.com/assets/2249/63/onlinebooks_list.xls'
    WileyScraping = Scrape_Booklist(url, folder)
    WileyScraping.fetch_unless_present()


def scrape_springer():
    folder = 'PublisherFiles/springer_output'
    url = 'http://ebookrecords.springer.com/marcdownload/file'

    book_codes = ["11641", "11640", "41168", "11642", "11643", "41169", "11644",
                  "11645", "11645-LN", "11646", "41170", "41171", "40367",
                  "11647", "41172", "11648", "41177", "41173", "11649",
                  "11649-LN", "11650", "11651", "11651-LN", "41174", "12059",
                  "41175", "41176", ]
    present_year = datetime.now().year
    all_years = [str(i) for i in range(2005, present_year + 1)]
    payload = {"code": book_codes,
               "year": all_years,
               "format": "EBOOKLIST",
               "grouping": "NONE",
               "SBA": "true",
               "date": "on", }
    SpringerScraping = Scrape_Booklist(url, folder, payload)
    SpringerScraping.fetch_unless_present()
    with zipfile.ZipFile(os.path.join(folder, 'file'), "r") as zip_ref:
        zip_ref.extractall(folder)


def scrape_elsevier():
    url = 'https://www.elsevier.com/solutions/sciencedirect/content/book-title-lists'
    folder = 'PublisherFiles/elsevier_output'
    ElsevierScraping = Scrape_Booklist(url, folder)
    frontlist_urls = [text
                      for elem in ElsevierScraping.make_soup().find_all('a')
                      if 'Frontlist for' in elem.text
                      for attr, text in elem.attrs.items()
                      if attr == 'href']
    backlist_urls = [text
                     for elem in ElsevierScraping.make_soup().find_all('a')
                     if 'Backlist for' in elem.text
                     for attr, text in elem.attrs.items()
                     if attr == 'href']
    all_urls = frontlist_urls
    all_urls.extend(backlist_urls)
    for url in all_urls:
        ElsevierScraping.fetch_unless_present(url=url)


def scrape_UPSO():
    url = 'http://www.universitypressscholarship.com/fileasset/Title%20Lists/UPSO_Alltitles.xls'
    folder = 'PublisherFiles/UPSO_output'
    UPSOScraping = Scrape_Booklist(url, folder)
    UPSOScraping.fetch_unless_present()


def scrape_JSTOR():
    url = 'http://about.jstor.org/sites/default/files/misc/Books_at_JSTOR_Title_List.xls'
    folder = 'PublisherFiles/JSTOR_output'
    JSTORScraping = Scrape_Booklist(url, folder)
    JSTORScraping.fetch_unless_present()


def scrape_cambridge():
    url = 'https://www.cambridge.org/core/services/agents/price-list'
    folder = 'PublisherFiles/cambridge_output'
    CambridgeScraping = Scrape_Booklist(url, folder)
    USD_urls = [text for elem in CambridgeScraping.make_soup().find_all('a')
                if 'For USD click here' in elem.text
                for attr, text in elem.attrs.items()
                if attr == 'href']
    for url in USD_urls:
        CambridgeScraping.fetch_unless_present(url=url, override_ext='xlsx')


def scrape_all():
    disclaimer = 'This script will not repull the datasets already present' \
                 'in the *_output folders.  If you wish to refresh any dataset, ' \
                 'do delete the currently present file.\n\n' \
                 'You must manually provide files for the datasets from ' \
                 'Taylor & Francis, from Knovel, and from OpenStax.\n' \
                 'Any xls, xlsx, or csv in an PublisherFiles\ subfolder ' \
                 'will be used as source data.'
    print(disclaimer)
    scrape_muse()
    scrape_wiley()
    scrape_springer()
    scrape_elsevier()
    scrape_UPSO()
    scrape_JSTOR()
    scrape_cambridge()


if __name__ == '__main__':
    scrape_all()
