# etextbookSearch

You are going to need 3 directories with data in it.

BookstoreFiles/  
CatalogFiles/  
PublisherFiles/  

## Creating the bookstore files

We receive a pdf from the bookstore, with a list of the texts being used in the coming semester. We only need the ISBNs. When I copy and paste the text - some of the numerals are letters, so I perform some crude OCR correction using simple find and replace.

* change O to 0
* change B to 8
* change l to 1

Since the ISBNs are all the script needs, I am not worried about the text changing.

Save it as a .txt and place in the BookstoreFiles directory.

## Creating the catalog files

I run a List Bibliography report in Symphony. The setting is to choose all titles with a location of ONLINE. The output is the 020 field to a pipe delimited file. I remove the blank lines and save as a .txt file.



## Creating the publisher files

This is the hardest step. As with the other files, we just need the ISBN. Most of the title lists are available on the publishers' websites.

* Project MUSE
	* https://muse.jhu.edu/cgi-bin/book_title_list_html.cgi
* Wiley
	* http://olabout.wiley.com/WileyCDA/Section/id-404513.html
	* Online Books and Book Series
* Springer
	* http://www.springernature.com/gp/librarians/manage-your-account/marc-records/title-list-downloader
	* choose all the English/International subjects and then everything 2005 to present
* Cambridge
	* https://www.cambridge.org/core/services/agents/price-list
	* For USD
* Taylor and Francis (including CRC)
	* request file from rep via email
	* Corey.Worthington@taylorandfrancis.com
	* http://www.crcnetbase.com/page/librarian_resources - by subject code
* Elsevier
	* From https://www.elsevier.com/solutions/sciencedirect/content/book-title-lists
	* Frontlist for current year(s)
	* Backlist for 2014-2006 and older years
	* Skip Freedom Collections and Insights Library Collections and Major Reference works. Note from Tom Diamond says to exclude those.
* UPSO
	* http://www.universitypressscholarship.com/page/230/subscriber-services
	* (View the complete title list for University Press Scholarship Online)
* Knovel
	* Knovel is subscription based. I download a list from the catalog and use that.
	* List bib report - exporting the 020.
* JSTOR
	* http://about.jstor.org/content-on-jstor-books
	* (Download Title List)
* Open Education Resources (OpenStax and others)
	* Run a List bibliography report for titles with Item Category 5 = ETEXTBOOK

The script needs the files to be csv. If all of the files are in a single directory, you can convert the ones that are Excel files into csv using used this utility: http://cwestblog.com/2013/04/12/batch-excel-to-csv-converter-application/. Put the converted csv files into the Publisher Files directory.

# Running findEtextbooks.py

Open the script in Idle. The first time running the script set queryWebService = True. That will allow the script to query the Xid webservice. After the first time, results are stored locally on a file, so that subsequent runs of the script may be run against the local file, depending what's going on. 