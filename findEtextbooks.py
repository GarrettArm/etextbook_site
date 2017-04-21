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
    for y in isbns:
        while '-' in y:
            y = y.replace('-', '')
        stripped.add(y)
    return stripped


def getMetadata(matchingISBNs, outFileName):
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
    print(rows)

    # print to csv
    with open(outFileName, "w", encoding="utf-8", errors="surrogateescape") as csvfile:
        try:
            fieldnames = rows[1].keys()
        # I don't know the actual error to expect, so i states an obviously wrong one.
        except EOFError:
            fieldnames = "nothing"
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                lineterminator='\n',
                                extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


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

# querying webservice for related isbns
# writing the results to file - so as not to overstay our welcome when running multiple times
# queryWebService will query xISBN webservice if true - will read previous results when false


xCourseISBNs = set()
if queryWebService:
    for i in courseISBNs:
        url = 'http://xisbn.worldcat.org/webservices/xid/isbn/' \
              '{}?method=getEditions&format=xml&ai=mike.waugh'.format(i)
        response = requests.get(url)
        tree = ET.fromstring(response.content)
        for child in tree:
            xCourseISBNs.add(child.text)
    with open("expandedCourseISBNs.txt", "w") as outfile:
        for item in xCourseISBNs:
            outfile.write("%s\n" % item)
else:
    with open("expandedCourseISBNs.txt", "r") as courseFile:
        xCourseISBNs = [book.strip() for book in courseFile]


# matches in pubfile and cat
# needToBuy in pubfile but not cat
# notDRMfree in cat but not pubfile,
# noMatch -- in the xCourseISBNs but not in pubfile or cat


matches = pubISBNs.intersection(catISBNs).intersection(xCourseISBNs)
needToBuy = pubISBNs.difference(catISBNs).intersection(xCourseISBNs)
notDRMfree = catISBNs.difference(pubISBNs).intersection(xCourseISBNs)


# noMatch = xCourseISBNs.difference(pubISBNs.union(catISBNs))

getMetadata(matches, "matches.csv")
getMetadata(needToBuy, "needToBuy.csv")
getMetadata(notDRMfree, "notDRMfree.csv")


print("done ")

