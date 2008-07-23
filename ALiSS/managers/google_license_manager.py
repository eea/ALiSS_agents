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
from Globals                  import InitializeClass
from AccessControl            import ClassSecurityInfo
from persistent.mapping       import PersistentMapping

#Product imports
from Products.ALiSS.constants import *
from Products.ALiSS           import utils


class LicenseItem:
    """ A License item store the data of a Google license.

            >>> from Products.ALiSS.managers.google_license_manager import LicenseItem
            >>> gLicense = LicenseItem( id=         'licId',
            ...                         license=    'licData')

        We have now created a license item and stored it in gLicense. Let's check if the values are ok.

            >>> gLicense.id
            'licId'
            >>> gLicense.license
            'licData' 

        Seams ok :)

        """

    meta_type = METATYPE_ALISSLICENSE
    def __init__(self, id, license):
        self.id =       id
        self.license =  license

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(LicenseItem)

class GoogleLicenseManager:
    """ """

    def __init__(self):
        self.__licenses_collection = PersistentMapping()
        self.__current_license = ''

    def __add_license_item(self, id, license):
        #create a new item
        item = LicenseItem(id, license)
        self.__licenses_collection[id] = item
        self.setCurrentLicense(license)

    def __update_license_item(self, id, license):
        #modify an item
        item = self.__licenses_collection.get(id)
        if item is not None:
            item.license = license
            self.__licenses_collection[id] = item

    def __delete_license_item(self, id):
        #delete an item
        try:    del(self.__licenses_collection[id])
        except: pass

    #################
    #   BASIC API   #
    #################
    def add_license_item(self, id, license):
        #create a new item
        self.__add_license_item(id, license)

    def update_license_item(self, id, license):
        #modify an item
        self.__update_license_item(id, license)

    def delete_license_item(self, ids):
        #delete 1 or more items
        map(self.__delete_license_item, ids)


    #################
    #   GETTERS     #
    #################
    def get_license_key(self, license_key):
        #get the license to be used
        licenses_list = self.get_licenses_list()
        if not license_key:
            return (self.getCurrentLicense(), 'ok')
        else:
            i = 0
            for k in licenses_list:
                i += 1
                if license_key == k.license:
                    break
            if i and len(licenses_list) > i:
                my_license = licenses_list[i].license
                self.setCurrentLicense(my_license)
                return (my_license, 'ok')
            else: return ('', 'end')

    def get_licenses_collection(self):
        #get the collection
        return self.__licenses_collection

    def get_licenses_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__licenses_collection.values(), 'license')

    def get_licenses_lists(self):
        #return the list with all items splited in two lists
        l = utils.utSortObjsListByAttr(self.__licenses_collection.values(), 'license')
        sp = len(l)/2
        return (l[:sp], l[sp:])

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


    #############################
    #  CURRENT LICENCE RELATED  #
    #############################
    def getCurrentLicense(self):
        #return current license
        return self.__current_license

    def setCurrentLicense(self, value):
        #set the current license
        self.__current_license = value
