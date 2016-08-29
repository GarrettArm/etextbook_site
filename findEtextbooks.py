import os
import re
import requests
import csv

import lxml.etree as ElementTree

pubFilePath = "PublisherFiles"
storeFilePath = "BookstoreFiles"
catFilePath = "CatalogFiles"
queryWebService = False     # needs to be True when running the first time - or when bookstore data changes


isbnPattern1 = re.compile(r'978(?:-?\d){10}')
isbnPattern2 = re.compile(r'[A-Za-z]((?:-?\d){10})\D')
isbnPattern3 = re.compile(r'[A-zA-Z]((?:-?\d){9}X)')
isbnPattern4 = re.compile(r'a(\d{10})\D')


def findISBNs(filepath, filename):
    print (filename)
    isbns = []
    with open(os.path.join(filepath, filename), "r", encoding="ascii", errors="surrogateescape") as isbn_lines:
        read_data = isbn_lines.readlines()
    for line in read_data:
        isbns.extend(isbnPattern1.findall(line))
        isbns.extend(isbnPattern2.findall(line))
        isbns.extend(isbnPattern3.findall(line))
        isbns.extend(isbnPattern4.findall(line))
    stripped = set()
    for y in isbns:
        while '-' in y:
            y = y.replace('-', '')
        stripped.add(y)
    return stripped


def getMetadata(matchingISBNs, outFileName):
    rows = []
    for z in matchingISBNs:
        urlz = 'http://xisbn.worldcat.org/webservices/xid/isbn/{}?method=getMetadata&format=xml&fl=*&ai=mike.waugh'.format(z)
        response = requests.get(urlz)
        tree = ElementTree.fromstring(response.content)
        if 'stat' in tree.attrib:
            print(z, 'returning url with', tree.attrib)
        for child in tree:
            rows.append(child.attrib)

    # print to csv
    with open(outFileName, "w") as csvfile:
        try:
            fieldnames = rows[1].keys()
        except:
            fieldnames = "nothing"
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


pubISBNs = set()
for pubFile in os.listdir(pubFilePath):
    pubISBNs.update(findISBNs(pubFilePath, pubFile))

courseISBNs = set()
for storeFile in os.listdir(storeFilePath):
    courseISBNs.update(findISBNs(storeFilePath, storeFile))

catISBNs = set()
for catFile in os.listdir(catFilePath):
    catISBNs.update(findISBNs(catFilePath, catFile))

# querying webservice for related isbns
# writing the results to file - so as not to overstay our welcome when running multiple times
# queryWebService will query xISBN webservice if true - will read previous results when false

# xCourseISBNs = []
# if queryWebService:
#     for i in courseISBNs:
#         url = 'http://xisbn.worldcat.org/webservices/xid/isbn/{}?method=getEditions&format=xml&ai=mike.waugh'.format(i)
#         response = requests.get(url)
#         tree = ElementTree.fromstring(response.content)
#         for child in tree:
#             xCourseISBNs.append(child.text)
#     xCourseISBNs = list(set(xCourseISBNs))
#     with open("expandedCourseISBNs.txt", "w") as outfile:
#         for item in xCourseISBNs:
#             outfile.write("%s\n" % item)
# else:
#     with open("expandedCourseISBNs.txt", "r") as courseFile:
#         xCourseISBNs = [book.strip() for book in courseFile]


# matches in pubfile and cat
# needToBuy in pubfile but not cat
# notDRMfree in cat but not pubfile,
# noMatch -- in the xCourseISBNs but not in pubfile or cat

matches = pubISBNs.intersection(catISBNs)
needToBuy = pubISBNs.difference(catISBNs)
notDRMfree = catISBNs.difference(pubISBNs)
# noMatch = xCourseISBNs.difference(pubISBNs.union(catISBNs))

getMetadata(matches, "matches.csv")
getMetadata(needToBuy, "needToBuy.csv")
getMetadata(notDRMfree, "notDRMfree.csv")


print("done ")
