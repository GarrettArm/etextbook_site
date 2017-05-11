import os
import re
import requests
import csv

import lxml.etree as ET


queryWebService = True     # needs to be True when running the first time - or when bookstore data changes

ISBNregex = re.compile(r'(\b\d{13}\b)|(\b\d{9}[\d|X]\b)')


def findISBNs(filepath, filename):
    print (filename)
    isbns = []
    full_filepath = os.path.join(filepath, filename)
    with open(full_filepath, "r", encoding="utf-8", errors="surrogateescape") as isbn_lines:
        read_data = isbn_lines.readlines()
    for line in read_data:
        isbns.extend(ISBNregex.findall(line))
    stripped = set()
    stripped = {isbn.replace('-', '') for tuple_group in isbns for isbn in tuple_group if isbn}
    return stripped


def getMetadata(matchingISBNs):
    rows = []
    for isbn in matchingISBNs:
        url = 'http://xisbn.worldcat.org/webservices/xid/isbn/' \
              '{}?method=getMetadata&format=xml&fl=*&ai=mike.waugh'.format(isbn)
        response = requests.get(url)
        tree = ET.fromstring(response.content)
        if 'stat' in tree.attrib:
            print(isbn, 'returning url with', tree.attrib)
        for child in tree:
            rows.append(child.attrib)
    return rows


def write_csv(rows, outFileName):
    try:
        fieldnames = rows[0].keys()
    except IndexError:
        print('{}: no data to write'.format(outFileName))
        return None
    with open(outFileName, "w", encoding="utf-8", errors="surrogateescape") as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                lineterminator='\n',
                                extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def make_isbn_sets():
    pubISBNs = set()
    pubFilePath = "PublisherFiles"
    for pubFile in os.listdir(pubFilePath):
        pubISBNs.update(findISBNs(pubFilePath, pubFile))

    courseISBNs = set()
    storeFilePath = "BookstoreFiles"
    for storeFile in os.listdir(storeFilePath):
        courseISBNs.update(findISBNs(storeFilePath, storeFile))

    catISBNs = set()
    catFilePath = "CatalogFiles"
    for catFile in os.listdir(catFilePath):
        catISBNs.update(findISBNs(catFilePath, catFile))

    return pubISBNs, courseISBNs, catISBNs

# querying webservice for related isbns
# writing the results to file - so as not to overstay our welcome when running multiple times
# queryWebService will query xISBN webservice if true - will read previous results when false


def flatten_set_of_sets(set_of_sets):
    return {i for bunch in set_of_sets for i in bunch}


def find_similar_isbns(isbn):
    similar_isbns = set()
    url = 'http://xisbn.worldcat.org/webservices/xid/isbn/' \
          '{}?method=getEditions&format=xml&ai=mike.waugh'.format(isbn)
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    for child in tree:
        similar_isbns.add(child.text)
    return similar_isbns


if __name__ == '__main__':
    # matches in pubfile and cat
    # needToBuy in pubfile but not cat
    # notDRMfree in cat but not pubfile,
    # noMatch -- in the xCourseISBNs but not in pubfile or cat
    pubISBNs, courseISBNs, catISBNs = make_isbn_sets()
    sets_of_similar_isbns = [find_similar_isbns(isbn) for isbn in courseISBNs]
    xCourseISBNs = flatten_set_of_sets(sets_of_similar_isbns)

    matches = pubISBNs.intersection(catISBNs).intersection(xCourseISBNs)
    needToBuy = pubISBNs.difference(catISBNs).intersection(xCourseISBNs)
    notDRMfree = catISBNs.difference(pubISBNs).intersection(xCourseISBNs)

    # noMatch = xCourseISBNs.difference(pubISBNs.union(catISBNs))

    matches_data = getMetadata(matches)
    write_csv(matches_data, "output/matches.csv")
    need_to_buy = getMetadata(needToBuy)
    write_csv(need_to_buy, "output/needToBuy.csv")
    not_drm_free = getMetadata(notDRMfree)
    write_csv(not_drm_free, "output/notDRMfree.csv")

    print("done ")
