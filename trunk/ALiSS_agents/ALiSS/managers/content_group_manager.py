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
from Globals                    import InitializeClass
from AccessControl              import ClassSecurityInfo
from persistent.mapping         import PersistentMapping

#Product imports
from Products.ALiSS.constants   import *
from Products.ALiSS             import utils


class ContentGroup:
    """ A ContentGroup item store the data of the queries used on Google update.

            >>> from Products.ALiSS.managers.content_group_manager import ContentGroup
            >>> from Products.ALiSS.constants                      import ALISS_DEFAULT_GOOGLE
            >>> gConGr = ContentGroup( id=        'cgId',
            ...                        name=      'cgName',
            ...                        filter=    'cgFilter',
            ...                        pattern=   'cgPattern')

        We have now created a content group item and stored it in gConGr. Let's check if the values are ok.

            >>> gConGr.id
            'cgId'
            >>> gConGr.name
            'cgName'
            >>> gConGr.filter
            'cgFilter'
            >>> gConGr.pattern
            'cgPattern'
            >>> gConGr.last_updated
            ''
            >>> gConGr.search_type
            'exact'

            >>> gConGr.start == ALISS_DEFAULT_GOOGLE['start']
            True
            >>> gConGr.maxResults == ALISS_DEFAULT_GOOGLE['maxResults']
            True
            >>> gConGr.g_filter == ALISS_DEFAULT_GOOGLE['filter']
            True
            >>> gConGr.restrict == ALISS_DEFAULT_GOOGLE['restrict']
            True
            >>> gConGr.safeSearch == ALISS_DEFAULT_GOOGLE['safeSearch']
            True
            >>> gConGr.language == ALISS_DEFAULT_GOOGLE['language']
            True
            >>> gConGr.inputencoding == ALISS_DEFAULT_GOOGLE['inputencoding']
            True
            >>> gConGr.outputencoding == ALISS_DEFAULT_GOOGLE['outputencoding']
            True
            >>> gConGr.http_proxy == ALISS_DEFAULT_GOOGLE['http_proxy']
            True

        Seams ok :)

        """

    meta_type = METATYPE_ALISSGROUP
    def __init__(self, id, name, filter, pattern):
        #identifier
        self.id =               id
        self.name =             name

        #object data
        self.filter =           filter
        self.pattern =          pattern
        self.last_updated =     ''
        self.search_type =      'exact'

        #google related data
        self.start =            ALISS_DEFAULT_GOOGLE['start']
        self.maxResults =       ALISS_DEFAULT_GOOGLE['maxResults']
        self.g_filter =         ALISS_DEFAULT_GOOGLE['filter']
        self.restrict =         ALISS_DEFAULT_GOOGLE['restrict']
        self.safeSearch =       ALISS_DEFAULT_GOOGLE['safeSearch']
        self.language =         ALISS_DEFAULT_GOOGLE['language']
        self.inputencoding =    ALISS_DEFAULT_GOOGLE['inputencoding']
        self.outputencoding =   ALISS_DEFAULT_GOOGLE['outputencoding']
        self.http_proxy =       ALISS_DEFAULT_GOOGLE['http_proxy']

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(ContentGroup)

class ContentGroupManager:
    """ """

    def __init__(self):
        self.__groups_collection = PersistentMapping()

    def __add_group_item(self, id, name, filter, pattern):
        #create a new item
        item = ContentGroup(id, name, filter, pattern)
        self.__groups_collection[id] = item

    def __update_group_item(self, id, name, filter, pattern):
        #modify an item
        item = self.__groups_collection.get(id)
        if item is not None:
            item.name =     name
            item.filter =   filter
            item.pattern =  pattern
            self.__groups_collection[id] = item

    def __delete_group_item(self, id):
        #delete an item
        try:    del(self.__groups_collection[id])
        except: pass


    #################
    #   BASIC API   #
    #################
    def get_groups_collection(self):
        #return the groups collection
        return self.__groups_collection

    def get_groups_ids(self):
        #get the groups ids
        return self.__groups_collection.keys()

    def get_groups_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__groups_collection.values(), 'name')

    def get_group_item(self, id):
        #get an item
        try:    return self.__groups_collection[id]
        except: return None

    def get_group_item_data(self, id):
        #get an item data
        item = self.get_group_item(id)
        if item is not None: 
            return ['update',
                    item.id,
                    item.name,
                    item.filter,
                    item.pattern,
                    item.start,
                    item.maxResults,
                    item.g_filter,
                    item.restrict,
                    item.safeSearch,
                    item.language,
                    item.inputencoding,
                    item.outputencoding,
                    item.http_proxy,
                    item.search_type]
        else:
            return ['add', '', '', '', '']

    def add_group_item(self, id, name, filter, pattern):
        #create a new item
        self.__add_group_item(id, name, filter, pattern)

    def update_group_item(self, id, name, filter, pattern):
        #modify an item
        self.__update_group_item(id, name, filter, pattern)

    def update_google_props(self, id, start, maxResults, filter, restrict, safeSearch,
                            language, inputencoding, outputencoding, http_proxy):
        #update the Google search properties
        msg = 0
        item = self.__groups_collection.get(id)
        if item is not None:
            #set data
            try:
                #check if integer values
                start =            int(start)
                maxResults =       int(maxResults)
                filter =           int(filter)
                safeSearch =       int(safeSearch)
            except:
                msg = 1
            if not msg:
                #set data
                item.start =            start
                item.maxResults =       maxResults
                item.g_filter =         filter
                item.safeSearch =       safeSearch
                item.restrict =         restrict
                item.language =         language
                item.inputencoding =    inputencoding
                item.outputencoding =   outputencoding
                item.http_proxy =       http_proxy
                self.__groups_collection[id] = item
        return msg

    def update_search_type(self, id, search_type):
        #update the Google search type
        item = self.__groups_collection.get(id)
        item.search_type = search_type
        self.__groups_collection[id] = item

    def delete_group_item(self, ids):
        #delete 1 or more items
        map(self.__delete_group_item, ids)

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(ContentGroupManager)