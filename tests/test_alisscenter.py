import os, sys
import difflib
import glob
import re

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Load fixture
import aliss_test_case
from data import *


class ALiSSCenterTest(aliss_test_case.ALiSSTestCase):

    def afterSetUp(self):
        aliss_test_case.ALiSSTestCase.afterSetUp(self)

        #add an ALiSSCenter
        self.addCenter( ALISS_CENTER )
        self.center = getattr(self.aliss, ALISS_CENTER['id'])
        self.addContentGroups()
        self.addLicenses()
        self.contentGrpId1 = CONTENT_GROUPS[0]['id']

    def test_initialSetup(self):
        center = self.center
        self.failIf(center == None)

        #check the initial values
        self.assertEquals(center.title, ALISS_CENTER['title']) 
        self.assertEquals(center.description, ALISS_CENTER['description'])
        self.assertEquals(center.gloss_url, ALISS_CENTER['gloss_url']) 
        self.assertEquals(center.gloss_skos, ALISS_CENTER['gloss_skos'])

    def test_changeProperties(self):
        center = self.center

        #check the changing of basic properties
        center.manageProperties(ALISS_CENTER['title'] + ALTER_PROP,
                                ALISS_CENTER['description'] + ALTER_PROP,
                                ALISS_CENTER['gloss_url'] + ALTER_PROP,
                                ALISS_CENTER['gloss_skos'] + ALTER_PROP)

        self.assertEquals(center.title, ALISS_CENTER['title'] + ALTER_PROP)
        self.assertEquals(center.description, ALISS_CENTER['description'] + ALTER_PROP)
        self.assertEquals(center.gloss_url, ALISS_CENTER['gloss_url'] + ALTER_PROP)
        self.assertEquals(center.gloss_skos, ALISS_CENTER['gloss_skos'] + ALTER_PROP)

    def test_basicUpdateAndCleanup(self):
        center = self.center
        self.assertEquals(center.testElementList(), 0)
        center.manageBasicUpdate()
        # check if we have four elements from the content/skos.rdf file
        self.assertEquals(center.testElementList(), 4)

        center.manageCleanUp()
        self.assertEquals(center.testElementList(), 0)

    def test_catalagConsistencyOnContentUpdate(self):
        center = self.center
        center.manageBasicUpdate()
        elements = center.getAllElements()
        self.assertEquals( len(elements), 4)

        # Try to reproduce a case when catalog wasn't updated when pressing 
        # update in content update. But it seams to work here in test.

        center.gloss_skos = ALISS_CENTER2['gloss_skos']
        center.manageBasicUpdate()
        elements = center.getAllElements()
        self.assertEquals( len(elements), 6)

    def test_catalagConsistencyOnLargeContentUpdate(self):
        center = self.center
        # Change center to large skos file "gemet.rdf"
        center.gloss_skos = ALISS_CENTER3['gloss_skos']
        center.manageBasicUpdate()

        elements = center.getAllElements()
        #print "number of concepts for gemet: %s" % len(elements)
        self.assertEquals( len(elements), 5208)

    def test_largeContentUpdateFromWWW(self):
        center = self.center
        # Change center to large skos gemet
        """center.gloss_skos = 'http://www.eionet.eu.int/gemet/gemet-definitions.rdf?langcode=en'
        center.manageBasicUpdate()

        elements = center.getAllElements()
        #print "number of concepts for gemet: %s" % len(elements)
        self.assertEquals( len(elements), 5208)
        center.manageCleanUp()
        """
         # Change center to large skos Glossary
        center.gloss_skos = 'http://glossary.eea.eu.int/EEAGlossary/skos.rdf?fromidx=0&toidx=2000'
        center.manageBasicUpdate()

        elements = center.getAllElements()
        #print "number of concepts for glossary: %s" % len(elements)
        self.assertEquals( len(elements), 1386)

    def test_getTermsForPage(self):
        center = self.center
        center.manageBasicUpdate()
        pageURL = PAGES[0]['URL']
        self.aliss.googleUpdate(center.center_uid, [ CONTENT_GROUPS[0]['id'] ,], ['main_srv'])

        terms = center._get_terms_for_page(pageURL)
        terms = [ term['ElementName'] for term in terms ]      
        expectedTerms = getTermsForPage(pageURL, [ CONTENT_GROUPS[0], ])
        self.assertEquals(terms.sort(), expectedTerms.sort())

    def test__getTopPages(self):
        center = self.center
        center.manageBasicUpdate()
        contentGrp = CONTENT_GROUPS[0]
        self.aliss.googleUpdate(center.center_uid, [ contentGrp['id'] ,], ['main_srv'])

        pages = center._get_top_pages(['dummyNotExistingTerm'],[self.contentGrpId1])

        self.assertEquals(pages, [])

        term_name = TERM_NAMES[0]
        termid = TERMSID_BY_NAME[term_name]
        term_def = self.center.getElements(termid)[0]['definition']
        expected = {'MatchType': 'exact', 'GroupID': contentGrp['id'], 'GroupName': contentGrp['name'],'Pages': [], 'ElementID': termid,'ElementName':term_name,'ElementDefinition':term_def}
        for page in getPagesByTermAndGroup(termid, [ contentGrp, ]):
           expected['Pages'].append({'url': page['URL'], 
                                     'title': page['title']})
        pages = center._get_top_pages([termid],[contentGrp['id'] ])

        #term_name, expectedPages = PAGES_BY_TERM.items()[0]
        term_name=TERM_NAMES[0]
        expectedPages=[]
        contentGrp = CONTENT_GROUPS[0]
        term_def = self.center.getElements(TERMSID_BY_NAME[term_name])[0]['definition']
        for tmppage in getPagesByTermAndGroup(term_name, [contentGrp]):
              expectedPages.append({'url': tmppage['URL'], 'title': tmppage['title'],'preview_img':'','snippet':tmppage['snippet']})
        expected = {'MatchType': 'exact', 'GroupID': contentGrp['id'], 'GroupName': contentGrp['name'],'Pages': expectedPages, 'ElementID': TERMSID_BY_NAME[term_name],'ElementName':term_name,'ElementDefinition':term_def}

        pages = center._get_top_pages([term_name],[contentGrp['id']])

        self.assertEquals(pages, [expected, ])

    def test_googleUpdate(self):
        center = self.center
        center.manageBasicUpdate()
        grpId = CONTENT_GROUPS[0]['id']
        grp = self.aliss.content_group_manager.get_group_item(grpId)
        center.googleUpdate( 'update', [grp,], ['main_srv'])
        pageUrls = [ page.page_url for page in center.getAllPages() ]
        expectedUrls = [ page['URL'] for page in getAllPagesByGroup( [CONTENT_GROUPS[0]]) ]
        self.assertEquals( pageUrls.sort(),  expectedUrls.sort())

    def test_getPagesByTermsAndGroups(self):
        center = self.center
        center.manageBasicUpdate()
        grps = [ CONTENT_GROUPS[0]['id'], CONTENT_GROUPS[1]['id'] ]
        self.aliss.googleUpdate( center.center_uid, grps, ['main_srv'])
        term_ids = TERMSID_BY_NAME.values()
        pages = center.getPagesByGroupsAndTerms(grps, term_ids)
        pagesUrl = [ page.page_url for page in pages ]

        expectedPages = getPagesByGroupsAndTerms(grps, term_ids)
        expectedUrls = [ page['URL'] for page in expectedPages ]
        self.assertEquals(pagesUrl.sort(), expectedUrls.sort())

    def test_getElementsByNames(self):
        center = self.center
        center.manageBasicUpdate()
        term_ids = TERMSID_BY_NAME.values()
        term_names = TERMSID_BY_NAME.keys()
        # Get one term by it's name
        terms = center.getElementsByNames(term_names[0])
        self.assertEquals(len(terms), 1)
        elem = terms[0]
        self.assertEquals(elem.name, term_names[0])

        # Get all terms by it's name
        terms = center.getElementsByNames(term_names)
        self.assertEquals(len(terms), 4)
        gotElemNames = [ elem.name for elem in terms ]
        self.assertEquals(gotElemNames.sort(), term_names.sort() )

    def test_getElementsByNamesSuggest(self):
        center = self.center
        center.manageBasicUpdate()
        term_ids = TERMSID_BY_NAME.values()
        term_names = TERMSID_BY_NAME.keys()

        # Get one term by it's name
        terms = center.getElementsByNames(term_names[0], True)
        self.assertEquals(len(terms), 1)
        elem = terms[0]
        self.assertEquals(elem.name, term_names[0])

        # Get suggestions for 'term'
        search = '%s*' % term_names[0][:3]
        terms = center.getElementsByNames(search, True)
        self.assertEquals(len(terms), len(term_names))
        gotElemNames = [ elem.name for elem in terms ]
        self.assertEquals(gotElemNames.sort(), term_names.sort() )

    def test_getAllElements(self):
        center = self.center
        center.manageBasicUpdate()
        term_ids = TERMSID_BY_NAME.values()
        term_names = TERMSID_BY_NAME.keys()

        gotElems = center.getAllElements()
        gotElemNames = [ elem.name for elem in gotElems ]
        self.assertEquals(gotElemNames, term_names )


def test_suite():
    import unittest

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ALiSSCenterTest))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
