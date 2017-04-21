#! /usr/bin/env python3

import os

import parse_scraped_sourcefiles


list_a = [("muse_output/2013_Complete_Supplement.xls", "2013 Complete Supplement", 3),
          ("muse_output/2014_Complete_Supplement.xls", "2014 Complete Supplement", 3),
          ("muse_output/2011_Complete_Supplement.xls", "2011 Complete Supplement", 3),
          ("muse_output/2010_Complete.xls", "2010 Complete", 3),
          ("muse_output/2011_Complete.xls", "2011 Complete", 3),
          ("muse_output/2017_Complete.xls", "2017 Complete", 3),
          ("muse_output/2016_Complete.xls", "2016 Complete", 3),
          ("muse_output/2015_Complete_Supplement.xls", "2015 Complete Supplement", 3),
          ("muse_output/Archive_Complete_Supplement_II.xls", "Archive Complete Supplement II", 3),
          ("muse_output/Archive_Complete_Supplement_III.xls", "Archive Complete Supplement II", 3),
          ("muse_output/2013_Complete_Supplement_II.xls", "2013 Complete Supplement II", 3),
          ("muse_output/Archive_Complete_Supplement_V.xls", "Archive Complete Supplement V", 3),
          ("muse_output/2012_Complete_Supplement_II.xls", "2012 Complete Supplement II", 3),
          ("muse_output/2012_Complete_Supplement.xls", "2012 Complete Supplement", 3),
          ("muse_output/Archive_Complete_Foundation.xls", "Archive Complete Foundation", 3),
          ("muse_output/2012_Complete.xls", "2012 Complete", 3),
          ("muse_output/Archive_Complete_Supplement_IV.xls", "Archive Complete Supplement IV", 3),
          ("muse_output/2013_Complete.xls", "2013 Complete", 3),
          ("muse_output/2014_Complete.xls", "2014 Complete", 3),
          ("muse_output/2015_Complete.xls", "2015 Complete", 3),
          ("muse_output/Archive_Complete_Supplement.xls", "Archive Complete Supplement", 3),
          ("UPSO_output/UPSO_Alltitles.xls", "UPSO_AllTitles", 0),
          ("elsevier_output/ebook2015.xlsx", "eBook_list_2015", 0),
          ("elsevier_output/ebook2016.xlsx", "eBook_list_2016", 0),
          ("elsevier_output/ebook2010.xlsx", "eBook_list_2010", 0),
          ("elsevier_output/ebookpre2007.xlsx", "WH Integrated pre2007 Backlist", 0),
          ("elsevier_output/ebook2012.xlsx", "eBook_list_2012", 0),
          ("elsevier_output/ebook2013.xlsx", "eBook_list_2013", 0),
          ("elsevier_output/ebook2017.xlsx", "eBook_list_2017", 0),
          ("elsevier_output/ebook2009.xlsx", "WH Integrated 2009 Backlist", 0),
          ("elsevier_output/ebook2011.xlsx", "eBook_list_2011", 0),
          ("elsevier_output/ebook2008.xlsx", "WH Integrated 2008 Backlist", 0),
          ("elsevier_output/ebook2014.xlsx", "eBook_list_2014", 0),
          ("elsevier_output/ebook2007.xlsx", "WH Integrated 2007 Backlist", 0),
          ("springer_output/Springer_eBook_list_20170320_200034.xlsx", "eBook list", 0),
          ("wiley_output/onlinebooks_list.xls", "Order Form", 18),
          ("wiley_output/onlinebooks_list.xls", "All Live", 2),
          ("wiley_output/onlinebooks_list.xls", "Forthcoming", 3),
          ("wiley_output/onlinebooks_list.xls", "Newly Released", 2),
          ("wiley_output/onlinebooks_list.xls", "Withdrawn", 4),
          ("wiley_output/onlinebooks_list.xls", "Book Series Back Volume", None),
          ("wiley_output/onlinebooks_list.xls", "Online Book Series", None),
          ("wiley_output/onlinebooks_list.xls", "Special Collection", 1),
          ("wiley_output/onlinebooks_list.xls", "Subject Page", None),
          ("cambridge_output/58454f443c2168686ad340d1.xlsx", "Cambridge eBooks Feb 2017 USD", 0),
          ("JSTOR_output/Books_at_JSTOR_Title_List.xls", "Books at JSTOR 3-3-17", 0)]


def test_find_headers_row():
    for file, sheet, headers_row in list_a:
        fullpath = os.path.join('PublisherFiles', file)
        assert parse_scraped_sourcefiles.find_headers_row(fullpath, sheet) == headers_row
