import os
import re
import string
import requests
import csv
from xml.etree import ElementTree

pubFilePath = "PublisherFiles"
storeFilePath = "BookstoreFiles"
catFilePath = "CatalogFiles"
queryWebService = False #needs to be True when running the first time - or when bookstore data changes

# here be isbn patterns

isbnPattern1 = re.compile(r'978(?:-?\d){10}')
isbnPattern2 = re.compile(r'[A-Za-z]((?:-?\d){10})\D')
isbnPattern3 = re.compile(r'[A-zA-Z]((?:-?\d){9}X)')
isbnPattern4 = re.compile(r'a(\d{10})\D')

def findISBNs (filename, path):
    print (filename)
    isbns = []
    with open(os.path.join(path, filename), "r", encoding="ascii", errors="surrogateescape") as isbn_lines:
        read_data = isbn_lines.readlines()
    for line in read_data:
        isbns.extend(isbnPattern1.findall(line))
        isbns.extend(isbnPattern2.findall(line))
        isbns.extend(isbnPattern3.findall(line))
        isbns.extend(isbnPattern4.findall(line))
    stripped = set()
    for y in isbns:
        while '-' in y:    
           stripped.add(y.replace('-',''))
    #    stripped.append(y.translate(str.maketrans('','','-')))
        stripped = list(stripped)
    return stripped

def getMetadata (matchingISBNs, outFileName):
    rows = []
    for z in matchingISBNs:
        urlz = 'http://xisbn.worldcat.org/webservices/xid/isbn/'+z+'?method=getMetadata&format=xml&fl=*&ai=mike.waugh'
        response = requests.get(urlz)
        tree = ElementTree.fromstring(response.content)
        for child in tree:
            rows.append(child.attrib)

    # print to csv
    with open (outFileName, "w") as csvfile:
        try:
            fieldnames = rows[1].keys()
        except:
            fieldnames = "nothing"
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


    
pubISBNs = []
for pubFile in os.listdir(pubFilePath):
    pubISBNs = pubISBNs + (findISBNs(pubFile,pubFilePath))

courseISBNs = []
for storeFile in os.listdir(storeFilePath):
    courseISBNs = courseISBNs + (findISBNs(storeFile,storeFilePath))

#querying webservice for related isbns
#writing the results to file - so as not to overstay our welcome when running multiple times
#queryWebService will query xISBN webservice if true - will read previous results when false

xCourseISBNs = []
if queryWebService:
    for i in courseISBNs:
        url = 'http://xisbn.worldcat.org/webservices/xid/isbn/'+i+'?method=getEditions&format=xml&ai=mike.waugh'
        response = requests.get(url)
        tree = ElementTree.fromstring(response.content)
        for child in tree:
            xCourseISBNs.append(child.text)
    xCourseISBNs = list(set(xCourseISBNs))
    with open("expandedCourseISBNs.txt", "w") as outfile:
        for item in xCourseISBNs:
            outfile.write("%s\n" % item)
else:
    with open("expandedCourseISBNs.txt", "r") as courseFile:
        xCourseISBNs = [book.strip() for book in courseFile]

catISBNs = []
for catFile in os.listdir(catFilePath):
    catISBNs = catISBNs + (findISBNs(catFile,catFilePath))

#match the files
#needToBuy in pubFile but not cat, notDRMfree in cat but not pubfile, matches in pubfile and cat
matches = []
notDRMfree = []
needToBuy = []
noMatch = 0
for x in xCourseISBNs:
    if x in pubISBNs and x in catISBNs:
        matches.append(x)
    elif x in pubISBNs and x not in catISBNs:
        needToBuy.append(x)
    elif x in catISBNs and x not in pubISBNs:
        notDRMfree.append(x)
    else:
        noMatch = noMatch + 1

getMetadata (matches, "matches.csv")
getMetadata (needToBuy, "needToBuy.csv")
getMetadata (notDRMfree, "notDRMfree.csv")

print ("done ")

    

