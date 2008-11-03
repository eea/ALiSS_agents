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
from Globals                              import InitializeClass
from AccessControl                        import ClassSecurityInfo
from BTrees.OOBTree import OOBTree

#Product imports
from Products.ALiSS.utils                 import utUrlEncode, utIsListType
from Products.ALiSS                       import content_filter
from Products.ALiSS.constants             import *
from Products.ALiSS.managers.google_item  import GoogleItem


class ElementItem:
    """ ElementItem is the "term", it contains information imported from SKOS/rdf, it also contains all results from 
        google search saved as GoogleItems.

            >>> from Products.ALiSS.managers.element_item import ElementItem
            >>> eItem = ElementItem( id=            'eItem',
            ...                      name=          'eName',
            ...                      definition=    'eDefinition',
            ...                      translations=  {'en':'eEN'},
            ...                      center_parent= 'cParent',
            ...                      url=           'eURL')

        Let's check if our initiation of ElementItem worked.

            >>> eItem.id
            'eItem'
            >>> eItem.name
            'eName'
            >>> eItem.definition
            'eDefinition'
            >>> eItem.translations
            {'en': 'eEN'}
            >>> eItem.center_parent
            'cParent'
            >>> eItem.url
            'eURL'
            >>> eItem.google_disabled
            []
            >>> len(eItem.google_collection)
            0

        We have a clean ElementItem with no indexed content groups associated (GoogleItem) stored.
        Lets add some content groups.

            >>> eItem.add_google_item(id=               'itemID',
            ...                       elem_parent=      'eItem',
            ...                       center_parent=    'cParent',
            ...                       group_id=         'grpId',
            ...                       match_level=      'exact')

        We have added a google item with id=gItem, let's try to retrieve it.

            >>> from Products.ALiSS.managers.google_item import GoogleItem
            >>> ourItem = eItem.get_google_collection_item('grpId')
            >>> isinstance(ourItem, GoogleItem)
            True

        Worked fine, there is not much more we can do here except delete the google item :)

            >>> eItem.delete_google_item('grpId')
            >>> ourItem = eItem.get_google_collection_item('grpId')
            >>> ourItem == None
            True

    """
    security = ClassSecurityInfo()

    meta_type = METATYPE_ALISSELEMENT
    def __init__(self, id, name, definition, translations, center_parent, url):
        #identifiers
        self.id =                   id
        self.center_parent =        center_parent

        #element data
        self.url =                  url
        self.name =                 name
        self.definition =           definition
        self.translations =         translations

        #google data
        self.google_collection =    OOBTree()
        self.google_disabled =      []


    def __getattr__(self, name):
        """ """
        if name.startswith('objecttrans_'):
            parts = name.split('_')
            func, lang = parts[0], parts[1]
            return self.objecttrans(lang)
        if name.startswith('objectname_'):
            parts = name.split('_')
            func, lang = parts[0], parts[1]
            return self.objectname(lang)
        raise AttributeError, name

    #################################
    #   GOOGLE_COLLECTION BASICS    #
    #################################
    def __add_google_page(self, group_id, id, google_parent, elem_parent, center_parent, g_server,
                          page_title, page_url, page_snippet, page_directoryTitle, page_cachedSize, page_hostName):
        #add a page
        google_item = self.get_google_collection_item(group_id)
        if google_item:
            google_item.add_google_page(id,
                                        google_parent,
                                        elem_parent,
                                        center_parent,
                                        g_server,
                                        page_title,
                                        page_url,
                                        page_snippet,
                                        page_directoryTitle,
                                        page_cachedSize,
                                        page_hostName)


    #################
    #   BASIC API   #
    #################
    def add_google_page(self, group_id, id, google_parent, elem_parent, center_parent, g_server,
                        page_title, page_url, page_snippet, page_directoryTitle, page_cachedSize, page_hostName):
        #create a new page
        self.__add_google_page(group_id, id, google_parent, elem_parent, center_parent, g_server,
                               page_title, page_url, page_snippet, page_directoryTitle, page_cachedSize, page_hostName)

    def add_google_item(self, id, elem_parent, center_parent, group_id, match_level):
        #create a new item
        item = GoogleItem(id, elem_parent, center_parent, group_id, match_level)
        self.google_collection[group_id] = item

    def delete_google_item(self, group_id):
        #delete an item
        if self.google_collection.get(group_id):
            del self.google_collection[group_id]


    ###############
    #   GETTERS   #
    ###############
    def get_google_collection(self):
        """ get the collection """
        return self.google_collection

    def get_google_ids(self):
        """ get the google ids """
        return self.google_collection.keys()

    def get_google_collection_item(self, group_id):
        """ get an item """
        return self.google_collection.get(group_id, None)

    def get_google_objs(self):
        """ get a list with all items """
        return self.google_collection.values()

    def getCollectionStatistics(self):
        """ """
        return self.get_google_ids()

    def getDefinition(self):
        """ return the definition in UTF8 for this item.
        Use this method when you want to display on UTF8/XHTML webpages. """
        return content_filter.safeXHTMLUnicode(self.definition)

    def getUrl(self):
        """ return the escaped URL for this item.
        Use this method when you want to display valid excaped URL in <a>-tag. """
        return utUrlEncode(self.url)

#TODO: DEPRECATED
#    def getName(self):
#        """ return lower name (for catalog use) """
#        return self.name.lower()


    #####################
    #   TRANSLATIONS    #
    #####################
    def hasTranslations(self):
        """ test if the element contains any translation """
        return len(self.translations.keys())

    def getTranslations(self):
        """ return all translations """
        return self.translations

    def getTranslation(self, lang):
        """ return a translation for a given language code """
        if lang == 'en': return self.name
        try:    return self.translations[lang]
        except: return ''

    def getTranslationsList(self):
        """ """
        trans = self.translations.values()
        trans.append(self.name)
        return trans

    def getTranslationsSuggest(self):
        """ """
        return ' '.join(self.getTranslationsList())

    def objecttrans(self, lang):
        """ used to catalog translations """
        return self.getTranslation(lang)

    def objectname(self, lang):
        """ used to catalog translations """
        return self.getTranslation(lang).lower()

    ####################################
    #   GOOGLE ENABLE/DISABLE RELATED  #
    ####################################
    def mark_google_error(self, group_id):
        #mark the object if an error occur on Google querying
        my_group = self.get_google_collection_item(group_id)
        my_group.google_error = 1
        self.google_collection[group_id] = my_group

    def set_google_enable(self, state, group_id):
        #set enable/disable state
        my_group = self.get_google_collection_item(group_id)
        my_group.google_enable = state
        self.google_collection[group_id] = my_group

    def __add_google_disabled(self, content_id):
        #add a disabled content group
        if content_id not in self.google_disabled:  
            self.google_disabled.append(content_id)

    def addGoogleDisabled(self, content_ids):
        #add a disabled content group
        if not utIsListType(content_ids): 
            content_ids = [ content_ids ]

        for content_id in content_ids:
          self.__add_google_disabled(content_id)

    def __del_google_disabled(self, content_id):
        #remove a disabled content group
        if content_id in self.google_disabled:  
            self.google_disabled.remove(content_id)

    def delGoogleDisabled(self, content_ids):
        #remove a disabled content group
        if not utIsListType(content_ids): 
            content_ids = [ content_ids ]

        for content_id in content_ids:
            self.__del_google_disabled(content_id)

    def isGroupDisabled(self, group_id):
        return group_id in self.google_disabled

    security.setDefaultAccess("allow")

InitializeClass(ElementItem)
