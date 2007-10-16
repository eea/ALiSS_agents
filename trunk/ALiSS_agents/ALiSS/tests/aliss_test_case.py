from Testing                        import ZopeTestCase
from Products.ALiSS                 import aliss
from Products.ALiSS.aliss_center    import manage_addAlissCenter
from data                           import *

# use our dummy google for the tests
import dummy_google
from Products.ALiSS.managers import google_manager
google_manager.google = dummy_google


ZopeTestCase.installProduct('ALiSS')
ZopeTestCase.installProduct('ZCTextIndex')

class ALiSSTestCase(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        #create an ALiSS instance
        aliss.manage_addALiSS(  self.app,
                                ALISS['id'],
                                ALISS['title'],
                                ALISS['description'])
        self.aliss = getattr(self.app, ALISS['id'])
        self.addContentGroups()
        self.addLicenses()

    def addContentGroups(self):
        for contentGrp in CONTENT_GROUPS:
            self.aliss.manage_add_group_item(contentGrp['id'],
                                             contentGrp['name'],
                                             contentGrp['filter'],
                                             contentGrp['pattern'])

    def addLicenses(self):
        for license in GOOGLE_KEYS:
            self.aliss.manage_add_license_item(license['id'], license['license'])

    def addCenter(self, center_dict):
        """ Adds a center to self.aliss from a center_dict in data.py """
        manage_addAlissCenter(self.aliss, center_dict['id'], 
                                          center_dict['title'], 
                                          center_dict['description'], 
                                          center_dict['gloss_url'], 
                                          center_dict['gloss_skos'])
