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
import Products
from OFS.Folder                                 import Folder
from Globals                                    import InitializeClass
from Globals                                    import DTMLFile
from AccessControl                              import ClassSecurityInfo
from AccessControl.Permissions                  import view_management_screens, view
from Products.PageTemplates.PageTemplateFile    import PageTemplateFile

#Product imports
from Products.ALiSS                                   import utils
from Products.ALiSS.constants                         import *
from Products.ALiSS.aliss_center                      import manage_addAlissCenter, manage_addAlissCenter_html
from Products.ALiSS.aliss_agent                       import manage_addAlissAgent, manage_addAlissAgent_html
from Products.ALiSS.aliss_catalog                     import manage_addAlissCatalog
from Products.ALiSS.managers.content_group_manager    import ContentGroupManager
from Products.ALiSS.managers.google_license_manager   import GoogleLicenseManager


manage_addALiSS_html = PageTemplateFile('zpt/ALiSS/aliss_add', globals())

def manage_addALiSS(self, id, title, description, REQUEST=None):
    """ add a new ALiSS object """
    id = utils.utCleanupId(id)
    if not id: id = PREFIX_ALISS + utils.utGenRandomId(6)
    ob = ALiSS(id, title, description)
    self._setObject(id, ob)
    ob = self._getOb(id)

    #creates the catalog
    ob.manage_addAlissCatalog()
    ob.catalog = getattr(ob, ALISS_CATALOG_ID)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class ALiSS(Folder):
    """ ALiSS object """

    meta_type = METATYPE_ALISS
    icon = 'misc_/ALiSS/ALiSS.gif'

    manage_options = (
        (
            Folder.manage_options[0],
            {'label':'Properties'       , 'action':'manage_properties_html'},
            {'label':'View'             , 'action':'index_html'},
            {'label':'Google Licenses'  , 'action':'manage_google_licenses_html'},
            {'label':'Google Update'    , 'action':'manage_google_update_html'},
            {'label':'Content Groups'   , 'action':'manage_content_groups_html'},
            {'label':'ALiSS Info'       , 'action':'manage_info_html'},
            {'label':'Alphabets'        , 'action':'manage_alphabets_html'},
            Folder.manage_options[3],
            Folder.manage_options[4],
            Folder.manage_options[5],
        )
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        #constructor
        self.id =                       id
        self.title =                    title
        self.description =              description
        self.gbox =                     ''
        self.content_group_manager =    ContentGroupManager()
        self.glicense_manager =         GoogleLicenseManager()

    def all_meta_types(self):
        """ What can you put inside me? """
        other_meta_types = Folder.all_meta_types(self)
        agents = [ metatype for metatype in other_meta_types
                            if metatype['name'] == METATYPE_ALISSAGENT ]
        local_meta_types = [{'name': METATYPE_ALISSCENTER, 'action': 'manage_addAlissCenter_html', 'product': ALISS_PRODUCT_NAME},
                            {'name': METATYPE_ALISSAGENT,  'action': 'manage_addAlissAgent_html',  'product': ALISS_PRODUCT_NAME},]
        local_meta_types.extend(agents)
        f = lambda x: x['name'] in ('Script (Python)', 'Image', 'Page Template', 'RAM Cache Manager', 'Site Error Log')
        for x in filter(f, Products.meta_types):
            local_meta_types.append(x)
        return local_meta_types

    #AlissCenter related
    security.declareProtected(view_management_screens, 'manage_addAlissCenter_html')
    manage_addAlissCenter_html = manage_addAlissCenter_html

    security.declareProtected(view_management_screens, 'manage_addAlissCenter')
    manage_addAlissCenter = manage_addAlissCenter

    #AlissAgent related
    security.declareProtected(view_management_screens, 'manage_addAlissAgent_html')
    manage_addAlissAgent_html = manage_addAlissAgent_html

    security.declareProtected(view_management_screens, 'manage_addAlissAgent')
    manage_addAlissAgent = manage_addAlissAgent

    #Ajax/XML-RPC related
    security.declareProtected('View','ajax_response_terms_related')
    ajax_response_terms_related = DTMLFile("dtml/ALiSS/ajax_response_terms_related", globals())

    security.declareProtected('View','ajax_response_page_related')
    ajax_response_page_related = DTMLFile("dtml/ALiSS/ajax_response_page_related", globals())

    security.declareProtected('View','ajax_response_terms_suggestion')
    ajax_response_terms_suggestion = DTMLFile("dtml/ALiSS/ajax_response_terms_suggestion", globals())

    security.declareProtected('View','ajax_response_text_related')
    ajax_response_text_related = DTMLFile("dtml/ALiSS/ajax_response_text_related", globals())


    #################
    #   GETTERS     #
    #################
    def getAlissRoot(self):  return self

    def getLanguagesIndexed(self):
        """ """
        res = {'en':0}
        langs = []
        props = []

        for index_name in self.catalog.indexes():
            if index_name.startswith('objecttrans_'):
                props.append(index_name)

        for center in self.getAllCenters():
            for brain in center.getAllElements():
                for prop_name in props:
                    if len(getattr(brain, prop_name, '')) > 0:
                        lang = prop_name.split('_')[1].lower()
                        res[lang] = res.get(lang, 0) + 1
        langs = res.keys()
        langs.sort()

        return (langs, res)

    def getAllAgents(self):
        """ return all Server Agents """
        return utils.utSortObjsListByAttr(self.objectValues(METATYPE_ALISSAGENT),'title')

    def getAllowedAgents(self):
        """ """
        return [agent for agent in self.getAllAgents() if agent.allow_in_navigation]

    def getDefaultGoogleList(self):
        return ALISS_DEFAULT_GOOGLE.keys()

    def getValueById(self, id):
        return ALISS_DEFAULT_GOOGLE[id]

    def getGroupsUsed(self):
        #return all content groups used in AlissCenters
        result={}
        for center in self.getAllCenters():
            for group_id in self.content_group_manager.get_groups_ids():
                result[group_id] = self.content_group_manager.get_group_item(group_id).name
        return result

    def getDefaultGoogle(self, name):
        #return the default google values
        return ALISS_DEFAULT_GOOGLE[name]

    def getElementsByNames(self, names, suggest=False, lang='en'):
        """ Search term across all centers in this aliss instance.
        Return all cataloged elements with names=names available
        or if suggest=True suggest which terms matches the names """
        names = utils.utToUnicode(names)
        query =  {'meta_type': {'query':METATYPE_ALISSELEMENT, 'operator':'and '},}
        if suggest:
            index_name = 'objecttrans_%s' % lang.lower()
            query[index_name] = names
        else:
            index_name = 'objectname_%s' % lang.lower()
            query[index_name] = {'query':names.lower(), 'operator':'and '}
        cat_res = self.catalog(query)
        if len(cat_res) > 0:
            return self.getTrans(cat_res[0], lang)
        return None

    def testGroupsIfUsed(self, group_id):
        #test if a content group is used
        for center in self.getAllCenters():
            if center.testElementList():
                elem_id = center.element_manager.get_elements_ids()[0]
                elem_ob = center.element_manager.get_element_item(elem_id)
                if group_id in elem_ob.get_google_ids():
                    return 1
        return 0

#TODO: deprecated implementation
#    security.declareProtected('View','filterStopWords')
#    def filterStopWords(self, query):
#        """ return list of words/terms filtered from stop words """
#        #TODO: try to replace split with the ZCTextIndex Lexicon API e.g. 'parseTerms'
#        #return self.catalog.getLexicon().parseTerms(query)
#
#        result = []
#        # terms should not have parenthesis inside. replace '(' and ')' otherwise error occures.
#        query=query.replace('(','')
#        query=query.replace(')','')
#        
#        query_terms = query.split()
#        for term in query_terms:
#            if term != '' and not self.catalog.checkDuplicate(term):
#                result.append(term)
#        return result

    security.declareProtected('View','filterStopWords')
    def filterStopWords(self, query):
        """ return list of words/terms filtered from stop words, by 
        using the catalog default lexicon. """
        #return list of words/terms filtered from stop words
        return self.catalog.getLexicon().parseTerms(query)

    #####################
    #  CATALOG RELATED  #
    #####################
    manage_addAlissCatalog = manage_addAlissCatalog

    def getCatalog(self):
        """ return the catalog object """
        return self._getOb(ALISS_CATALOG_ID, None)

    def getAllCenters(self):
        """ return all ALiSS Centers """
        return self.catalog.searchCatalog([('meta_type', METATYPE_ALISSCENTER)], 1)

    def getDefaultIndexes(self):
        """ return the default indexes """
        return self.catalog.getDefaultIndexes()

    def getCenterByUID(self, center_uid):
        """ return an ALiSS Center by its UID """
        res = self.catalog.searchCatalog([('center_uid', center_uid)], 1)
        if res: return res[0]
        return None

    def getIndexById(self, id):
        """ return an index by its ID """
        return self.catalog.getIndexById(id)

    def testGBoxContent(self):
        """ test if Google box was used in Google updates """
        query = [('meta_type',METATYPE_ALISSPAGE),
                 ('g_server', 'box_srv')]
        if self.catalog.searchCatalog(query): return 1
        return 0

    #non catalog related getters
    def get_center_by_UID(self, center_uid):
        #return an ALiSS Centers by its UID
        for item in self.objectValues(METATYPE_ALISSCENTER):
            if item.center_uid == center_uid: return item
        return None

    def get_all_centers(self):
        #return all ALiSS Centers
        return self.objectValues(METATYPE_ALISSCENTER)

    def getTrans(self, brain, lang):
        #return translation
        try:    return eval('brain.objectname_%s' % lang)
        except: return ''


    ######################
    #   BASIC PROPERTIES #
    ######################
    security.declareProtected(view_management_screens, 'manageProperties')
    def manageProperties(self, title='', description='', gbox='', REQUEST=None):
        """ manage basic properties """
        self.title =        title
        self.description =  description
        self.gbox =         gbox
        self._p_changed =   1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')


    ######################
    #   LICENCE RELATED  #
    ######################
    security.declareProtected(view_management_screens, 'manage_add_license_item')
    def manage_add_license_item(self, id=None, license='', REQUEST=None):
        """ manage Google Licences """
        glicense_manager = self.getLicenseManager()
        if not id: id = utils.utGenRandomId()
        glicense_manager.add_license_item(id, license)
        self.setCurrentLicense(license)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_google_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_update_license_item')
    def manage_update_license_item(self, id='', license='', REQUEST=None):
        """ update Google Licences """
        glicense_manager = self.getLicenseManager()
        glicense_manager.update_license_item(id, license)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_google_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_delete_licenses')
    def manage_delete_licenses(self, ids=[], REQUEST=None):
        """ delete Google Licences """
        glicense_manager = self.getLicenseManager()
        glicense_manager.delete_license_item(utils.utConvertToList(ids))
        if REQUEST: REQUEST.RESPONSE.redirect('manage_google_licenses_html?save=ok')

    security.declareProtected(view_management_screens, 'getLicenseItemData')
    def getLicenseItemData(self):
        """ return a license based on its ID """
        glicense_manager = self.getLicenseManager()
        return glicense_manager.get_license_item_data( self.REQUEST.get('id', None))

    security.declareProtected(view_management_screens, 'getLicenseManager')
    def getLicenseManager(self):
        """ return the license manager """
        return self.glicense_manager

    security.declareProtected(view_management_screens, 'getLicensesList')
    def getLicensesList(self):
        """ return all licenses """
        return self.glicense_manager.get_licenses_list()

    security.declareProtected(view_management_screens, 'setCurrentLicense')
    def setCurrentLicense(self, license):
        """ set the current license """
        license_manager = self.getLicenseManager()
        license_manager.setCurrentLicense(license)
        self.glicense_manager = license_manager
        self._p_changed = 1


    #############################
    #   CONTENT GROUP RELATED   #
    #############################
    security.declareProtected(view_management_screens, 'manage_add_group_item')
    def manage_add_group_item(self, id=None, name='', filter='', pattern='', REQUEST=None):
        """ add a content group item """
        if len(name)==0: name = filter
        if not id: id = utils.utGenRandomId()

        self.content_group_manager.add_group_item(id, name, filter, pattern)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_delete_groups')
    def manage_delete_groups(self, ids=[], REQUEST=None):
        """ delete a content group item """
        err = 0
        for group_id in utils.utConvertToList(ids):
            if self.testGroupIsUsed(group_id):
                err = 1
                break
        if err:
            if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?save=err')
        else:
            self.content_group_manager.delete_group_item(utils.utConvertToList(ids))
            if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?save=ok')

    security.declareProtected(view_management_screens, 'manage_update_group_item')
    def manage_update_group_item(self, id='', name='', filter='', pattern='', REQUEST=None):
        """ update a content group item """
        self.content_group_manager.update_group_item(id, name, filter, pattern)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?id=%s&save=ok' % id)

    def testGroupIsUsed(self, group_id):
        #test if a content group is used in any ALiSSCenter
        for center in self.getAllCenters():
            if center.testElementList():
                elem_id = center.element_manager.get_elements_ids()[0]
                elem_ob = center.element_manager.get_element_item(elem_id)
                if group_id in elem_ob.get_google_ids():  return 1

        #test if a content group is associated to any ALiSS Agent Server
        for agent in self.getAllAgents():
            if group_id in agent.content_groups:   return 1

        return 0

    security.declareProtected(view_management_screens, 'loadGoogleDefault')
    def loadGoogleDefault(self, id='', REQUEST=None):
        """ load default Google parameters """
        msg = self.content_group_manager.update_google_props(id,
                                                             self.getDefaultGoogle('start'),
                                                             self.getDefaultGoogle('maxResults'),
                                                             self.getDefaultGoogle('filter'),
                                                             self.getDefaultGoogle('restrict'),
                                                             self.getDefaultGoogle('safeSearch'),
                                                             self.getDefaultGoogle('language'),
                                                             self.getDefaultGoogle('inputencoding'),
                                                             self.getDefaultGoogle('outputencoding'),
                                                             self.getDefaultGoogle('http_proxy'))
        if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?id=%s&menu_index=1&save=ok' % id)

    security.declareProtected(view_management_screens, 'manageGoogleSearchProperties')
    def manageGoogleSearchProperties(self, id='', start='', maxResults='', filter='', restrict='', safeSearch='',
                                     language='', inputencoding='', outputencoding='', http_proxy=None, REQUEST=None):
        """ manage Google indexing properties """
        msg = self.content_group_manager.update_google_props(id, start, maxResults, filter, restrict, safeSearch,
                                                             language, inputencoding, outputencoding, http_proxy)
        if REQUEST and not msg: REQUEST.RESPONSE.redirect('manage_content_groups_html?id=%s&menu_index=1&save=ok' % id)
        elif REQUEST and msg: REQUEST.RESPONSE.redirect('manage_content_groups_html?id=%s&menu_index=1&save=err' % id)

    security.declareProtected(view_management_screens, 'manageSearchType')
    def manageSearchType(self, id, search_type, REQUEST=None):
        """ set the type of search: 'exact', 'medium', 'weak' or 'all' """
        self.content_group_manager.update_search_type(id, search_type)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_content_groups_html?id=%s&menu_index=2&save=ok' % id)

    security.declareProtected(view_management_screens, 'getGroupItemData')
    def getGroupItemData(self, id=None):
        if not id:
            id = self.REQUEST.get('id', None)
        return self.content_group_manager.get_group_item_data(id)

    security.declareProtected(view_management_screens, 'getGroupsList')
    def getGroupsList(self):
        return self.content_group_manager.get_groups_list()


    #########################
    #   GOOGLE UPDATE       #
    #########################
    security.declareProtected(view_management_screens, 'googleUpdate')
    def googleUpdate(self, centers_list, groups=[], servers=[], update_type='update', REQUEST=None):
        """ do Google indexing on selected content groups """
        if not len(servers) or not len(groups):
            if REQUEST: REQUEST.RESPONSE.redirect('manage_google_update_html?done=select')
        else:
            glicense_manager = self.getLicenseManager()
            license = glicense_manager.getCurrentLicense()
            for center_uid in utils.utSplitToList(centers_list, ','):
                #do Goole update
                center = self.getCenterByUID(center_uid)

                getGroup = self.content_group_manager.get_group_item
                my_groups = [ getGroup(group_id) for group_id in groups ]

                center.setLicense(license)
                err_count = center.googleUpdate(update_type, my_groups, servers)
                center.setLicense('')

                #set messages
                if err_count:
                    l_msg = 'done=err&err_count=%s' % err_count
                else:
                    l_msg = 'done=ok'

            if REQUEST: REQUEST.RESPONSE.redirect('manage_google_update_html?%s' % l_msg)

    security.declareProtected(view_management_screens, 'googleResume')
    def googleResume(self, centers_list, groups=[], servers=[], REQUEST=None):
        """ do Google resume on selected content groups """
        return self.googleUpdate(centers_list, groups, servers, 'resume', REQUEST)

    security.declareProtected(view_management_screens, 'googleCleanup')
    def googleCleanup(self, centers_list, groups=[], servers=[], REQUEST=None):
        """ delete a groups content """
        if not len(servers) or not len(groups):
            if REQUEST: REQUEST.RESPONSE.redirect('manage_google_update_html?done=select')
        else:
            for center_uid in utils.utSplitToList(centers_list, ','):
                center = self.getCenterByUID(center_uid)
                for id in groups:
                    if center.testGroupContent(id):
                        for elem in center.element_manager.get_elements_list():
                            google_item = elem.get_google_collection_item(id)

                            if len(servers) == 2:
                                #uncatalog google pages
                                self.catalog.UncatalogObject(google_item.get_page_collection_objs())
                                #uncatalog google items
                                self.catalog.UncatalogObject([google_item])
                                #delete google items
                                elem.delete_google_item(id)
                            else:
                                pages_by_srv = google_item.get_page_collection_by_srv(servers[0])
                                #uncatalog google pages
                                self.catalog.UncatalogObject(pages_by_srv)
                                #delete google pages
                                for page in pages_by_srv:
                                    google_item.delete_google_page(page.id)
                                if not google_item.get_page_collection_objs():
                                    #uncatalog google items
                                    self.catalog.UncatalogObject([google_item])
                                    #delete google items
                                    elem.delete_google_item(id)
                    center._p_changed = 1

            self._p_changed = 1
            if REQUEST: REQUEST.RESPONSE.redirect('manage_google_update_html?done=cleanup')


    #################
    #   ZMI PAGES   #
    #################
    security.declareProtected(view_management_screens, 'manage_properties_html')
    manage_properties_html =        PageTemplateFile('zpt/ALiSS/aliss_edit', globals())

    security.declareProtected(view_management_screens, 'manage_google_licenses_html')
    manage_google_licenses_html =   PageTemplateFile('zpt/ALiSS/aliss_google_licenses', globals())

    security.declareProtected(view_management_screens, 'manage_options_style')
    manage_options_style =          PageTemplateFile('zpt/ALiSS/aliss_zmi_style', globals())

    security.declareProtected(view_management_screens, 'manage_content_groups_html')
    manage_content_groups_html =    PageTemplateFile('zpt/ALiSS/aliss_content_groups', globals())

    security.declareProtected(view_management_screens, 'manage_google_update_html')
    manage_google_update_html =     PageTemplateFile('zpt/ALiSS/aliss_google_update', globals())

    security.declareProtected(view_management_screens, 'manage_info_html')
    manage_info_html =              PageTemplateFile('zpt/ALiSS/aliss_info', globals())

    security.declareProtected(view_management_screens, 'manage_alphabets_html')
    manage_alphabets_html =              PageTemplateFile('zpt/ALiSS/aliss_alphabets', globals())

    #####################
    #   PUBLIC PAGES    #
    #####################
    security.declarePublic('index_html')
    index_html =    PageTemplateFile('zpt/ALiSS/aliss_index', globals())

    security.declarePublic('results')
    results =    PageTemplateFile('zpt/ALiSS/aliss_results', globals())

    #google ajax search
    security.declarePublic('google_cs_ajax_js')
    google_cs_ajax_js = DTMLFile('dtml/ALiSS/google_cs_ajax_js', globals())

    #aliss ajax clients files
    security.declarePublic('aliss_css')
    aliss_css = DTMLFile('client/dtml/aliss_css', globals())

    security.declarePublic('aliss_js')
    aliss_js = DTMLFile('client/dtml/aliss_js', globals())

    security.declarePublic('prototype_js')
    prototype_js = DTMLFile('client/dtml/prototype_js', globals())

    security.declarePublic('rico_js')
    rico_js = DTMLFile('client/dtml/rico_js', globals())

    security.declarePublic('aliss_flash_js')
    aliss_flash_js = DTMLFile('client/dtml/aliss_flash_js', globals())

InitializeClass(ALiSS)
