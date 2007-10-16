# use our dummy google for the tests
import os, sys
import unittest

from data import *
from Products.ALiSS.managers.element_manager import ElementManager
from Products.ALiSS.managers.element_item import ElementItem
from BTrees.OOBTree import OOBTree


if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from data                     import *

class ElementItemTest(unittest.TestCase):
    
    def setUp(self):
        self.ELEMENT = { 'id' : 'elementId',
                         'name' : 'element name',
                         'definition' : 'element definition',
                         'translations' : {'en':'element translation'},
                         'url' : 'element url',
                         'center_parent' : 'center_parent' }
                         
    def test_initElementItem(self):
        EL = self.ELEMENT
        element = ElementItem( EL['id'],
                               EL['name'],
                               EL['definition'],
                               EL['translations'],
                               EL['center_parent'],
                               EL['url'] )
        self.assertEquals(element.id, EL['id'])
        self.assertEquals(element.name, EL['name'])
        self.assertEquals(element.definition, EL['definition'])
        self.assertEquals(element.translations, EL['translations'])
        self.assertEquals(element.center_parent, EL['center_parent'])
        self.assertEquals(element.url, EL['url'])
        self.assertEquals(type(element.google_collection), type(OOBTree()))
        self.assertEquals(len(element.google_collection), len(OOBTree()))
        self.assertEquals(element.google_disabled, [])


class ElementManagerTest(unittest.TestCase):
    
    def setUp(self):
        self.element_manager = element_manager.ElementManager()
    
   
        
def test_suite():
    import unittest
    from Testing import ZopeTestCase

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ElementManagerTest))
    suite.addTest(unittest.makeSuite(ElementItemTest))

    # documentation tests
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/element_item.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))
    suite.addTest(ZopeTestCase.doctest.FunctionalDocFileSuite('managers/element_manager.py',
                                                              package='Products.ALiSS',
                                                              test_class=ZopeTestCase.ZopeTestCase))

    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)