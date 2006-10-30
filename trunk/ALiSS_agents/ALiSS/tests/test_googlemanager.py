# use our dummy google for the tests
import dummy_google
from Products.ALiSS.managers import google_manager
google_manager.google = dummy_google

import os, sys
import unittest

from data import *

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from data import *

class GoogleManagerTest(unittest.TestCase):

    def setUp(self):
        self.google_manager = google_manager.GoogleManager()

    def test_googleSearchExact(self):
        gm = self.google_manager

        for term in TERM_NAMES:
            for group in CONTENT_GROUPS:
                exppages=getPagesByTermAndGroup(term,[group,])
                # Make query for exact match level and content group settings
                query ='"'+term+'"'+' site:'+group['filter']
                self.assertEquals(gm._doGoogleSearch(query), ( GOOGLE_RESULTS['metadata'], list(exppages),'done') )
                self.assertEquals(gm.doGoogleSearch(query, start = 0, maxResults = 10, filter = 1,
                                                    restrict='', safeSearch = 0, language = '',
                                                    inputencoding = '', outputencoding = '',\
                                                    http_proxy = None ), 
                                  ( GOOGLE_RESULTS['metadata'], list(exppages),'done') )

        #TODO: enable/fix these tests when we dummy google handles all match_levels like medium and weak 
        # Search all terms
        # query = ' '.join(terms)
        # expected = []
        # for pages in PAGES_BY_TERM.values():
        #    expected.extend(pages)
        # self.assertEquals(gm.doGoogleSearch(query, start = 0, maxResults = 10, filter = 1,
        #                                    restrict='', safeSearch = 0, language = '',
        #                                    inputencoding = '', outputencoding = '',\
        #                                    http_proxy = None ), 
        #                 ( GOOGLE_RESULTS['metadata'], list(expected),'done') )
        
        # Search all terms filter on URL
        #filter = URLS[0]
        #expected = []
        #for pages in PAGES_BY_TERM.values():
        #   expected.extend( [ page for page in pages if filter in page['URL'] ] )
               
        #query = gm.createGoogleQuery(query, CONTENT_GROUPS[0]['filter'], 'exact', CONTENT_GROUPS[0]['pattern'] )
        
        #self.assertEquals(gm.doGoogleSearch(query, start = 0, maxResults = 10, filter = 1,
        #                                    restrict='', safeSearch = 0, language = '',
        #                                    inputencoding = '', outputencoding = '',\
        #                                    http_proxy = None ), 
        #                  ( GOOGLE_RESULTS['metadata'], list(expected),'done') )

    def test_googleSearchMedium(self):
        gm = self.google_manager  
        #terms = PAGES_BY_TERM.keys()
        term=TERM_NAMES[0]
        words=term.split(' ')
        query=''
        for w in words:
         query += ' +%s' % w
        #query='+AA +label2'
        group=CONTENT_GROUPS[0]
        exppages=getPagesByWordsMedium(words,[group,])

        query=query+' site:'+group['filter']
        expected=( GOOGLE_RESULTS['metadata'], list(exppages),'done') 
        got = gm.doGoogleSearch(query, start = 0, maxResults = 10, filter = 1,
                                            restrict='', safeSearch = 0, language = '',
                                            inputencoding = '', outputencoding = '',\
                                            http_proxy = None )
        expectedUrls = [ page['URL'] for page in expected[1] ]
        gotUrls = [ page['URL'] for page in got[1] ]
        self.assertEquals( gotUrls, expectedUrls)
                 
    def test_googleSpellingSuggestion(self):
        gm = self.google_manager
        phrase = 'query'
        self.assertEquals(gm.doSpellingSuggestion(phrase), phrase[::-1])

    def test_doGetCachedPage(self):
        gm = self.google_manager
        self.assertEquals(gm.doGetCachedPage('url'), GOOGLE_CACHED_PAGE)


def test_suite():
    import unittest
    from Testing import ZopeTestCase

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GoogleManagerTest))

    # documentation tests
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/google_page.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/google_item.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)