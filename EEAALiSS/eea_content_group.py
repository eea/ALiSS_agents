# -*- coding: utf-8 -*-
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
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Alexandru Ghica - Finsiel Romania
# Antonio De Marinis - EEA
# Sasha Vinčić - Systemvaruhuset

#Python imports

#Zope imports
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo

#Product imports
from Products.EEAALiSS.constants    import *
from Products.EEAALiSS              import utils

class ContentGroup:
    """ """

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
        self.__groups_collection = {}

    #################
    #   BASIC API   #
    #################
    def get_groups_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__groups_collection.values(), 'name', 0)

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
        item = ContentGroup(id, name, filter, pattern)
        self.__groups_collection[id] = item

    def update_group_item(self, id, name, filter, pattern):
        #modify an item
        try:    item = self.__groups_collection[id]
        except: pass
        else:
            item.name =     name
            item.filter =   filter
            item.pattern =  pattern

    def delete_group_item(self, ids):
        #delete 1 or more items
        for id in ids:
            try:    del(self.__groups_collection[id])
            except: pass


    #################
    #   GETTERS     #
    #################
    def getDefaultGroups(self):
        #returns default groups list
        return DEFAULT_CONTENT_GROUPS

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(ContentGroupManager)