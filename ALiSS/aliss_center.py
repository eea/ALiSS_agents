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
from Globals                                    import InitializeClass
from OFS.Cache                                  import Cacheable
from OFS.Folder                                 import Folder
from AccessControl                              import ClassSecurityInfo
from AccessControl.Permissions                  import view_management_screens, view
from Products.PageTemplates.PageTemplateFile    import PageTemplateFile

#Product imports
from Products.ALiSS.managers.timeoutsocket            import setDefaultSocketTimeout
from Products.ALiSS.constants                         import *
from Products.ALiSS                                   import utils
from Products.ALiSS.managers.skos_manager             import SkosImport
from Products.ALiSS.managers.element_manager          import ElementManager
from Products.ALiSS.managers.google_manager           import GoogleManager
from Products.ALiSS.alphabet_charts                   import unicode_character_map

manage_addAlissCenter_html = PageTemplateFile('zpt/ALiSSCenter/aliss_center_add', globals())

def manage_addAlissCenter(self, id, title, description, gloss_url, gloss_skos, REQUEST=None):
    """ add a new AlissCenter object """
    id = utils.utCleanupId(id)
    if not id: id = PREFIX_ALISSCENTER + utils.utGenRandomId(6)
    center_uid = utils.utGenRandomId(10)
    ob = ALiSSCenter(id, title, description, center_uid, gloss_url, gloss_skos)
    ob.catalog = self.catalog
    ob.element_manager.catalog = self.catalog
    self._setObject(id, ob)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class ALiSSCenter(Folder,
                  Cacheable,
                  GoogleManager):
    """ ALiSSCenter object """

    meta_type = METATYPE_ALISSCENTER
    icon = 'misc_/ALiSS/ALiSSCenter.gif'

    manage_options = (
        (
            {'label':'Properties'       , 'action':'manage_properties_html'},
            {'label':'Update content'   , 'action':'manage_update_html'},
            {'label':'Elements list'    , 'action':'manage_elements_html'},
            {'label':'Disabled/Errors'  , 'action':'manage_errors_html'},
            {'label':'Top pages list'   , 'action':'manage_top_pages_html'},
            Cacheable.manage_options[0],
            Folder.manage_options[0],
            Folder.manage_options[3],
            Folder.manage_options[4],
            Folder.manage_options[5],
        )
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description, center_uid, gloss_url, gloss_skos):
        #constructor
        self.id =               id
        self.title =            title
        self.description =      description
        self.center_uid =       center_uid
        self.gloss_url =        gloss_url
        self.gloss_skos =       gloss_skos
        self.last_updated =     ''
        self.gloss_http_proxy = ''
        self.element_manager = ElementManager()
        GoogleManager.__init__(self)

    def getLastUpdate(self): return utils.utShowDateTime(self.last_updated)

    #########################
    #   MANAGEMENT ACTIONS  #
    #########################
    def manage_afterAdd(self, item, container):
        """ This method is called, whenever _setObject in ObjectManager gets called. """
        Folder.inheritedAttribute('manage_afterAdd')(self, item, container)
        catalog = self.catalog
        catalog.CatalogObject(self)
        element_manager = self.element_manager
        if element_manager.testElementList():
            for id in element_manager.get_elements_ids():
                elem = element_manager.get_elements_collection()[id]

                #catalog google items
                google_list = [elem.get_google_collection()[google_id] for google_id in elem.get_google_ids()]
                for google_item in google_list:
                    catalog.CatalogObject(google_item)

                #catalog element items
                catalog.CatalogObject(element_manager.get_element_item(id))

    def manage_beforeDelete(self, item, container):
        """ This method is called, when the object is deleted. """
        catalog = self.catalog
        Folder.inheritedAttribute('manage_beforeDelete')(self, item, container)
        element_manager = self.element_manager
        for id in element_manager.get_elements_ids():
            elem = element_manager.get_elements_collection()[id]

            for google_id in elem.get_google_ids():
                google_item = elem.get_google_collection()[google_id]

                #uncatalog google pages
                catalog.UncatalogObject(google_item.get_page_collection_objs())
                #uncatalog google items
                catalog.UncatalogObject([google_item])

            #uncatalog element items
            catalog.UncatalogObject(elem)
        catalog.UncatalogObject(self)


    #########################
    #   PROPERTIES ACTIONS  #
    #########################
    security.declareProtected(view_management_screens, 'manageProperties')
    def manageProperties(self, title='', description='', gloss_url='', gloss_skos='', timeout='', gloss_http_proxy='', REQUEST=None):
        """ manage basic properties """
        self.title =            title
        self.description =      description
        self.gloss_url =        gloss_url
        self.gloss_skos =       gloss_skos
        self.timeout =          timeout
        self.gloss_http_proxy = gloss_http_proxy
        self.catalog.RecatalogObject(self)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')


    #########################
    #   SKOS UPDATE ACTIONS #
    #########################
    security.declareProtected(view_management_screens, 'manageBasicUpdate')
    def manageBasicUpdate(self, REQUEST=None):
        """ manage update elements from SKOS """
        #get/update data from RDF files
        skos_elements_list = SkosImport(self.gloss_skos)

        #set RDF's data
        if skos_elements_list == 'err' or len(skos_elements_list.items()) == 0:
            response_msg = 'err'
        else:
            element_manager = self.element_manager
            #if ALiSSCenter contain no data all elements are added
            if not element_manager.testElementList():
                for elem in skos_elements_list.keys():
                    element_manager.add_element_item( skos_elements_list[elem].id,
                                                      skos_elements_list[elem].name,
                                                      skos_elements_list[elem].definition,
                                                      skos_elements_list[elem].translations,
                                                      skos_elements_list[elem].url,
                                                      self.center_uid)

            #if ALiSSCenter contain some data
            else:
                #update elements data
                for data in skos_elements_list.keys():
                    #elements are updated if already exist
                    if data in element_manager.get_elements_ids():
                        element_manager.update_element_basic( skos_elements_list[data].id,
                                                              skos_elements_list[data].name,
                                                              skos_elements_list[data].definition,
                                                              skos_elements_list[data].translations,
                                                              skos_elements_list[data].url)
                    #elements are added if doesnt exist
                    else:
                        element_manager.add_element_item( skos_elements_list[data].id,
                                                          skos_elements_list[data].name,
                                                          skos_elements_list[data].definition,
                                                          skos_elements_list[data].translations,
                                                          skos_elements_list[data].url,
                                                          self.center_uid)

                #elements witch are no longer found on the new RDF are deleted
                if not len(skos_elements_list) == element_manager.testElementList():
                    ids = []
                    ids_append = ids.append
                    for id in element_manager.get_elements_ids():
                        if not id in skos_elements_list.keys():
                            ids_append(id)
                    element_manager.delete_element_item(ids)

            self.last_updated = utils.getCurrentDate()
            self._p_changed = 1
            response_msg = 'ok'

        if REQUEST: REQUEST.RESPONSE.redirect('manage_update_html?update=%s' % response_msg)
        else: return response_msg

    security.declareProtected(view_management_screens, 'manageCleanUp')
    def manageCleanUp(self, REQUEST=None):
        """ manage delete all elements """
        self.element_manager.cleanUpContent()
        if REQUEST: REQUEST.RESPONSE.redirect('manage_update_html?delete=ok')

    security.declareProtected(view_management_screens, 'manage_element_list')
    def manage_element_list(self, elem_id, content_id=None, page_id=None, servers=[], REQUEST=None):
        """ manage elements list actions """
        catalog = self.catalog
        action_msg = 'done='

        #set general data
        elem_ob = self.element_manager.get_element_item(elem_id)
        if content_id: content_ob = elem_ob.get_google_collection_item(content_id)
        content_disable = REQUEST.get('content_disable')

        #enable all content groups for a specific element
        if REQUEST.get('enable_all'):
            google_list = elem_ob.get_google_objs()
            map(lambda x, y: x.set_google_enable(1, y.group_id), (elem_ob,)*len(google_list), google_list)
            map(lambda x, y: x.RecatalogObject(y),(catalog,)*len(google_list), google_list)
            map(lambda x, y: x.delGoogleDisabled(y.group_id),(elem_ob,)*len(google_list), google_list)
            action_msg = 'done=enable all'
            self._p_changed = 1

        #disable all content groups for a specific element
        elif REQUEST.get('disable_all'):
            google_list = elem_ob.get_google_objs()
            map(lambda x, y: x.set_google_enable(0, y.group_id), (elem_ob,)*len(google_list), google_list)
            map(lambda x, y: x.RecatalogObject(y),(catalog,)*len(google_list), google_list)
            map(lambda x, y: x.addGoogleDisabled(y.group_id),(elem_ob,)*len(google_list), google_list)
            action_msg = 'done=disable all'
            self._p_changed = 1

        #update from a Google server a selected content group on a specific element
        elif REQUEST.get('content_update'):
            aliss = self.aq_parent
            content_group = aliss.content_group_manager.get_group_item(content_id)
            if not len(aliss.getLicenseManager().get_licenses_collection()):
                action_msg = 'done=license'
            elif not len(servers):
                action_msg = 'done=select'
            else:
                glicense_manager = aliss.getLicenseManager()
                license = glicense_manager.getCurrentLicense()
                self.setLicense(license)
                action_msg = self.googleUpdate('update', [content_group], servers, elem_id)
                if not action_msg: action_msg = 'done=ok'
                self.setLicense('')

        #enable/disable a specific content group for a given element
        elif content_disable:
            if content_disable == 'enabled': 
                elem_ob.set_google_enable(1, content_ob.group_id)
                elem_ob.delGoogleDisabled(content_id)
                action_msg = 'done=enabled'
            else:
                elem_ob.set_google_enable(0, content_ob.group_id)
                elem_ob.addGoogleDisabled(content_id)
                action_msg = 'done=disabled'
            catalog.RecatalogObject(content_ob)
            self._p_changed = 1

        if REQUEST and page_id: REQUEST.RESPONSE.redirect('manage_errors_html?elem_id=%s&%s&page=%s#%s' % (elem_id, action_msg, page_id, elem_id))
        else:                   REQUEST.RESPONSE.redirect('manage_elements_html?elem_id=%s&%s#%s' % (elem_id, action_msg, elem_id))


    #########################
    #   CATALOG RELATED     #
    #########################
    #TODO: make sure that we ask for meta_type=METATYPE_ALISSELEMENT when we do getElements from Catalog, instead of using zope_obj=1 or 2 parameter.

    def getElements(self, element_ids):
        query = [('meta_type',METATYPE_ALISSELEMENT),
                 ('center_parent', self.center_uid),
                 ('id', element_ids)]
        return self.catalog.searchCatalog(query)

    def getAllElements(self):
        query = [('meta_type',METATYPE_ALISSELEMENT),
                 ('center_parent', self.center_uid)]
        return self.catalog.searchCatalog(query)

    def getElementsWithErrors(self, group_id):
        """ return elements with update errors on a specific content group """
        element_ids = []
        query = [('meta_type', METATYPE_ALISSGOOGLE),
                 ('group_id', group_id),
                 ('google_error', 1),
                 ('center_parent', self.center_uid)]
        for google_item in self.catalog.searchCatalog(query):
            element_ids.append(google_item.elem_parent)
        return self.getElements(element_ids)

    def getAllElementsWithErrors(self):
        """ return all elements with update errors """
        elements = []
        query = [('meta_type', METATYPE_ALISSGOOGLE),
                 ('google_error', 1),
                 ('center_parent', self.center_uid)]
        for google_item in self.catalog.searchCatalog(query):
            elements.append(self.element_manager.get_element_item(google_item.elem_parent))
        return elements

    def getAllElementsDisabled(self):
        """ return all disabled elements """
        elements = []
        query = [('meta_type', METATYPE_ALISSGOOGLE),
                 ('google_enable', 0),
                 ('center_parent', self.center_uid)]
        for google_item in self.catalog.searchCatalog(query):
            elements.append(self.element_manager.get_element_item(google_item.elem_parent))
        return elements

    def getElementsForPage(self, pageURL):
        """ return the elements for a given page.
        Note: only elements with exact match level will be returned. """
        elem_ids=[]
        google_pages = self.catalog({'page_url':     {'query':pageURL, 'operator':'and '},
                                     'center_parent':{'query':self.center_uid, 'operator':'and '},
                                     'meta_type':    {'query':METATYPE_ALISSPAGE, 'operator':'and '}})
        google_item_ids = [ google_page.google_parent for google_page in google_pages ]

        #ask catalog if there are google items with "exact" macth level.
        google_parent_groups=self.catalog({'id':         {'query':google_item_ids},
                                           'match_level':{'query':'exact', 'operator':'and '},
                                           'meta_type':  {'query':METATYPE_ALISSGOOGLE, 'operator':'and '}})
        for google_parent_group in google_parent_groups:
            #if this page was collected via a google exact search then included in the list
            if google_parent_group.elem_parent not in elem_ids:
               elem_ids.append(google_parent_group.elem_parent)

        #create result
        res = []
        add_res = res.append
        for elem in self.getElements(elem_ids):
            add_res(elem)
        return res

    def getAllPages(self):
        """ return all ALiSS Pages of a Center """
        return self.catalog.searchCatalog([('meta_type', METATYPE_ALISSPAGE),
                                           ('center_parent', self.center_uid)], 2)

    def getPagesByGroupsAndTerms(self, group_ids, term_ids):
        query = [ ('meta_type',     METATYPE_ALISSPAGE),
                  ('center_parent', self.center_uid),
                  ('gloss_parent',  group_ids),
                  ('elem_parent',   term_ids) ]
        return self.catalog.searchCatalog(query)

    def getElementsByNames(self, names, suggest=False, lang='en'):
        """ return all cataloged elements with names=names part to this center
        or if suggest=True suggest which terms matches the names """
        names = utils.utToUnicode(names)
        query =  {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                  'center_parent': {'query':self.center_uid, 'operator':'and '}}
        if suggest:
            query['objecttrans_%s' % lang.lower()] = names
        else:
            query['objectname_%s' % lang.lower()] = {'query':names.lower(), 'operator':'and '}
        cat_res = self.catalog(query)
        return cat_res

    def getElementsByLetter(self, letter, lang):
        """ """
        query_letter = letter
        id_indexname = 'objecttrans_%s' % lang
        if len(letter) in [1, 2]:
            query = {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                     'center_parent': {'query':self.center_uid, 'operator':'and '},
                     id_indexname:  {'query':'%s*' % query_letter}}
        elif letter == 'num':
            digit_query = ''
            length = len(utils.getDigits())
            index = 0

            for digit in utils.getDigits():
                index += 1
                if index == length:
                    digit_query = '%s%s*' % (digit_query, digit)
                else:
                    digit_query = '%s%s* or ' % (digit_query, digit)

            query = {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                     'center_parent': {'query':self.center_uid, 'operator':'and '},
                     id_indexname:  {'query':digit_query}}
        elif letter == 'all':
            query = {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                     'center_parent': {'query':self.center_uid}}
        elif letter == 'other':
            query = {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                     'center_parent': {'query':self.center_uid}}
            tmp_cat_res = self.catalog(query)
            cat_res = []
            for brain in tmp_cat_res:
                try:
                    trans = self.getTrans(brain, lang)

                    if len(trans) > 0:
                        for dig in utils.getDigits():
                            if trans.startswith(dig):
                                raise
                        for charset in unicode_character_map[lang]:
                            for char in charset:
                                if trans.startswith(char):
                                    raise
                        cat_res.append(trans)
                except:
                    pass
        else:
            query = {'meta_type':     {'query':''}}

        if letter != 'other':
            cat_res = []
            res = self.catalog(query)
            for brain in res:
                cat_res.append(self.getTrans(brain, lang))

        return cat_res


    #############
    #   OTHER   #
    #############
    security.declareProtected(view_management_screens, 'testGroupContent')
    def testGroupContent(self, group_id='', server='all', REQUEST=None):
        """ test if a content group has indexed content """
        if self.testElementList():
            for elem in self.element_manager.get_elements_list():
                google_ob = elem.get_google_collection_item(group_id)

                if server != 'all' and google_ob:
                    page_list = google_ob.get_page_collection_by_srv(server)
                else:
                    page_list = google_ob

                if page_list: return 1
            return 0

    security.declareProtected(view_management_screens, 'testGroupErrors')
    def testGroupErrors(self, group_id='', server='all', REQUEST=None):
        """ test if a content group has elements with errors """
        if self.testElementList():
            for elem in self.element_manager.get_elements_list():
                google_ob = elem.get_google_collection_item(group_id)

                if google_ob:
                    if google_ob.google_error: return 1
            return 0

    def testElementList(self):
        """ A proxy method for page templates. Returns size of element list."""
        return self.element_manager.testElementList()

    def getElementsList(self):
        """ return elements list """
        return self.element_manager.get_elements_list()

    def getTopPagesList(self):
        """ return all indexed URLs with their associated elements """
        urls_list = []
        results = []

        #create a list of unique indexed URLs
        for my_page in self.getAllPages():
            if my_page.page_url not in urls_list: urls_list.append(my_page.page_url)

        #associates the elements to their URLs
        for my_url in urls_list:
            results.append((my_url, self.getElementsForPage(my_url)))

        return results

    def getNoDisableElements(self):
        """ return the disabled elements number """
        return len(self.getAllElementsDisabled())

    def getNoElementsWithErrors(self):
        """ return the error elements number """
        return len(self.getAllElementsWithErrors())

    def googleUpdate(self, type, content_groups, servers, element_id=None):
        """ google update """
        #set general data
        element_manager = self.element_manager
        catalog = self.catalog
        setDefaultSocketTimeout(self.timeout)
        err_count = 0

        #set elemnts to be used on update
        if element_id:  elem_list_org = element_manager.get_element_item(element_id)
        else:           elem_list_org = self.getAllElements()

        #do the google update
        for gserver in servers:
            for content_group in content_groups:
                content_group.last_updated = utils.getCurrentDate()
                group_id = content_group.id

                if type == 'update':
                    elem_list = utils.utConvertToList(elem_list_org)
                else:
                    #resume list of elements with update errors
                    elem_list = self.getElementsWithErrors(group_id)

                for elem in elem_list:
                    if not element_id:
                        elem = element_manager.get_element_item(elem.id)

                    #handle disabled content groups
                    if elem.isGroupDisabled(group_id):
                        #handle the non existing content group case
                        if not elem.get_google_collection_item(group_id):
                            #add a empty content group
                            elem.add_google_item(utils.utGenRandomId(), elem.id, self.center_uid, group_id, 'exact')
                            new_google_item = elem.get_google_collection_item(group_id)
                            elem.set_google_enable(0, new_google_item.group_id)
                            catalog.CatalogObject(new_google_item)

                    #do Google search
                    else:
                        #return the Google search results and match type
                        (results, google_match_type) = self._google_search( elem.name,
                                                                            content_group.filter,
                                                                            gserver,

                                                                            #doGoogleSearch parameters
                                                                            content_group.start,
                                                                            content_group.maxResults,
                                                                            content_group.g_filter,
                                                                            content_group.restrict,
                                                                            content_group.safeSearch,
                                                                            content_group.language,
                                                                            content_group.inputencoding,
                                                                            content_group.outputencoding,
                                                                            content_group.http_proxy,
                                                                            content_group.search_type,
                                                                            content_group.pattern)

                        #if Google query has errors keep the old data and mark the google object with error
                        if results[2] == 'err':
                            err_count += 1
                            google_item = elem.get_google_collection_item(group_id)

                            #test if an old google object exist
                            if google_item:
                                #mark the error on google object
                                elem.mark_google_error(google_item.group_id)
                                catalog.RecatalogObject(google_item)
                            else:
                                #add google items and mark the error
                                elem.add_google_item(utils.utGenRandomId(), elem.id, self.center_uid, group_id, google_match_type)
                                google_item = elem.get_google_collection_item(group_id)
                                elem.mark_google_error(google_item.group_id)
                                catalog.CatalogObject(google_item)

                        #if Google query goes well, just delete the old data and add the new one
                        else:
                            #uncatalog old google pages
                            old_google_item = elem.get_google_collection_item(group_id)
                            other_pages = []

                            if old_google_item:
                                #get the pages indexed using the other server type
                                if gserver == 'main_srv': srv_name = 'box_srv'
                                else:                     srv_name = 'main_srv'
                                other_pages = old_google_item.get_page_collection_by_srv(srv_name)

                                catalog.UncatalogObject(old_google_item.get_page_collection_objs())

                                #delete old google items
                                catalog.UncatalogObject([old_google_item])
                            elem.delete_google_item(group_id)

                            #add google items
                            elem.add_google_item(utils.utGenRandomId(), elem.id, self.center_uid, group_id, google_match_type)
                            new_google_item = elem.get_google_collection_item(group_id)
                            catalog.CatalogObject(new_google_item)

                            #add google pages indexed used the other server type
                            for item in other_pages:
                                elem.add_google_page(content_group.id, utils.utGenRandomId(), new_google_item.id, elem.id,
                                                     self.center_uid, item.g_server, item.page_title, item.page_url, item.page_snippet,
                                                     item.page_directoryTitle, item.page_cachedSize, item.page_hostName)

                            #add google pages
                            map(lambda x, y, z, w, m, n:  x.add_google_page(y.id,               #group_id
                                                                            z.utGenRandomId(),  #id
                                                                            n.id,               #google_parent
                                                                            x.id,               #elem_parent
                                                                            m.center_uid,       #center_parent
                                                                            gserver,            #server used (gserver)

                                                                            w['title'],
                                                                            w['URL'],
                                                                            w['snippet'],
                                                                            w['directoryTitle'],
                                                                            w['cachedSize'],
                                                                            w['hostName']),
                                                    (elem,)*len(results[1]),
                                                    (content_group,)*len(results[1]),
                                                    (utils,)*len(results[1]),
                                                    results[1],
                                                    (self,)*len(results[1]),
                                                    (new_google_item,)*len(results[1]))

                            #catalog google pages
                            google_page_list = new_google_item.get_page_collection_objs()
                            map(lambda x,y:  x.CatalogObject(y), (catalog,)*len(google_page_list), google_page_list)

                            #recatalog the new google item
                            catalog.RecatalogObject(new_google_item)
        return err_count

    #########################
    #   XML/RPC RELATED     #
    #########################
    def _get_top_pages(self, terms_names, groups, results_number=None):
        #Return TopPages for a given list terms of this center. Terms is a list of term names/labels.

        results = []
        #get all terms object connected to this center via Catalog.
        res_elems_list=self.getElementsByNames(terms_names)

        #get all content groups labels/names to be used in the group results
        aliss = self.aq_parent
        groups_names = aliss.getGroupsUsed()

        for elem in res_elems_list:
            #not needed res_terms_list contains objects
            #elem_ob = self.element_manager.get_element_item(elem.id)

            elem_ob = self.element_manager.get_element_item(elem.id)
            if elem_ob!=None:
                for group_id in groups: 
                    pages = []
                    match_level='Exact' # default value
                    google_item = elem_ob.get_google_collection_item(group_id)
                    if google_item!=None:
                        match_level=google_item.match_level
                        #get TopPages data
                        for page in google_item.get_page_collection_objs():
                            #TODO: Encoding error - Temporary fixed with try/except. Sometime encoding to utf8 doesn't work. fix encoding. 
                            #Encoding should be dynamic depending on how the enconding was done via google for this page.
                            try:
                                ptitle=page.page_title.encode('utf8')
                            except:
                                ptitle=page.page_title
                            pages.append({'title': ptitle, 'url': page.page_url,'preview_img':page.getPreviewImageUrl(),'snippet':page.page_snippet})

                    #append each result matched
                    results.append({'ElementID':         elem_ob.id,
                                    'ElementName':       elem_ob.name,
                                    'ElementDefinition': elem_ob.definition,
                                    'GroupID':           group_id,
                                    'GroupName':         groups_names[group_id],
                                    'Pages':             pages[:results_number],
                                    'MatchType':         match_level})

        return results

    def _get_terms_for_page(self, pageURL, results_number=None, filteroutTerms=None):
        #return terms for page
        results = []

        #gets all elements containing the pageURL from catalog
        elems_list = self.getElementsForPage(pageURL)

        #creates the results list
        for elem in elems_list:
            results.append({'ElementId':         elem.id,
                            'ElementName':       elem.name,
                            'ElementDefinition': elem.definition,
                            'ElementURL':        elem.url})

        #TODO: to implement filteroutTerms

        #set the number of results to be returned
        if results_number == 'all':  return results
        else:                        return results[:results_number]


    #################
    #   ZMI PAGES   #
    #################
    security.declareProtected(view_management_screens, 'manage_properties_html')
    manage_properties_html =        PageTemplateFile('zpt/ALiSSCenter/aliss_center_edit', globals())

    security.declareProtected(view_management_screens, 'manage_update_html')
    manage_update_html =            PageTemplateFile('zpt/ALiSSCenter/aliss_center_update', globals())

    security.declareProtected(view_management_screens, 'manage_elements_html')
    manage_elements_html =          PageTemplateFile('zpt/ALiSSCenter/aliss_center_elements', globals())

    security.declareProtected(view_management_screens, 'manage_top_pages_html')
    manage_top_pages_html =         PageTemplateFile('zpt/ALiSSCenter/aliss_center_top_pages', globals())

    security.declareProtected(view_management_screens, 'manage_errors_html')
    manage_errors_html =            PageTemplateFile('zpt/ALiSSCenter/aliss_center_errors', globals())

    security.declareProtected(view_management_screens, 'manage_progress_html')
    manage_progress_html =          PageTemplateFile('zpt/ALiSSCenter/aliss_center_progress', globals())

InitializeClass(ALiSSCenter)
