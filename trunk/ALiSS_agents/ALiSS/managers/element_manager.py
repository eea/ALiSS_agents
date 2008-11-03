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
# Authors:
# Alexandru Ghica - Eau de Web
# Antonio De Marinis - EEA

#Python imports

#Zope imports
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo
from BTrees.OOBTree import OOBTree

#Product imports
from Products.ALiSS                       import utils
from Products.ALiSS.constants             import *
from Products.ALiSS.managers.element_item import ElementItem

#manager class
class ElementManager:
    """ ElementManager contains results of the rdf indexed.

            >>> from Products.ALiSS.managers.element_manager import ElementManager
            >>> class DummyCatalog:
            ...     def __init__(self):
            ...         pass
            ...     def CatalogObject(self, param1):
            ...         pass
            ...     def RecatalogObject(self, param1):
            ...         pass
            ...     def UncatalogObject(self, param1):
            ...         pass

            >>> eManag = ElementManager()
            >>> eManag.catalog = DummyCatalog()

        Let's check if our initiation of ElementItem worked.
            
            >>> len(eManag.get_elements_collection())
            0

        We have a clean ElementManager with no elements (ElementItem) stored.
        Lets add some elements.

            >>> eManag.add_element_item(id=             'elemID',
            ...                        name=            'elemName',
            ...                        definition=      'elemDef',
            ...                        translations=    'elemTrans',
            ...                        url=             'elemURL',
            ...                        center_parent=   'cParent')

        We have added a element with id=elemID, let's try to retrieve it.

            >>> from Products.ALiSS.managers.element_item import ElementItem
            >>> ourElem = eManag.get_element_item('elemID')
            >>> isinstance(ourElem, ElementItem)
            True

        Lets modify the existing element.

            >>> eManag.update_element_basic(id=           'elemID',
            ...                             name=         'elemName2',
            ...                             definition=   'elemDef2',
            ...                             translations= {'en':'eEN'},
            ...                             url=          'elemURL2',)
            >>> ourElem = eManag.get_element_item('elemID')
            >>> ourElem.name
            'elemName2'
            >>> ourElem.definition
            'elemDef2'
            >>> ourElem.translations
            {'en': 'eEN'}
            >>> ourElem.url
            'elemURL2'

        Worked fine, there is not much more we can do here except delete the element :)

            >>> eManag.delete_element_item(['elemID'])
            >>> ourElem = eManag.get_element_item('elemID')
            >>> ourElem == None
            True

    """

    def __init__(self):
        self.__elements_collection = OOBTree()

    #################
    #   BASIC API   #
    #################
    def add_element_item(self, id, name, definition, translations, url, center_parent):
        self.catalog.checkCatalogIndexes(translations)
        item = ElementItem(id, name, definition, translations, center_parent, url)
        self.__elements_collection[id] = item
        self.catalog.CatalogObject(item)

    def update_element_basic(self, id, name, definition, translations, url):
        if self.__elements_collection.has_key(id):
            self.catalog.checkCatalogIndexes(translations)
            item = self.__elements_collection[id]
            item.name =         name
            item.definition =   definition
            item.translations = translations
            item.url =          url
            self.__elements_collection[id] = item
            self.catalog.RecatalogObject(self.get_element_item(id))

    def delete_element_item(self, ids):
        #delete 1 or more items
        catalog = self.catalog
        collection = self.get_elements_collection()
        for id in ids:
            elem = collection[id]

            for google_id in elem.get_google_ids():
                google_item = elem.get_google_collection()[google_id]

                #uncatalog google pages
                catalog.UncatalogObject(google_item.get_page_collection_objs())
                #uncatalog google items
                catalog.UncatalogObject([google_item])

            #uncatalog element items
            catalog.UncatalogObject(elem)

            #delete element items
            del collection[id]


    ###############
    #   GETTERS   #
    ###############
    def get_elements_collection(self):
        #get the collection
        return self.__elements_collection

    def get_elements_ids(self):
        """ Returns the ids/keys as a list from our BTree element collection. """
        return [ id for id in self.__elements_collection.keys() ]

    def get_elements_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__elements_collection.values(), 'name')

    def get_element_item(self, id):
        #get an item
        if self.__elements_collection.has_key(id):
            return self.__elements_collection[id]
        else:
            return None


    #############
    #   OTHER   #
    #############
    def testElementList(self):
        #test if any elements already exist
        return len(self.get_elements_collection())

    def cleanUpContent(self):
        #delets all elements
        self.delete_element_item(self.get_elements_ids())
