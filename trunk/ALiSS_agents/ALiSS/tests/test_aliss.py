from Products.ALiSS.tests import aliss_test_case

import os, sys
import difflib
import glob
import re

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from dummy_google_manager           import dummyDoGoogleBoxSearch
from Products.ALiSS.constants       import * 
from Products.ALiSS                 import utils
from data                           import *


class ALiSSTest(aliss_test_case.ALiSSTestCase):

    def test_initialSetup(self):
        # Did it work? do we have an ALiSS?
        aliss = self.aliss
        self.failIf(aliss == None)

        # Check if we have a catalog with right ID
        aliss_catalog = aliss.getCatalog()
        self.failIf( aliss_catalog == None)

        # Check if default number of licenses is correct
        # These values should be test values not in the code
        licenses = aliss.getLicenseManager().get_licenses_list()
        self.assertEquals(len(GOOGLE_KEYS), len(licenses))

        self.assertEquals(len (aliss.getGroupsList()), len(CONTENT_GROUPS))
        self.assertEquals( aliss.getDefaultIndexes(), ALISS_INDEXES.keys())

    def test_changeProperties(self):
        aliss = self.aliss

        # Check the changing of basic properties
        aliss.manageProperties( ALISS['title'] + ALTER_PROP,
                                ALISS['description'] + ALTER_PROP,
                                ALISS['gbox'] + ALTER_PROP)

        self.assertEquals(aliss.title, ALISS['title'] + ALTER_PROP)
        self.assertEquals(aliss.description, ALISS['description'] + ALTER_PROP)
        self.assertEquals(aliss.gbox, ALISS['gbox'] + ALTER_PROP)

    def test_licenseManagement(self):
        aliss = self.aliss
        glicense_manager = aliss.getLicenseManager()

        licID, licText = 999, 'a licens code'

        # Add a license
        licenses = glicense_manager.get_licenses_list()
        aliss.manage_add_license_item(id=licID, license=licText)
        noLicenses = len( glicense_manager.get_licenses_list() )
        self.assertEquals( len(licenses)+1, noLicenses)

        licItem = glicense_manager.get_license_item(licID)
        self.failIf(licItem == None)
        self.assertEquals(licItem.license, licText)

        # Update license and verify it
        licTextUpdated = 'updated code'
        aliss.manage_update_license_item(id=licID, license=licTextUpdated)
        licItem = glicense_manager.get_license_item(licID)
        self.failIf(licItem == None)
        self.assertEquals(licItem.license, licTextUpdated)

        # Delete the license
        aliss.manage_delete_licenses([licID,])
        licItem = glicense_manager.get_license_item(licID)
        self.assertEquals(licItem, None)

    def test_contentGroupManagement(self):
        aliss = self.aliss
        content_grp_manager = aliss.content_group_manager

        contentGrp = CONTENT_GROUPS[0]
        contentGrp2 = CONTENT_GROUPS[1]
        contentID = contentGrp['id']

        # Add a content group
        aliss.manage_add_group_item(contentID, contentGrp['name'], contentGrp['filter'], contentGrp['pattern'])
        grpItem = content_grp_manager.get_group_item(contentID)
        self.failIf(grpItem == None)
        self.assertEquals(grpItem.name, contentGrp['name'])
        self.assertEquals(grpItem.filter, contentGrp['filter'])
        self.assertEquals(grpItem.pattern, contentGrp['pattern'])

        # Update a content group
        aliss.manage_update_group_item(contentID, contentGrp2['name'], contentGrp2['filter'], contentGrp2['pattern'])
        grpItem = content_grp_manager.get_group_item(contentID)
        self.failIf(grpItem == None)
        self.assertEquals(grpItem.name, contentGrp2['name'])
        self.assertEquals(grpItem.filter, contentGrp2['filter'])
        self.assertEquals(grpItem.pattern, contentGrp2['pattern'])

        # Update a content group's google search properties
        aliss.manageGoogleSearchProperties( contentID,
                                            GOOGLE_PROPERTIES['start'],
                                            GOOGLE_PROPERTIES['maxResults'],
                                            GOOGLE_PROPERTIES['filter'],
                                            GOOGLE_PROPERTIES['restrict'],
                                            GOOGLE_PROPERTIES['safeSearch'],
                                            GOOGLE_PROPERTIES['language'],
                                            GOOGLE_PROPERTIES['inputencoding'],
                                            GOOGLE_PROPERTIES['outputencoding'],
                                            GOOGLE_PROPERTIES['http_proxy'])
        grpItem = content_grp_manager.get_group_item(contentID)
        self.failIf(grpItem == None)
        self.assertEquals(grpItem.start,            GOOGLE_PROPERTIES['start'])
        self.assertEquals(grpItem.maxResults,       GOOGLE_PROPERTIES['maxResults'])
        self.assertEquals(grpItem.g_filter,         GOOGLE_PROPERTIES['filter'])
        self.assertEquals(grpItem.restrict,         GOOGLE_PROPERTIES['restrict'])
        self.assertEquals(grpItem.safeSearch,       GOOGLE_PROPERTIES['safeSearch'])
        self.assertEquals(grpItem.language,         GOOGLE_PROPERTIES['language'])
        self.assertEquals(grpItem.inputencoding,    GOOGLE_PROPERTIES['inputencoding'])
        self.assertEquals(grpItem.outputencoding,   GOOGLE_PROPERTIES['outputencoding'])
        self.assertEquals(grpItem.http_proxy,       GOOGLE_PROPERTIES['http_proxy'])

        # Update a content group's search type
        search_type = 'all'
        aliss.manageSearchType(contentID, search_type)
        grpItem = content_grp_manager.get_group_item(contentID)
        self.failIf(grpItem == None)
        self.assertEquals(grpItem.search_type, search_type)

        # Delete a content group
        aliss.manage_delete_groups(ids=[contentID,])
        grpItem = content_grp_manager.get_group_item(contentID)
        self.failIf(grpItem != None)

    def test_contentGroupInformation(self):
        # Check a content group information
        aliss = self.aliss
        self.assertEquals(aliss.getGroupItemData(),  ['add', '', '', '', ''])

    def test_groupsInUse(self):
        aliss = self.aliss
        self.addCenter( ALISS_CENTER )

        groupsUsed = aliss.getGroupsUsed()
        gotIds = groupsUsed.keys()
        expectedIds = [ cGrp['id'] for cGrp in CONTENT_GROUPS ]
        # Check if all expected id are there
        compIds = [ id for id in expectedIds if id in gotIds ]
        self.assertEquals(compIds, expectedIds)

        gotValues = groupsUsed.values()
        # Check if all expected content group names are there
        expectedValues = [ cGrp['name'] for cGrp in CONTENT_GROUPS ]
        compValues = [ val for val in expectedValues if val in gotValues ]
        self.assertEquals(compValues, expectedValues)

    def test_catalog(self):
        # Check if any aliss catalog instance
        catalog = [self.aliss.getCatalog()]
        self.assertEquals(len(catalog), 1)

    def test_centers(self):
        # Check if centers are returned via catalog
        self.addCenter( ALISS_CENTER )
        
        centers = self.aliss.getAllCenters()
        self.assertEquals(len(centers), 1)
        
    def test_licenseInformation(self):
        # Check an license information
        aliss = self.aliss
        self.assertEquals(aliss.getLicenseItemData(), ['add', '', ''])

        self.assertEquals( len(aliss.getLicensesList()), 2)

    def test_googleUpdate(self):
        #add two centers
        self.addCenter( ALISS_CENTER )
        self.addCenter( ALISS_CENTER2 )
        aliss = self.aliss

        #create the IDs list
        center1 = getattr(aliss, ALISS_CENTER['id'])
        center2 = getattr(aliss, ALISS_CENTER['id'])
        my_centers_list = ','.join([center1.center_uid, center2.center_uid])

        grp = CONTENT_GROUPS[0]
        # Load elements/terms into the center
        center1.manageBasicUpdate()
        center2.manageBasicUpdate()

        #check
        aliss.googleUpdate( centers_list=my_centers_list, groups=[ grp['id'], ], servers=['main_srv'])
        self.verifyAfterGoogle(center1)
        self.verifyAfterGoogle(center2)

    def test_googleBoxUpdate(self):
        #add two centers
        self.addCenter( ALISS_CENTER )
        self.addCenter( ALISS_CENTER2 )
        aliss = self.aliss

        #create the IDs list
        center1 = getattr(aliss, ALISS_CENTER['id'])
        center2 = getattr(aliss, ALISS_CENTER2['id'])
        my_centers_list = ','.join([center1.center_uid, center2.center_uid])

        grp = CONTENT_GROUPS[0]
        # Load elements/terms into the center
        center1.manageBasicUpdate()
        center2.manageBasicUpdate()

        center1._doGoogleBoxSearch = dummyDoGoogleBoxSearch
        center2._doGoogleBoxSearch = dummyDoGoogleBoxSearch

        #check
        aliss.googleUpdate( centers_list=my_centers_list, groups=[grp['id'], ], servers=['main_srv', 'box_srv'])

        pageUrls = [page.page_url for page in center1.getAllPages()]
        self.assertEquals(len(pageUrls), 14)

        pageUrls = [page.page_url for page in center2.getAllPages()]
        self.assertEquals(len(pageUrls), 18)

    def test_googleResume(self):
        #add two centers
        self.addCenter( ALISS_CENTER )
        self.addCenter( ALISS_CENTER2 )
        aliss = self.aliss

        #create the IDs list
        center1 = getattr(aliss, ALISS_CENTER['id'])
        center2 = getattr(aliss, ALISS_CENTER2['id'])
        my_centers_list = ','.join([center1.center_uid, center2.center_uid])

        grp = CONTENT_GROUPS[0]
        # Load elements/terms into the center
        center1.manageBasicUpdate()
        center2.manageBasicUpdate()

        #check
        aliss.googleResume( centers_list=my_centers_list, groups=[ grp['id'], ] )
        self.verifyAfterGoogle(center1)
        self.verifyAfterGoogle(center2)

    def verifyAfterGoogle(self, center):
        pageUrls = [ page.page_url for page in center.getAllPages() ]
        expectedUrls = [ page['URL'] for page in getAllPagesByGroup( [CONTENT_GROUPS[0]]) ]
        self.assertEquals( pageUrls.sort(),  expectedUrls.sort())

    def verifyAfterGoogleBox(self, center):
        pageUrls = [ page.page_url for page in center.getAllPages() ]
        self.assertEquals( len(pageUrls), 18)

def test_suite():
    import unittest
    from Testing import ZopeTestCase

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ALiSSTest))

    # documentation tests
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/google_license_manager.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/content_group_manager.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))

    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
