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
from types import StringType
import re
import string

#Zope imports
from Globals                                    import InitializeClass
from Globals                                    import DTMLFile
from OFS.Cache                                  import Cacheable
from OFS.Folder                                 import Folder
from AccessControl                              import ClassSecurityInfo
from AccessControl.Permissions                  import view_management_screens, view
from Products.PageTemplates.PageTemplateFile    import PageTemplateFile

#Product imports
from Products.ALiSS                     import utils
from Products.ALiSS.utils               import batch_utils
from Products.ALiSS.constants           import *
from Products.ALiSS.managers.wikipedia  import WikipediaImages
from Products.ALiSS.alphabet_charts     import unicode_character_map


manage_addAlissAgent_html = PageTemplateFile('zpt/ALiSSAgent/aliss_agent_add', globals())

def manage_addAlissAgent(self, id, title, description, REQUEST=None):
    """ add a new AlissAgent object """
    id = utils.utCleanupId(id)
    if not id: id = PREFIX_ALISSAGENT + utils.utGenRandomId(6)
    ob = ALiSSAgent(id, title, description)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class ALiSSAgent(Folder,
                 Cacheable):
    """ ALiSSAgent object """

    meta_type = METATYPE_ALISSAGENT
    icon = 'misc_/ALiSS/ALiSSAgent.gif'

    manage_options = (
        (   {'label':'Settings'             , 'action':'manage_settings_html'},
            {'label':'Basic properties'     , 'action':'manage_properties_html'},
            {'label':'View'                 , 'action':'index_html'},
            Folder.manage_options[0],
            Cacheable.manage_options[0],
            Folder.manage_options[3],
            Folder.manage_options[4],
            Folder.manage_options[5],
        )
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        #constructor
        self.id =               id
        self.title =            title
        self.description =      description
        self.content_groups =   []
        self.aliss_centers =    []
        self.google_servers =   []
        self.display_type =     1
        self.res_per_page =     10

        #MediaWiki
        self.wiki_service = 0
        self.wiki_images =  1
        self.wiki_height =  200
        self.wiki_width =   200
        self.wiki_host =    'http://en.wikipedia.org' #deprecated

    def __setstate__(self,state):
        """ """
        ALiSSAgent.inheritedAttribute('__setstate__')(self, state)
        if not hasattr(self, 'display_type'):
            #default view is set A-Z
            self.display_type = 1
        if not hasattr(self, 'res_per_page'):
            #default number of results per page
            self.res_per_page = 10

        #mediawiki settings
        if not hasattr(self, 'wiki_service'):
            self.wiki_service = 0
        if not hasattr(self, 'wiki_images'):
            self.wiki_images = 1
        if not hasattr(self, 'wiki_height'):
            self.wiki_height = 200
        if not hasattr(self, 'wiki_width'):
            self.wiki_width = 200
        if not hasattr(self, 'wiki_host'):
            self.wiki_host = 'http://en.wikipedia.org'


    #########################
    #   PROPERTIES ACTIONS  #
    #########################
    security.declareProtected(view_management_screens, 'manageProperties')
    def manageProperties(self, title='', description='', REQUEST=None):
        """ manage basic properties """
        self.title =        title
        self.description =  description
        self._p_changed =   1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')


    #########################
    #   CONTENT GROUPS      #
    #########################
    def manageContentGroups(self, ids=[], REQUEST=None):
        """ manage associated content groups """
        self.content_groups =   ids
        self._p_changed =       1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_settings_html?save=ok')

    def getContentGroups(self):
        """ return associated content groups ids """
        return self.content_groups

    security.declarePublic('getContentGroupsObjs')
    def getContentGroupsObjs(self):
        """ return associated content groups objects """
        cglist=[]
        for group_id in self.getContentGroups():
            group_obj=self.content_group_manager.get_group_item(group_id)
            cglist.append(group_obj)
        return cglist


    #########################
    #   ALiSS CENTERS       #
    #########################
    def manageAlissCenters(self, ids=[], REQUEST=None):
        """ manage associated aliss centers UIDs """
        self.aliss_centers =   ids
        self._p_changed =       1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_settings_html?save=ok')

    def getAlissCentersIds(self):
        """ return associated aliss centers UIDs"""
        return self.aliss_centers

    security.declareProtected(view_management_screens, 'getAlissCenterById')
    def getAlissCenterById(self, center_uid):
        """ return any AlissCenter object based of its UID """
        my_catalog = self.getCatalog()
        return my_catalog.getCenterByUID(center_uid)
        
    security.declareProtected(view_management_screens, 'getAlissCenters')
    def getAlissCenters(self):
        """ return associated AlissCenters objects"""
        my_catalog = self.getCatalog()
        centers=[]
        for cid in self.getAlissCentersIds():
              centers.append(self.getAlissCenterById(cid))
        return centers


    #########################
    #   GOOGLE SERVERS      #
    #########################
    security.declareProtected(view_management_screens, 'manageGoogleServers')
    def manageGoogleServers(self, ids=[], REQUEST=None):
        """ manage associated google servers """
        self.google_servers =   ids
        self._p_changed =       1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_settings_html?save=ok')

    security.declarePublic('getGoogleServers')
    def getGoogleServers(self):
        """ return associated content groups """
        return self.google_servers


    #########################
    #   MEDIAWIKI SETTINGS  #
    #########################
    security.declareProtected(view_management_screens, 'manageMediaWiki')
    def manageMediaWiki(self, wiki_service=0, wiki_images=1, wiki_height=200, wiki_width=200, REQUEST=None):
        """ manage mediawiki settings """
        self.wiki_service = wiki_service
        self.wiki_images =  wiki_images
        self.wiki_height =  wiki_height
        self.wiki_width =   wiki_width
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_settings_html?save=ok')

    def getWikiState(self):  return self.wiki_service
    def getWikiHost(self):   return self.wiki_host
    def getWikiHeight(self): return self.wiki_height
    def getWikiWidth(self):  return self.wiki_width
    def getWikiNumber(self): return self.wiki_images

    security.declarePublic('getWikiImages')
    def getWikiImages(self, query, type='single'):
        """ """
        wiki = WikipediaImages(query)
        return wiki.getImages(self.getWikiHeight(),
                              self.getWikiWidth(),
                              self.getWikiNumber(),
                              self.getWikiHost())

    security.declarePublic('getWikiImages')
    def getWikiFeed(self, query, type='single', REQUEST=None):
        """ """
        wiki = WikipediaImages(query)
        REQUEST.RESPONSE.setHeader('content-type', 'text/xml')
        return wiki.getFeed(self.getWikiHeight(),
                              self.getWikiWidth(),
                              self.getWikiNumber(),
                              self.getWikiHost())

    def getWikiFeddJS(self, query):
        """ """
        return """
  <script type="text/javascript">
    //<![CDATA[
    samples = "%(context)s/getWikiFeed?query=%(query)s&invalidate="+Math.random();
    function load() {

      var options = {
        linkTarget : google.feeds.LINK_TARGET_BLANK,
        fullControlPanel : true,
        transistionTime: 600,
        displayTime: 4000
      };

      new GFslideShow(samples, "slideshow", options);
    }
    google.load("feeds", "1");
    google.setOnLoadCallback(load);
    // ]]>
  </script>""" % {'context': self.absolute_url(), 'query': query}


    #########################
    #   DISPLAY TYPE        #
    #########################
    security.declareProtected(view_management_screens, 'manageDisplayType')
    def manageDisplayType(self, display_type, res_per_page, REQUEST=None):
        """ manage display types """
        if not res_per_page:  res_per_page = 1
        self.display_type =   display_type
        self.res_per_page =   res_per_page
        self._p_changed =     1
        if REQUEST: REQUEST.RESPONSE.redirect('manage_settings_html?save=ok')

    security.declarePublic('getDisplayType')
    def getDisplayType(self):
        """ return the display type """
        return self.display_type

    security.declarePublic('getResPerPage')
    def getResPerPage(self):
        """ return the number of results per page """
        return self.res_per_page


    #########################
    #      AGENT API        #
    #   XML/RPC METHODS     #
    #########################
    security.declarePublic('getTopPagesForTerms')
    def getTopPagesForTerms(self, glossary_elements, results_number=None, REQUEST=None):
        """ Return TopPages of for requested glossary_elements (list of terms' names).
        Each TopPage contains [title, url, snippet]"""
        results = []

        #If glossary_elements is a string then convert to list by splitting via ',' if more then one term supplied ex 'term 1,term 2'.
        if type(glossary_elements) is  StringType:
            glossary_elements=utils.utSplitToList(glossary_elements,',')


        # we use this Agent content groups for all associeated aliss centers
        content_groups=self.getContentGroups()

        #Loop trough all aliss centers for this agent and get top pages for certain content groups
        for aliss_center in self.getAlissCenters():
            results.extend(aliss_center._get_top_pages(glossary_elements, content_groups, results_number))
        return results

    security.declarePublic('getTermsForPage')
    def getTermsForPage(self, pageURL, results_number=None, filteroutTerms=None, REQUEST=None):
        """ Return this center glossary elements (term) related to requested pageURL.
        Each term contains [term label, definition, term_url] """
        results = []

        #Loop trough all aliss centers associated to this agent and get terms for pageURL
        for aliss_center in self.getAlissCenters():
            results.extend(aliss_center._get_terms_for_page(pageURL, results_number, filteroutTerms))

        return results

    security.declarePublic('getRelatedPagesForPage')
    def getRelatedPagesForPage(self, pageURL, relation_types='all', REQUEST=None):
        """ Return related pages for a specific pageURL. 
        It works by getting first all the terms for the pageURL then collecting all the toppages for each term found.
        Each TopPage contains [title, url, snippet] """
        results = []

        #TODO: implement this getRelatedPagesForPage for different relation_types.
        #get terms for pageURL
        terms=self.getTermsForPage(pageURL)
        #get similar pages: pages with terms in common on pageURL
        for term in terms:
            tmp_relation_group={'RelationType':'SimilarPage','RelationLabel':term['ElementName'],'RelationDescription':term['ElementDefinition'],'RelationID':term['ElementId'],'MatchType':'exact','Pages':[]}
            tmp_pages=[]
            for pages_group in self.getTopPagesForTerms(term['ElementName']):
                #include related pages from only exact matches
                if pages_group['MatchType']=='exact':
                    for page in pages_group['Pages']:
                        if page['url']!=pageURL:
                            tmp_pages.append(page)
            if len(tmp_pages)>0:
               tmp_relation_group['Pages']=tmp_pages
               results.append(tmp_relation_group)

        return results

    def getTermSuggestions(self, query, extended=False,size=100):
        """ Returns term suggetions (max by default size=100 terms) in all centers and returns a list of unique terms. """
        results = []

        # filter out stop words and normalize
        words=self.filterStopWords(query)
        query=" ".join(words)
        # if after stopwords removal the query is empty then return empty results
        if utils.isEmptyString(query):
            return []

        if extended:
            for aliss_center in self.getAlissCenters():
                terms = []
                for elem in aliss_center.getElementsByNames(query, True):
                    if elem.name not in terms:
                        terms.append(elem.name)
                        term = {'id':          elem.id,
                                'label':       elem.name,
                                'label_orig':  elem.name,
                                'url':         elem.url,
                                'concept_url': self.absolute_url() + '/concept_html?term=' + utils.utUrlEncode(elem.name),
                                'preview_img': self.absolute_url() + '/misc_/ALiSS/ALiSSConcept.gif'
                               }
                        results.append(term)
        else:
            for aliss_center in self.getAlissCenters():
                terms = [ elem.name for elem in aliss_center.getElementsByNames(query, True) 
                             if elem.name not in results ]
                results.extend(terms)

        return results[:size]

    def getBrainData(self, brain, lang):
        """ """
        #TODO: fix this in order to get data from brain
        elem_path = self.catalog.getpath(brain.data_record_id_)
        elem_ob = self.catalog.get_aliss_object(elem_path)
        elem_trans = elem_ob.getTranslation(lang)
        return (elem_ob, elem_trans)

    def getTermSuggestionsBrains(self, query, extended=False, lang='en', size=100):
        """ Returns term suggetions (max by default size=100 terms) in all centers and returns a list of unique terms. """
        results = []
        orig_query = query

        # filter out stop words and normalize
        words=self.filterStopWords(query)
        query=" ".join(words)
        # if after stopwords removal the query is empty then return empty results
        if utils.isEmptyString(query):
            return []

        if extended:
            terms = []
            for aliss_center in self.getAlissCenters():
                for elem in aliss_center.getElementsByNames(query, True, lang):
                    elem_data = self.getBrainData(elem, lang)
                    elem_ob = elem_data[0]
                    elem_trans = elem_data[1]
                    if elem_trans not in terms and elem_trans.lower()!=orig_query.lower():
                        terms.append(elem_trans)
                        results.append(elem_ob)
        else:
            for aliss_center in self.getAlissCenters():
                for elem in aliss_center.getElementsByNames(query, True, lang):
                    elem_data = self.getBrainData(elem, lang)
                    elem_ob = elem_data[0]
                    elem_trans = elem_data[1]
                    if elem_trans not in results:
                        terms.append(elem_trans)
                results.extend(elem_ob)

        return utils.utSortObjsListByAttr(results[:size], 'name')

    security.declarePublic('getTermsInText')
    def getTermsInText(self,text,search_depth=10):
        """ Returns a dictionary with following keys:
        'foundterms': list of terms found in text.
        'linkedterms': list of terms linked in marked_text.
        'marked_text': html snippet with terms hyperlinked 
        to concept page.
        
        'search_depth' defines how deep the search should go. 
        The smallest the fastest search.
        The highest the most terms are likely to be found. 
        Test according to the application real-time needs. 
        
        If you experience slow performance for this method
        decrease the search_depth."""
        words = self.filterStopWords(text)
        tmptext = text.lower()
        suggestionterms = {}
        resterms = []
        labels = []
        foundterms = []
        linkedterms = []
        restext = ''

        for w in words:
            #skip ParseError when common words are passed.
            try:
                for suggestionTerm in self.getTermSuggestions(w, True, search_depth):
                    suggestionterms[suggestionTerm['label']] = suggestionTerm
            except:
                pass

        #sort the words list based on their length because the compound words had to be replaced first
        resterms.extend(utils.utSortListByLen(suggestionterms.keys()))

        for resterm in resterms:
            findTerm = utils.utToUTF8(suggestionterms[resterm]['label'])
            findTerm = findTerm.translate(string.maketrans('*.,()[]{}|?#<>=!\\', '                 '))
            p = re.compile('\\b' + findTerm + '\\b', re.UNICODE | re.IGNORECASE)
            pos = 0
            while 1:
                m = p.search(text[pos:])
                if m:
                    wStart = pos + m.start()
                    wEnd = pos + m.end()
                    foundterms.append([wStart,wEnd,findTerm])

                    a_start = text[wEnd:].find('<a')
                    a_end = text[wEnd:].find('/a>')

                    wReplace = findTerm
                    origTerm = text[wStart:wEnd]
                    if self.textCompare(origTerm, findTerm):
                        if (a_start > a_end) and (a_end > -1):
                            wReplace = findTerm
                        elif (a_start == -1) and (a_end > -1):
                            wReplace = findTerm
                        else:
                            wReplace = '<a href=\"%s\" title=\"%s\">%s</a>' % \
                                            (suggestionterms[resterm]['concept_url'],
                                             findTerm,
                                             origTerm)
                            text = text[:wStart] + wReplace + text[wEnd:]
                            linkedterms.append([wStart,wEnd,findTerm])
                    pos = wStart + len(wReplace)
                else:
                    break
        return {'foundterms':foundterms, 'linkedterms':linkedterms, 'marked_text':text.strip()}

    security.declarePublic('textCompare')
    def textCompare(self, orig, sugg):
        """ Make sure not to replace a acronym instead of a noun """
        cmp1 = ''
        cmp2 = ''
        for word in orig.split(' '):
            cmp1 += "%s%s" % (word[0].lower(), word[1:])
        for word in sugg.split(' '):
            cmp2 += "%s%s" % (word[0].lower(), word[1:])
        return cmp1 == cmp2

    security.declarePublic('getConceptInfo')
    def getConceptInfo(self, term_name, returnobj='return objects'):
        """This is the xml-rpc call for getConceptDetails. it doesn not return the list of objects.
         It returns an aggregated info about the concept with label 'term_name'. 
        The data contains term name, all definitions with sources(URLs) """
        return self.getConceptDetails(term_name,'en',False)

    security.declarePublic('getConceptDetails')
    def getConceptDetails(self, term_name, lang='en', return_objects=True):
        """ return an aggregated info about the concept with label 'term_name'. 
        The data contains term name, all definitions with sources(URLs) 
        and source terms elements objects list. None object is returned if term not found. 
        'return_objects' is default True and means that the list of python terms object is returned. 
        When calling this method via xml-rpc you need to set this argument to False. """
        terms_list = []
        definitions = {}
        translations = {}

        if not term_name:
           return None

        term_name=term_name.strip()
        results={'term_name':'',
                 'term_url':'',
                 'definitions':definitions,
                 'translations':translations,
                 'terms_list':terms_list}

        #search all terms associated with this ALiSS Agent
        for aliss_center in self.getAlissCenters():
            [terms_list.append(aliss_term) for aliss_term in aliss_center.getElementsByNames(term_name.lower(), lang=lang) if aliss_term]

        #TODO: fix this to use data from brains
        tmp_terms_list = []
        for elem in terms_list:
            elem_data = self.getBrainData(elem, lang)
            elem_ob = elem_data[0]
            tmp_terms_list.append(elem_ob)

        #case of no terms found
        if len(terms_list) == 0:  return None

        #set terms name
        results['term_name'] = tmp_terms_list[0].getTranslation(lang)
        results['term_url'] = utils.utUrlEncode(tmp_terms_list[0].getTranslation(lang))

        l_terms_list = []
        for aliss_term in tmp_terms_list:
            #set terms list
            if utils.isEmptyString(aliss_term.definition):
                definitions[aliss_term.url] = 'Definition not available.'
            else:
                #set definitions and sources(URLs)
                definitions[aliss_term.url] = aliss_term.getDefinition()

            #set translations
            if aliss_term.hasTranslations():
                for langcode in aliss_term.getTranslations().keys():
                    term_trans = aliss_term.getTranslation(langcode)
                    if len(term_trans.strip()) > 0:
                        if translations.has_key(langcode):
                            if term_trans not in translations[langcode]:
                                trans_count = len(translations[langcode])
                                if trans_count == 1:
                                    translations[langcode][0] = '1) %s' % translations[langcode][0]
                                translations[langcode].append('%s) %s' % (trans_count+1, term_trans))
                        else:
                            translations[langcode] = [term_trans]
            translations['en'] = [aliss_term.name]

            l_terms_list.append(aliss_term)

        results['definitions'] = definitions
        results['translations'] = translations
        if return_objects:
            results['terms_list'] = l_terms_list
        else:
            # if we do not want to pass objects then the list of objects is set to empty. 
            # Needed when calling this method via xml-rpc, cannot marshall objects
            results['terms_list'] = []

        return results


    #################
    #   ZMI PAGES   #
    #################
    security.declareProtected(view_management_screens, 'manage_properties_html')
    manage_properties_html =    PageTemplateFile('zpt/ALiSSAgent/aliss_agent_edit', globals())

    security.declareProtected(view_management_screens, 'manage_settings_html')
    manage_settings_html =      PageTemplateFile('zpt/ALiSSAgent/aliss_agent_settings', globals())


    #####################
    #   PUBLIC PAGES    #
    #####################
    security.declarePublic('index_html')
    index_html =    PageTemplateFile('zpt/ALiSSAgent/aliss_agent_index', globals())

    security.declarePublic('list_html')
    list_html =    PageTemplateFile('zpt/ALiSSAgent/aliss_agent_list', globals())

    security.declarePublic('concept_html')
    concept_html =    PageTemplateFile('zpt/ALiSSAgent/aliss_agent_concept', globals())

    security.declarePublic('terminology_sources_html')
    terminology_sources_html =    PageTemplateFile('zpt/ALiSSAgent/aliss_agent_list_sources', globals())

    security.declarePublic('flash_search')
    flash_search =    PageTemplateFile('zpt/ALiSSAgent/aliss_flash_search', globals())

    security.declarePublic('sitesearch')
    sitesearch =  PageTemplateFile('zpt/ALiSSAgent/sitesearch', globals()) 


    #####################
    #   FLASH CLIENT    #
    #####################
    security.declarePublic('flash_config_xml')
    flash_config_xml = DTMLFile('client/dtml/flash_config_xml', globals())


    #####################
    #   GENERAL Methods #
    #####################
    def getLettersLower(self):  return utils.getLettersLower()
    def getDigits(self):        return utils.getDigits()
    def isNumeric(self, param): return utils.isNumeric(param)
    def compareLetter(self, letter1, letter2):
        return utils.compareLetter(letter1, letter2)

    security.declarePublic('testFirstLetter')
    def testFirstLetter(self, word, letter, dtype):
        """ test the first letter of a word if correspond with a given letter """
        cmp_word = utils.utToUTF8(word)
        if not dtype: return True

        res = False
        if letter == 'num':
            if word[0] in self.getDigits(): res = True
            else:                           res = False
        elif letter == 'other':
            if not (word[0] in self.getDigits() or word[0].lower() in self.getLettersLower()):
                res = True
        elif letter in self.getDigits():
            #res = utils.compareLetter(word[0], letter)
            res = utils.compareLetter(word, letter)
        else:
            #res = utils.compareLetter(word[:dtype], letter[:dtype])
            res = utils.compareLetter(word, letter[:dtype])
        return res

    security.declarePublic('get_terms')
    def get_terms(self, letter, dtype, lang='en'):
        """ return all cataloged terms starting with 'letter' parameter """
        #default data
        terms_list = []
        res = []

        #get cataloged terms
        for aliss_center in self.getAlissCenters():
            terms_list.extend(aliss_center.getElementsByLetter(letter, lang))

        #filter terms by first letter
        alphabet = self.unicode_map(lang)
        letters_list = []
        for letters in alphabet:
            if utils.ut_to_unicode(letter) in letters:
                letters_list = letters
                break
        if len(letters_list) == 0: letters_list = [letter]

        for term in utils.utElimintateDuplicates(terms_list, 'name'):
            trans = term.getTranslation(lang)

            if len(letters_list) == 1:
                #TODO: fix 'other' and 'num'
                res.append(term)
                break
            for let in letters_list:
                if trans.startswith(let):
                    term.url =      utils.utUrlEncode(term.url)
                    term.page_url = utils.utUrlEncode(trans)
                    term.name =     trans
                    res.append(term)
                    break

        return res

    security.declarePublic('hasContent')
    def hasContent(self, letter, dtype=1):
        """ """
        return len(self.get_terms(letter, dtype))

    security.declarePublic('getTerms')
    def getTerms(self, letter, dtype=1, p_start=0, lang='en'):
        """ return all cataloged terms starting with 'letter' parameter """
        #default data
        results = []
        try:    p_start = int(p_start)
        except: p_start = 0

        #get data
        results.extend(utils.utSortObjsListByAttr(self.get_terms(letter, dtype, lang), 'name'))

        #batch related
        batch_obj = batch_utils(self.getResPerPage(), len(results), p_start)
        if len(results) > 0:
            paging_informations = batch_obj.butGetPagingInformations()
        else:
            paging_informations = (-1, 0, 0, -1, -1, 0, self.getResPerPage(), [0])

        return (paging_informations, results[paging_informations[0]:paging_informations[1]])

    security.declarePublic('mergeTopResults')
    def mergeTopResults(self, group_id, terms_list, max_res):
        """ return merged content from main and box Google servers """
        results = {}

        for aliss_term in terms_list:
            group_obj = self.content_group_manager.get_group_item(group_id)
            google_obj = aliss_term.get_google_collection_item(group_id)

            if google_obj:
                #case of indexed google content
                main_pages = google_obj.get_page_collection_by_srv('main_srv')
                box_pages = google_obj.get_page_collection_by_srv('box_srv')

                #test if ALiSS Agent expose this data
                if not(len(main_pages) and 'main_srv' in self.getGoogleServers()):
                    main_pages = []
                if not(len(box_pages) and 'box_srv' in self.getGoogleServers()):
                    box_pages = []

                g_data = {}
                g_data['cg_name'] = group_obj.name
                g_data['cg_updated'] = google_obj.last_updated

                #set indexed google data
                if len(main_pages) or len(box_pages):
                    g_data['google_pages'] = utils.merge_top_results(main_pages, box_pages, max_res)
                else:
                    g_data['google_pages'] = []

                if self.testElement(results, g_data, group_obj.id):
                    results[group_obj.id] = g_data
            else:
                #case of no google content
                g_data = {}
                g_data['cg_name'] = group_obj.name
                g_data['cg_updated'] = None
                g_data['google_pages'] = []
                if self.testElement(results, g_data, group_obj.id):
                    results[group_obj.id] = g_data

        return results

    security.declarePublic('testElement')
    def testElement(self, results, data, group_id):
        """ test witch google data should be return from similar elements """
        if results.has_key(group_id):
            if len(data['google_pages']):
                if data['cg_updated'] > results[group_id]['cg_updated']:
                    return True
            return False
        return True


    #####################################
    #   ALPHABET LISTING AND NAVIGATION #
    #####################################

    def getLettersUpper(self, lang): return utils.getLettersUpper()

    def generateMenu(self, lang):
        """ generate the alphabetic menu """
        menuData = {}
        conceptsNumber = 0
        for aliss_center in self.getAlissCenters():
            query = {'meta_type':     {'query':METATYPE_ALISSELEMENT, 'operator':'and '},
                     'center_parent': {'query':aliss_center.center_uid}}

            for term in utils.utElimintateDuplicates(self.catalog(query), 'name'):
                try:
                    elem_path = self.catalog.getpath(term.data_record_id_)
                    elem_ob = self.catalog.get_aliss_object(elem_path)
                    trans = elem_ob.getTranslation(lang)

                    if len(trans)>0:
                        conceptsNumber += 1

                        for letters in self.unicode_map(lang):
                            for letter in letters:
                                if trans.startswith(letter):
                                    menuData[letters[1].encode('utf8')] = menuData.get(letters[1].encode('utf8'), 0) + 1
                                    raise
                        menuData[trans[0]] = menuData.get(trans[0], 0) + 1

                except:
                    pass
        return (conceptsNumber, menuData)

    def hasOther(self, data, lang):
        """ """
        digits = self.getDigits()
        for key in data.keys():
             if not (key in digits or key.lower() in self.getLettersLower()):
                return True
        return False

    def hasDigits(self, data):
        """ """
        digits = self.getDigits()
        for key in data.keys():
            if key in digits: return True
        return False

    def unicode_langs(self):
        """ temporary list of implemented languages """
        return unicode_character_map.keys()

    def unicode_map(self, lang):
        """ return unicode set of characters for a given language """
        return unicode_character_map[lang]


    #####################
    #   Translations    #
    #####################

    def generateTransLink(self, current_lang, target_lang, REQUEST=None):
        """ """
        url = self.absolute_url()
        if '.%s.' % current_lang in url:
            url = url.replace('.%s.' % current_lang, '.%s.' % target_lang)
        else:
            #EN case, e.g. http://glossary.eea.europa.eu
            url = url.replace('glossary.eea', 'glossary.%s.eea' % target_lang)
            #url = url.replace('alecw.eaudeweb', 'alecw.%s.eaudeweb' % target_lang)
        return url

    def jsSelectedLanguage(self, lang):
        """ """
        return """<script  type="text/javascript">
    // <![CDATA[
        var selected_language = '%s';
    // ]]>
</script>""" % lang

InitializeClass(ALiSSAgent)
