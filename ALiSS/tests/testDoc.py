import os
import sys
import unittest
from Testing import ZopeTestCase

ZopeTestCase.utils.startZServer()

import aliss_test_case
from Products.ALiSS.aliss_center import manage_addAlissCenter
from Products.ALiSS.aliss_agent import manage_addAlissAgent
from data import *

# acquire relevant paths
currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.join(currentDir, '..')
sys.path.append(parentDir)


from zope.testing.doctest import DocFileSuite, DocTest

class DocTests(ZopeTestCase.Functional, aliss_test_case.ALiSSTestCase):
    """ Convenient class """

    def afterSetUp(self):
        aliss_test_case.ALiSSTestCase.afterSetUp(self)
        manage_addAlissCenter(self.aliss, ALISS_CENTER['id'], 
                                          ALISS_CENTER['title'], 
                                          ALISS_CENTER['description'], 
                                          ALISS_CENTER['gloss_url'], 
                                          ALISS_CENTER['gloss_skos'])
        self.center = getattr(self.aliss, ALISS_CENTER['id'])

        manage_addAlissAgent(self.aliss,  ALISS_AGENT['id'], 
                                          ALISS_AGENT['title'], 
                                          ALISS_AGENT['description'])
        self.agent = getattr(self.aliss, ALISS_AGENT['id'])
        self.addContentGroups()
        self.addLicenses()
        self.center.manageBasicUpdate()
        self.contentGrpId1 = CONTENT_GROUPS[0]['id']
        self.contentGrpId2 = CONTENT_GROUPS[1]['id']
        self.aliss.googleUpdate(self.center.center_uid, [ self.contentGrpId1,self.contentGrpId2], ['main_srv'])
        self.agent.manageContentGroups([self.contentGrpId1,])
        self.agent.manageAlissCenters([self.center.center_uid,])
# Appends the parent dir to the module search path

def test_suite():
    return unittest.TestSuite((
        ZopeTestCase.FunctionalDocFileSuite('howto_aliss_client_side.txt',
                     package='doc',
                     test_class=DocTests ),
        ))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
