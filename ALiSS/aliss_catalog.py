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
import urllib, time

#Zope imports
from Globals                                 import InitializeClass
from AccessControl                           import ClassSecurityInfo
from Products.ZCatalog.ZCatalog              import ZCatalog
from Products.ZCTextIndex.ZCTextIndex        import manage_addLexicon
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl.Permissions               import view_management_screens

#Product imports
from Products.ALiSS.constants   import *
from Products.ALiSS             import utils


def manage_addAlissCatalog(self, REQUEST=None):
    """ add a new AlissCatalog object """
    ob = AlissCatalog()
    self._setObject(ALISS_CATALOG_ID, ob)
    ob = self._getOb(ALISS_CATALOG_ID)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class AlissCatalog(ZCatalog):
    """ AlissCatalog object """

    meta_type = METATYPE_ALISSCATALOG
    icon = 'misc_/ALiSS/ALiSSCatalog.gif'

    manage_options = (
        {'label': 'Contents',           # TAB: Contents
         'action': 'manage_main',
         'help': ('OFSP','ObjectManager_Contents.stx')},
        {'label': 'Catalog',            # TAB: Cataloged Objects
         'action': 'manage_catalogView',
         'help':('ZCatalog','ZCatalog_Cataloged-Objects.stx')},
        {'label': 'Properties',         # TAB: Properties
         'action': 'manage_propertiesForm',
         'help': ('OFSP','Properties.stx')},
        {'label': 'Indexes',            # TAB: Indexes
         'action': 'manage_catalogIndexes',
         'help': ('ZCatalog','ZCatalog_Indexes.stx')},
        {'label': 'Metadata',           # TAB: Metadata
         'action': 'manage_catalogSchema',
         'help':('ZCatalog','ZCatalog_MetaData-Table.stx')},
        {'label': 'Find Objects',       # TAB: Find Objects
         'action': 'manage_catalogFind',
         'help':('ZCatalog','ZCatalog_Find-Items-to-ZCatalog.stx')},
        {'label': 'Find ALiSS Objects',       # TAB: Find ALiSS Objects
         'action': 'manage_catalogAlissFind',
         'help':('ALiSS','ALiSSCatalog_Find-ALiSS-Items-to-ZCatalog.stx')},
        {'label': 'Advanced',           # TAB: Advanced
         'action': 'manage_catalogAdvanced',
         'help':('ZCatalog','ZCatalog_Advanced.stx')},
        {'label': 'Undo',               # TAB: Undo
         'action': 'manage_UndoForm',
         'help': ('OFSP','Undo.stx')},
        {'label': 'Security',           # TAB: Security
         'action': 'manage_access',
         'help': ('OFSP','Security.stx')},
        {'label': 'Ownership',          # TAB: Ownership
         'action': 'manage_owner',
         'help': ('OFSP','Ownership.stx'),}
        )

    security = ClassSecurityInfo()

    def __init__(self, id=ALISS_CATALOG_ID, title=ALISS_CATALOG_TITLE):
        ZCatalog.__init__(self, id, title)
        self.__generateDefaultIndexes()

    def __addLexicons(self):
        #Adds the default lexicons
        elements = []
        wordSplitter = MyData()
        wordSplitter.group = 'Word Splitter'
        wordSplitter.name = 'HTML aware splitter'

        caseNormalizer = MyData()
        caseNormalizer.group = 'Case Normalizer'
        caseNormalizer.name = 'Case Normalizer'

        stopWords = MyData()
        stopWords.group = 'Stop Words'
        stopWords.name = ALISS_LEXICON_REMOVE_SW_AND_SINGLE

        elements.append(wordSplitter)
        elements.append(caseNormalizer)
        elements.append(stopWords)
        id = 'Lexicon'
        title = 'Default Lexicon'

        manage_addLexicon(self, id, title, elements)

        elements = []
        wordSplitter = MyData()
        wordSplitter.group = 'Word Splitter'
        wordSplitter.name = 'HTML aware splitter'

        caseNormalizer = MyData()
        caseNormalizer.group = 'Case Normalizer'
        caseNormalizer.name = 'Case Normalizer'

        stopWords = MyData()
        stopWords.group = 'Stop Words'
        stopWords.name = " Don't remove stop words"

        elements.append(wordSplitter)
        elements.append(caseNormalizer)
        elements.append(stopWords)
        id = 'LexiconID'
        title = 'Default Lexicon for IDs'

        manage_addLexicon(self, id, title, elements)

        elements = []
        wordSplitter = MyData()
        wordSplitter.group = 'Word Splitter'
        wordSplitter.name = 'Unicode Whitespace splitter'

        caseNormalizer = MyData()
        caseNormalizer.group = 'Case Normalizer'
        caseNormalizer.name = 'Unicode Case Normalizer'

        stopWords = MyData()
        stopWords.group = 'Stop Words'
        stopWords.name = " Don't remove stop words"

        elements.append(wordSplitter)
        elements.append(caseNormalizer)
        elements.append(stopWords)
        id = 'LexiconUnicode'
        title = 'Unicode Lexicon'

        manage_addLexicon(self, id, title, elements)


    def __generateDefaultIndexes(self):
        available_indexes = self.indexes()
        available_metadata = self.schema()

        self.__addLexicons()

        for index in self.getDefaultIndexes():
            if not (index in available_indexes):
                if self.getIndexById(index)[0] == 'ZCTextIndex':
                    p_extras =              MyData()
                    p_extras.doc_attr =     self.getIndexById(index)[1]
                    p_extras.index_type =   self.getIndexById(index)[2]
                    p_extras.lexicon_id =   self.getIndexById(index)[3]
                else:
                    p_extras = None
                self.addIndex(index, self.getIndexById(index)[0], p_extras)
            if not (index in available_metadata):
                self.addColumn(index)

    def __createObjecttransIndex(self, index):
        p_extras =              MyData()
        p_extras.doc_attr =     index
        p_extras.index_type =   'Okapi BM25 Rank'
        p_extras.lexicon_id =   'LexiconUnicode'
        self.addIndex(index, 'ZCTextIndex', p_extras)
        if not (index in self.schema()):
            self.addColumn(index)

    def __createObjectnameIndex(self, index):
        self.addIndex(index, 'FieldIndex')

    def searchCatalog(self, filters, zope_obj=None):
        #get catalog
        results = []

        #create filter
        criteria = {}
        for item in filters:
            criteria[item[0]] = item[1]

        #get brains list
        results.extend(self(criteria))

        #get ojects list (1 for zope objects, 2 for google page objects and None for element objects)
        #TODO:remove the parameter solution zope_obj and work with meta_type instead.
        if zope_obj == 1:    results = map(self.getobject, map(getattr, results, ('data_record_id_',)*len(results)))
        elif zope_obj == 2:  results = map(self.getgooglepages,map(getattr,results,('data_record_id_',)*len(results)))

        #eliminate duplicates
        return utils.utElimintateDuplicates(results)


    ###################
    #   REINDEX API   #
    ###################
    def getCatalogedMetas(self):
        return METATYPE_CATALOGED

    def resolve_path(self, path):
        """
        Attempt to resolve a url into an object in the Zope
        namespace. The url may be absolute or a catalog path
        style url. If no object is found, None is returned.
        No exceptions are raised.
        """
        if path:
            if path[0] == '/':
                #zope objects case
                try:    return self.unrestrictedTraverse(path)
                except: pass
            else:
                #aliss (python) objects case
                try:    return self.get_aliss_object(path)
                except: pass
        #case of no path
        pass

    def get_aliss_object(self, path):
        #return a cataloged aliss object based on the catalog path
        my_path_list = path.split('/')
        obj_level = len(my_path_list)

        #get the ALiSSCenter object
        gloss_center = self.get_center_by_UID(my_path_list[0])

        #get the element object
        gloss_elem = gloss_center.element_manager.get_element_item(my_path_list[1])
        if obj_level == 2:
            return gloss_elem

        #get the google item object
        google_item = None
        for item in gloss_elem.get_google_objs():
            if my_path_list[2] == item.id: google_item = item
        if obj_level == 3:
            return google_item

        #get the google page object
        google_page = None
        for item in google_item.get_page_collection_objs():
            if my_path_list[3] == item.id: google_page = item
        if obj_level == 4:
            return google_page

        #case of no object found
        return None

    def manage_catalogFoundAlissItems(self, obj_metatypes, URL1, REQUEST=None):
        """ Find object according to search criteria and Catalog them """
        metas = []
        elapse = time.time()
        c_elapse = time.clock()

        if 'all' in obj_metatypes:
            metas.extend(self.getCatalogedMetas())
        else:
            metas.extend(obj_metatypes)

        if self.testMetas(metas, METATYPE_ALISSCENTER):
            #ALiSS Centers
            l_centers = self.get_all_centers()
            for center in l_centers:
                if METATYPE_ALISSCENTER in metas:
                    self.CatalogObject(center)

                #ALiSS Elements
                if self.testMetas(metas, METATYPE_ALISSELEMENT):
                    for elem in center.element_manager.get_elements_list():
                        if METATYPE_ALISSELEMENT in metas:
                            self.CatalogObject(elem)

                        #ALiSS Google Items
                        if self.testMetas(metas, METATYPE_ALISSGOOGLE):
                            for g_item in elem.get_google_objs():
                                if METATYPE_ALISSGOOGLE in metas:
                                    self.CatalogObject(g_item)

                                #ALiSS Google Page
                                if self.testMetas(metas, METATYPE_ALISSPAGE):
                                    for g_page in g_item.get_page_collection_objs():
                                        if METATYPE_ALISSPAGE in metas:
                                            self.CatalogObject(g_page)

        elapse = time.time() - elapse
        c_elapse = time.clock() - c_elapse

        if REQUEST: REQUEST.RESPONSE.redirect(
            URL1 +
            '/manage_catalogView?manage_tabs_message=' +
            urllib.quote('Catalog Updated\n'
                         'Total time: %s\n'
                         'Total CPU time: %s'
                         % (`elapse`, `c_elapse`))
            )

    def testMetas(self, obj_metatypes, meta):
        #test meta_types
        return {
          METATYPE_ALISSCENTER  : len(obj_metatypes),
          METATYPE_ALISSELEMENT : len(utils.utRemoveFromList(obj_metatypes, [METATYPE_ALISSCENTER])),
          METATYPE_ALISSGOOGLE  : len(utils.utRemoveFromList(obj_metatypes, [METATYPE_ALISSCENTER, METATYPE_ALISSELEMENT])),
          METATYPE_ALISSPAGE    : METATYPE_ALISSPAGE in obj_metatypes
        }[meta]


    #################
    #   BASIC API   #
    #################
    def getDefaultIndexes(self):
        return ALISS_INDEXES.keys()

    def getIndexById(self, id):
        return ALISS_INDEXES[id]

    def getLexicon(self):
        """ return the default Lexicon object """
        #return self._getOb('Lexicon')
        return self._getOb('LexiconUnicode')

    def BuildCatalogPath(self, p_item):
        """ build a path for items to be added in catalog """
        #create a path for a GlossElement object
        if p_item.meta_type == METATYPE_ALISSELEMENT:
            return '%s/%s' % (p_item.center_parent, p_item.id)
        #create a path for a Google object
        elif p_item.meta_type == METATYPE_ALISSGOOGLE:
            return '%s/%s/%s' % (p_item.center_parent, p_item.elem_parent, p_item.id)
        #create a path for a GooglePage object
        elif p_item.meta_type == METATYPE_ALISSPAGE:
            return '%s/%s/%s/%s' % (p_item.center_parent, p_item.elem_parent, p_item.google_parent, p_item.id)
        #create a path for a ALiSSCenter object
        elif p_item.meta_type == METATYPE_ALISSCENTER:
            return '/'.join(p_item.getPhysicalPath())

    def CatalogObject(self, p_ob):
        """ catalog objects """
        self.catalog_object(p_ob, self.BuildCatalogPath(p_ob))

    def UncatalogObject(self, p_ob):
        """ uncatalog objects """
        if utils.utIsListType(p_ob):  map(lambda x, y: x.uncatalog_object(x.BuildCatalogPath(y)), (self,)*len(p_ob), p_ob)
        else:                        self.uncatalog_object(self.BuildCatalogPath(p_ob))

    def RecatalogObject(self, p_ob):
        """ recatalog Issue objects """
        self.UncatalogObject(p_ob)
        self.CatalogObject(p_ob)

    def getgooglepages(self, rid, REQUEST=None):
        #return a cataloged google item object given a 'data_record_id_'
        my_path_list = self.getpath(rid).split('/')

        #get the ALiSSCenter object
        gloss_center = self.aq_parent.getCenterByUID(my_path_list[0])

        #get the element object
        gloss_elem = gloss_center.element_manager.get_element_item(my_path_list[1])

        #get the google item object
        for item in gloss_elem.get_google_objs():
            if my_path_list[2] == item.id: google_item = item

        #get the google page object
        for item in google_item.get_page_collection_objs():
            if my_path_list[3] == item.id: return item

    def checkCatalogIndexes(self, trans):
        """ check if catalog contain all required language indexes """
        for lang in trans.keys():
            index_id = 'objecttrans_%s' % lang
            if not index_id in self.indexes():
                self.__createObjecttransIndex(index_id)
            index_id = 'objectname_%s' % lang
            if not index_id in self.indexes():
                self.__createObjectnameIndex(index_id)


    ################
    #   UPDATES    #
    ################

    security.declareProtected(view_management_screens, 'updateCatalogMultilingual')
    def updateCatalogMultilingual(self):
        """ """
        #cleanup
        old_indexes = ['translations_suggest', 'id_suggest', 'getName', 'name_suggest']
        remove_indexes = []
        remove_schemas = []
        for index in old_indexes:
            if index in self.indexes():
                remove_indexes.append(index)
            if index in self.schema():
                remove_schemas.append(index)
        self.manage_delIndex(ids=remove_indexes)
        self.manage_delColumn(names=remove_schemas)

        #update
        info = []
        for lang in self.getLanguagesIndexed()[0]:
            objectname_index = 'objectname_%s' % lang.lower()
            objecttrans_index = 'objecttrans_%s' % lang.lower()
            if not objecttrans_index in self.indexes():
                self.__createObjecttransIndex(objecttrans_index)
                info.append(objecttrans_index)
            if not objectname_index in self.indexes():
                self.__createObjectnameIndex(objectname_index)
                info.append(objectname_index)
        self.manage_reindexIndex(ids=info)
        return info


    #################
    #   ZMI PAGES   #
    #################
    manage_catalogAlissFind = PageTemplateFile('zpt/ALiSSCatalog/catalogAlissFind', globals())

InitializeClass(AlissCatalog)

class MyData: pass
