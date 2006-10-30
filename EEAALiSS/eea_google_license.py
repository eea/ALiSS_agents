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
from Products.EEAALiSS.constants import *
from Products.EEAALiSS           import utils


class LicenseItem:
    """ """

    meta_type = METATYPE_ALISSLICENSE
    def __init__(self, id, license):
        self.id =   id
        self.license = license

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(LicenseItem)


class GoogleLicenseManager:
    """ """

    def __init__(self):
        self.__licenses_collection = {}


    #################
    #   BASIC API   #
    #################
    def add_license_item(self, id, license):
        #create a new item
        item = LicenseItem(id, license)
        self.__licenses_collection[id] = item

    def update_license_item(self, id, license):
        #modify an item
        try:    item = self.__licenses_collection[id]
        except: pass
        else:   item.license = license

    def delete_license_item(self, ids):
        #delete 1 or more items
        for id in ids:
            try:    del(self.__licenses_collection[id])
            except: pass


    #################
    #   GETTERS     #
    #################
    def get_licenses_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__licenses_collection.values(), 'license', 0)

    def get_license_item(self, id):
        #get an item
        try:    return self.__licenses_collection[id]
        except: return None

    def get_license_item_data(self, id):
        #get an item data
        item = self.get_license_item(id)
        if item is not None: 
            return ['update', item.id, item.license]
        else:
            return ['add', '', '']

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(GoogleLicenseManager)
