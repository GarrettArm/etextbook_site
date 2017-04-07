#! /usr/bin/env python3

import re
import os
import json
from io import BytesIO

import requests
import pymarc


ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


def get_password():
    with open('passwords.txt', 'r') as f:
        parsed_json = json.load(f)
        key = parsed_json['Worldcat']
        return key


def lookup_alternates(ISBN, password):
    response = call_worldcat(ISBN, password)
    isbns_marcrecords = parse_marcxml_for_ISBNS(BytesIO(response))
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


def main(isbn):
    worldcat_key = get_password()
    return lookup_alternates(isbn, worldcat_key)


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    expanded_isbns, expanded_records = main('0803741693')
    a_string = "{}\n\n{}".format(expanded_isbns, "\n".join([str(i.as_dict()) for i in expanded_records]))
    with open(os.path.join('output', 'worldcat_expanded.txt'), 'w') as f:
        f.write(a_string)
