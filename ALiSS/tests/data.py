# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania and Eau de Web are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
try:
    from Products.ALiSS.constants import ALISS_PRODUCT_PATH
except:
    ALISS_PRODUCT_PATH = '.'

import os

#other data
ALTER_PROP = ' ch'

#Temporary 'Google Licences'
GOOGLE_KEYS = [{'id':'1', 'license':'abcdefg'},
               {'id':'2', 'license':'hijklmn'}]

URLS = ( 'aaa.com', 'bbb.gov', 'ccc.net' )

#Temporary 'Content Groups'
CONTENT_GROUPS = [{'id':'1', 'name':'AAA',      'filter': URLS[0],               'pattern':''},
                  {'id':'2', 'name':'BBB',      'filter': URLS[1],               'pattern':''},
                  {'id':'3', 'name':'CCC',      'filter': URLS[2],               'pattern':''}]

# TERMS temporary NAME - ID mapping, it has to be consistent with skos data.
TERMSID_BY_NAME = {'term label1':       'whitefish:8080_GlossaryTest_B_term1',
                   'term AA label2':    'whitefish:8080_GlossaryTest_B_term2',
                   'term label3':       'whitefish:8080_GlossaryTest_B_term3',
                   'term label4':       'whitefish:8080_GlossaryTest_B_term4'}

TERM_NAMES = TERMSID_BY_NAME.keys()

GOOGLE_PROPERTIES = {   'start':            1,
                        'maxResults':       1,
                        'filter':           1,
                        'restrict':         'restrict',
                        'safeSearch':       0,
                        'language':         'en',
                        'inputencoding':    'utf8',
                        'outputencoding':   'utf8',
                        'http_proxy':       'http_proxy'}

#ALiSS's basic properties
ALISS = { 'id':             'aliss_id',
          'title':          'ALiSS title',
          'description':    'ALiSS description',
          'gbox':           'http://google.box.com'
        }

#ALiSSCenter's basic properties
ALISS_CENTER = { 'id' :             'center1',
                 'title' :          'Center title',
                 'description' :    'A short center description',
                 'gloss_url' :      'http://glossurl/',
                 'gloss_skos' :     os.path.join(ALISS_PRODUCT_PATH, 'tests', 'content', 'skos.rdf') }

ALISS_CENTER2 = { 'id' :             'center2',
                 'title' :          'Center2 title',
                 'description' :    'A short center2 description',
                 'gloss_url' :      'http://glossurl2/',
                 'gloss_skos' :     os.path.join(ALISS_PRODUCT_PATH, 'tests', 'content', 'skos2.rdf') }
                 
ALISS_CENTER3 = { 'id' :             'center3',
                 'title' :          'Center3 title',
                 'description' :    'A short center3 description',
                 'gloss_url' :      'http://glossurl3/',
                 'gloss_skos' :     os.path.join(ALISS_PRODUCT_PATH, 'tests', 'content', 'gemet.rdf') }

#ALiSS center with real skos url (to test update from web)
ALISS_CENTER4 = { 'id' :             'center4',
                 'title' :          'Center4 title',
                 'description' :    'A short center4 description',
                 'gloss_url' :      'http://glossurl4/',
                 'gloss_skos' :     'http://www.eionet.eu.int/gemet/gemet-definitions.rdf?langcode=en'}

ALISS_CENTERS = [ ALISS_CENTER, ALISS_CENTER2, ALISS_CENTER3]

#ALiSSAgent's basic properties
ALISS_AGENT = { 'id' : 'agent1',
                 'title' : 'Agent title',
                 'description' : 'Agent description' }

# Some Google result structs of pages
# Creating some pages

PAGES = []
for n in range(10):
    PAGES.append( { 'URL' : '%s/%d' % (URLS[n % 3], n),
                    'title' : 'title (HTML)%d' % n,
                    'snippet' : 'snippet showing query context (HTML) %d with terms' % n,
                    'cachedSize' : 'size of cached version of this result, (KB) %d' % n,
                    'relatedInformationPresent' : 'is the "related:" keyword supported? %d' % n,
                    'hostName' :  'used when filtering occurs %d' % n,
                    'directoryCategory' :  { 'fullViewableName': 'the Open Directory category %d' % n,
                                           'specialEncoding' : 'encoding scheme of this directory category %d' % n  },
                    'directoryTitle' : 'Open Directory title of this result (or blank) %d' % n,
                    'summary': 'Open Directory summary for this result (or blank) %d' % n } )

#Exact match
PAGES_BY_TERM = { TERM_NAMES[0] : (PAGES[0],PAGES[8],PAGES[1],PAGES[3]),
                  TERM_NAMES[1] : (PAGES[2],),
                  TERM_NAMES[2] : (PAGES[5], PAGES[6], PAGES[7],PAGES[0],PAGES[2]),
                  TERM_NAMES[3] : (PAGES[8], PAGES[4], PAGES[9], PAGES[0])}


#uses the exact match data to retrieve the medium match.
def getPagesByWordsMedium(words,grps):
    pages=[]
    for term in PAGES_BY_TERM.keys():
        wfound=1
        for w in words:
            if term.find(w)==-1:
                wfound=0
        if wfound:
            for page in PAGES_BY_TERM[term]:
                for grp in grps:
                 if (grp['filter'] in page['URL']) and (page not in pages):
                   pages.append(page)
    return pages

#uses the exact match data to retrieve the weak match.
def getPagesByWordsWeak(words,grps):
    pages=[]
    for term in PAGES_BY_TERM.keys():
        wfound=0
        for w in words:
            if term.find(w)>-1:
                wfound=1
        if wfound:
            for page in PAGES_BY_TERM[term]:
                for grp in grps:
                 if (grp['filter'] in page['URL']) and (page not in pages):
                   pages.append(page)           
    return pages

#Helpmethods for expected data
def getAllPagesByGroup(grps):
    pages = []
    for term in PAGES_BY_TERM.keys():
        pages.extend( getPagesByTermAndGroup(term, grps) )
    return pages
    
def getPagesByTermAndGroup(term, grps):
    pages=[]
    fakePages = PAGES_BY_TERM.get(term,[])
    for page in fakePages:
        for grp in grps:
            if (grp['filter'] in page['URL']) and (page not in pages):
                 pages.append(page)
    return pages

def getTermsForPage(pageURL,grps):
    terms=[]
    for grp in grps:
        if grp['filter'] in pageURL:
            for page in PAGES:
                if pageURL == page['URL']:
                   for term, pages in PAGES_BY_TERM.items():
                       if page in pages:
                           terms.append(term)
                   break
    return terms
    
def getPagesByGroupsAndTerms(grp_ids, term_ids):
    terms = [ label for label,term_id in TERMSID_BY_NAME.items()
                    if term_id in term_ids ]
    pages = []
    groups = [ grp  for grp in CONTENT_GROUPS 
                if grp['id'] in grp_ids ]
    for term in terms:
        pages.extend(getPagesByTermAndGroup(term, groups) )
    return pages
        
def printPageByTerm():
    """used to easily visulize the terms pages data group """
    for tn in TERM_NAMES:
        print '\n'+tn+':\n'
        for page in PAGES_BY_TERM[tn]:
                print page['URL']
            
# Used in dummy google
GOOGLE_RESULTS = { 'metadata' : {   'documentFiltering' : False,
                                    'searchComments' : "'the' is a very common word and was not included in your search",
                                    'estimatedTotalResultsCount': 999,
                                    'estimateIsExact' : False,
                                    'searchQuery': 'search string that initiated this search',
                                    'startIndex' : 0,
                                    'endIndex': 10,
                                    'searchTips': 'human-readable informational message on how to better use Google.',
                                    'directoryCategories' : { 'fullViewableName': 'the Open Directory category',
                                                             'specialEncoding':  'encoding scheme of this directory category'
                                                            },
                                    'searchTime' : 1 },
                    'data' : PAGES_BY_TERM }
                    



GOOGLE_CACHED_PAGE = """A simpel text page is returned, no HTML here.

                        What still reading? It's finnished go!
                     """

#Google Box data
GOOGLE_BOX_RDF = os.path.join(ALISS_PRODUCT_PATH, 'tests', 'content', 'google_box.rdf')