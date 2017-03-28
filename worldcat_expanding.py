#! /usr/bin/env python3

import requests
import pymarc
import os
import re


ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


def get_password():
    with open('worldcat_password.txt', 'r') as f:
        key = f.read()
        return key


def lookup_alternates(ISBN, password):
    response = call_worldcat(ISBN, password)
    # cant get pymarc to parse a marcxml bytestream or string,
    # so writing it to file, which pymarc can parse.  hack.
    filename = "there_should_not_be_a_file_named_thshis.txt"
    with open(filename, 'wb') as f:
        f.write(response)
    isbns_marcrecords = parse_marcxml_for_ISBNS(filename)
    os.remove(filename)
    return isbns_marcrecords


def call_worldcat(ISBN, password):
    url = """http://www.worldcat.org/webservices/catalog/search/worldcat/sru?query=srw.bn+all+"{}"&wskey={}""".format(ISBN, password)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    marc_records_xml = response.content
    return marc_records_xml


def match_regex(string):
    return {i for i in ISBNregex.findall(string)}


def parse_marcxml_for_ISBNS(filename):
    xml_array = pymarc.parse_xml_to_array(filename)
    records = [i for i in xml_array if i]
    all_isbns = set()
    for record in records:
        for field in record.get_fields('020'):
            all_matches = match_regex(field.value())
            if not all_matches:
                print(field.value(), '\t', 'found no match')
                continue
            for tuple_match in all_matches:
                for match in tuple_match:
                    if not match:
                        continue
                    all_isbns.add(match)

    return (all_isbns, records)


if __name__ == '__main__':
    worldcat_key = get_password()
    lookup_alternates('9780123749284', worldcat_key)
