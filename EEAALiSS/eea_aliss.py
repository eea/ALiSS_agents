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
import Products
from Globals                                    import InitializeClass
from OFS.Folder                                 import Folder
from AccessControl                              import ClassSecurityInfo
from OFS.SimpleItem                             import SimpleItem
from AccessControl.Permissions                  import view_management_screens, view
from Products.PageTemplates.PageTemplateFile    import PageTemplateFile

#Product imports

from Products.EEAALiSS                          import utils
from Products.EEAALiSS.constants                import *
from Products.EEAALiSS.eea_content_group        import ContentGroupManager
from Products.EEAALiSS.eea_google_license       import GoogleLicenseManager
try:
    from Products.ALiSS.aliss                   import ALiSS
except:
    pass


manage_addEEAALiSS_html = PageTemplateFile('zpt/eea_add', globals())

def manage_addEEAALiSS(self, id, title, description, REQUEST=None):
    """ add a new EEAALiSS object """
    id = utils.utCleanupId(id)
    if not id: id = PREFIX_EEAALISS + utils.utGenRandomId(6)
    ob = EEAALiSS(id, title, description)
    self._setObject(id, ob)
    ob = self._getOb(id)
    ob.loadDefaultData()

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAALiSS(SimpleItem):
    """ EEAALiSS object """

    meta_type = METATYPE_EEAALISS
    icon = 'misc_/EEAALiSS/EEAALiSS.gif'

    manage_options = (
        (
            {'label':'Properties', 'action':'eea_properties_html'},
            {'label':'Licenses', 'action':'eea_licenses_html'},
            {'label':'Content Groups', 'action':'eea_content_groups_html'},
            {'label':'ALiSS', 'action':'eea_aliss_html'},
        )
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        #constructor
        self.id =               id
        self.title =            title
        self.description =      description
        self.licenses =         GoogleLicenseManager()
        self.content_groups =   ContentGroupManager()

    security.declarePrivate('loadDefaultData')
    def loadDefaultData(self):
        #loads default Google Licences
        for license in ALISS_GOOGLE_KEYS:
            self.licenses.add_license_item(license['id'], license['license'])
            
        #loads default Content Groups
        for group in DEFAULT_CONTENT_GROUPS:
            self.content_groups.add_group_item(group['id'],
                                               group['name'],
                                               group['filter'],
                                               group['pattern'])


    #########################
    #   BASIC PROPERTIES    #
    #########################
    security.declareProtected(view_management_screens, 'manageProperties')
    def manageProperties(self, title='', description='', REQUEST=None):
        """ manage basic properties """
        self.title =        title
        self.description =  description
        self._p_changed =   1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_properties_html?save=ok')


    ######################
    #   LICENCE RELATED  #
    ######################
    security.declareProtected(view_management_screens, 'manage_add_license_item')
    def manage_add_license_item(self, id=None, license='', REQUEST=None):
        """ manage Google Licences """
        if not id: id = utils.utGenRandomId()
        self.licenses.add_license_item(id, license)
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_update_license_item')
    def manage_update_license_item(self, id='', license='', REQUEST=None):
        """ update Google Licences """
        self.licenses.update_license_item(id, license)
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_delete_licenses')
    def manage_delete_licenses(self, ids=[], REQUEST=None):
        """ delete Google Licences """
        self.licenses.delete_license_item(utils.utConvertToList(ids))
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'getLicenseItemData')
    def getLicenseItemData(self):
        """ return a license by id """
        return self.licenses.get_license_item_data( self.REQUEST.get('id', None))

    security.declareProtected(view_management_screens, 'getGroupsList')
    def getLicensesList(self):
        """ return all licenses """
        return self.licenses.get_licenses_list()


    #############################
    #   CONTENT GROUP RELATED   #
    #############################
    def getDefaultGoogle(self, name):
        """ return the default google values """
        return ALISS_DEFAULT_GOOGLE[name]

    security.declareProtected(view_management_screens, 'manage_add_group_item')
    def manage_add_group_item(self, id=None, name='', filter='', pattern='', REQUEST=None):
        """ add a content group item """
        if len(name)==0: name = filter
        if not id: id = utils.utGenRandomId()

        self.content_groups.add_group_item(id, name, filter, pattern)
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_content_groups_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_delete_groups')
    def manage_delete_groups(self, ids=[], REQUEST=None):
        """ delete a content group item """
        self.content_groups.delete_group_item(utils.utConvertToList(ids))
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_content_groups_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_update_group_item')
    def manage_update_group_item(self, id='', name='', filter='', pattern='', REQUEST=None):
        """ update a content group item """
        self.content_groups.update_group_item(id, name, filter, pattern)
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_content_groups_html?id=%s&save=ok' % id)

    security.declareProtected(view_management_screens, 'loadGoogleDefault')
    def loadGoogleDefault(self, id='', REQUEST=None):
        """ load default Google parameters """
        content_group =                  self.content_groups.get_group_item(id)
        content_group.start =            self.getDefaultGoogle('start')
        content_group.maxResults =       self.getDefaultGoogle('maxResults')
        content_group.g_filter =         self.getDefaultGoogle('filter')
        content_group.restrict =         self.getDefaultGoogle('restrict')
        content_group.safeSearch =       self.getDefaultGoogle('safeSearch')
        content_group.language =         self.getDefaultGoogle('language')
        content_group.inputencoding =    self.getDefaultGoogle('inputencoding')
        content_group.outputencoding =   self.getDefaultGoogle('outputencoding')
        content_group.http_proxy =       self.getDefaultGoogle('http_proxy')
        self._p_changed =                1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_content_groups_html?id=%s&menu_index=1&save=ok' % id)

    security.declareProtected(view_management_screens, 'manageGoogleSearchProperties')
    def manageGoogleSearchProperties(self, id='', start='', maxResults='', filter='', restrict='', safeSearch='',
                                     language='', inputencoding='', outputencoding='', http_proxy=None, REQUEST=None):
        """ manage Google indexing properties """
        err = 0
        #get the current content group
        content_group = self.content_groups.get_group_item(id)

        #set data
        try:
            #check if integer values
            start =            int(start)
            maxResults =       int(maxResults)
            filter =           int(filter)
            safeSearch =       int(safeSearch)
        except:
            err = 1
        if not err:
            #set data
            content_group.start =            start
            content_group.maxResults =       maxResults
            content_group.g_filter =         filter
            content_group.safeSearch =       safeSearch
            content_group.restrict =         restrict
            content_group.language =         language
            content_group.inputencoding =    inputencoding
            content_group.outputencoding =   outputencoding
            content_group.http_proxy =       http_proxy
            self._p_changed =                1
        if REQUEST and not err: REQUEST.RESPONSE.redirect('eea_content_groups_html?id=%s&menu_index=1&save=ok' % id)
        elif REQUEST and err: REQUEST.RESPONSE.redirect('eea_content_groups_html?id=%s&menu_index=1&save=err' % id)

    security.declareProtected(view_management_screens, 'manageSearchType')
    def manageSearchType(self, id, search_type, REQUEST=None):
        """ set the type of search: 'exact', 'medium', 'weak' or 'all' """
        content_group =              self.content_groups.get_group_item(id)
        content_group.search_type =  search_type
        self._p_changed =            1
        if REQUEST: REQUEST.RESPONSE.redirect('eea_content_groups_html?id=%s&menu_index=2&save=ok' % id)

    security.declareProtected(view_management_screens, 'getGroupItemData')
    def getGroupItemData(self):
        """ return a content group by its id """
        return self.content_groups.get_group_item_data( self.REQUEST.get('id', None))

    security.declareProtected(view_management_screens, 'getGroupsList')
    def getGroupsList(self):
        """ return all content groups """
        return self.content_groups.get_groups_list()


    #########################
    #   ALiSS RELATED       #
    #########################
    security.declareProtected(view_management_screens, 'getGBoxDefault')
    def getGBoxDefault(self):
        """ return the default Google box server URL """
        return ALISS_GOOBLE_BOX

    security.declareProtected(view_management_screens, 'manageAliss')
    def manageAliss(self,id='', title='', description='',gbox='', REQUEST=None):
        """ manage ALiSS creation """
        id = utils.utCleanupId(id)
        if not id: id = PREFIX_ALISS + utils.utGenRandomId(6)

        #create the ALiSS instance
        try:
            ob = ALiSS(id, title, description)
            self.aq_parent._setObject(id, ob)
            ob = self.aq_parent._getOb(id)
            ob.gbox = gbox
            ob.manage_addAlissCatalog()
            ob.catalog = getattr(ob, ALISS_CATALOG_ID)

            #add the default content groups
            for group in self.getGroupsList():
                ob.content_group_manager.add_group_item(group.id,
                                                        group.name,
                                                        group.filter,
                                                        group.pattern)
            #add the deafault licenses
            for license in self.getLicensesList():
                ob.getLicenseManager().add_license_item(license.id,
                                                        license.license)
            msg = 'ok'
        except:
            msg = 'err'
        if REQUEST: REQUEST.RESPONSE.redirect('eea_aliss_html?save=%s' % msg)


    #################
    #   ZMI PAGES   #
    #################
    security.declareProtected(view_management_screens, 'eea_properties_html')
    eea_properties_html =       PageTemplateFile('zpt/eea_properties', globals())

    security.declareProtected(view_management_screens, 'eea_licenses_html')
    eea_licenses_html =         PageTemplateFile('zpt/eea_licenses', globals())

    security.declareProtected(view_management_screens, 'eea_content_groups_html')
    eea_content_groups_html =   PageTemplateFile('zpt/eea_content_groups', globals())

    security.declareProtected(view_management_screens, 'eea_aliss_html')
    eea_aliss_html =            PageTemplateFile('zpt/eea_aliss', globals())

    security.declareProtected(view_management_screens, 'manage_options_style')
    manage_options_style =      PageTemplateFile('zpt/eea_zmi_style', globals())

InitializeClass(EEAALiSS)
