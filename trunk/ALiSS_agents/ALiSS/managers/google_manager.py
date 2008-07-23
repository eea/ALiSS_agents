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
import string
import google
from SOAP import faultType
import sys

#Zope imports

#Product imports
from Products.ALiSS.managers.timeoutsocket      import Timeout
from Products.ALiSS                             import utils
from Products.ALiSS.constants                   import *
from Products.ALiSS.managers.google_box_manager import GBoxImport

class GoogleManager:
    """ """

    def __init__(self):
        self.license = ''
        self.timeout = 5

    def __getDefaultGoogleList(self):
        return ALISS_DEFAULT_GOOGLE.keys()

    def __getValueById(self, id):
        return ALISS_DEFAULT_GOOGLE[id]


    #################
    #   GOOGLE API  #
    #################
    def _formatGoogleData(self, g_data):
        #format Google data
        l_meta = {
            'documentFiltering':            g_data.meta.documentFiltering,
            'searchComments':               g_data.meta.searchComments,
            'estimatedTotalResultsCount':   g_data.meta.estimatedTotalResultsCount,
            'estimateIsExact':              g_data.meta.estimateIsExact,
            'searchQuery':                  g_data.meta.searchQuery,
            'startIndex':                   g_data.meta.startIndex,
            'endIndex':                     g_data.meta.endIndex,
            'searchTips':                   g_data.meta.searchTips,
            'directoryCategories':          g_data.meta.directoryCategories,
            'searchTime':                   g_data.meta.searchTime,
        }
        l_result = []
        for r in g_data.results:
            l_result.append(
                {
                    'URL':                          r.URL,
                    'title':                        r.title,
                    'snippet':                      r.snippet,
                    'cachedSize':                   r.cachedSize,
                    'relatedInformationPresent':    r.relatedInformationPresent,
                    'hostName':                     r.hostName,
                    'directoryCategory':            r.directoryCategory,
                    'directoryTitle':               r.directoryTitle,
                    'summary':                      r.summary,
                }
            )
        return (l_meta, l_result, 'done')

    def _doGoogleBoxSearch(self, query, start = 0, maxResults = 10, filter = 1, restrict = '', safeSearch = 0, language = '', inputencoding = 'UTF-8', outputencoding = 'UTF-8', http_proxy=None):
        #doGoogleBoxSearch
        my_query = '%s/search?q=%s&start=%s&num=%s&restrict=%s&lr=%s&ie=%s&oe=%s&output=%s&client=%s&site=%s' % \
                   (self.aq_parent.gbox,
                    query,
                    start,
                    maxResults,
                    restrict,
                    language,
                    inputencoding,
                    outputencoding,
                    'xml_no_dtd',
                    'default_frontend',
                    'default_collection')

        return self._formatGoogleData(GBoxImport(my_query))

    def doGoogleBoxSearch(self, query, start, maxResults, filter, restrict, safeSearch, language, inputencoding, outputencoding, http_proxy):
        #doGoogleBoxSearch
        try:
            return self._doGoogleBoxSearch(query,
                                           start,
                                           maxResults,
                                           filter,
                                           restrict,
                                           safeSearch,
                                           language,
                                           inputencoding,
                                           outputencoding,
                                           http_proxy)
        except Timeout, error:
            self.error_log.raising(sys.exc_info())
            return ({}, [], 'err')
        except:
            self.error_log.raising(sys.exc_info())
            return ({}, [], 'err')

    def _doGoogleSearch(self, query, start = 0, maxResults = 10, filter = 1, restrict = '', safeSearch = 0, language = '', inputencoding = 'UTF-8', outputencoding = 'UTF-8', http_proxy=None, license_key=''):
        #doGoogleSearch
        return self._formatGoogleData(google.doGoogleSearch(query,
                                                            start,
                                                            maxResults,
                                                            filter,
                                                            restrict,
                                                            safeSearch,
                                                            language,
                                                            inputencoding,
                                                            outputencoding,
                                                            license_key,
                                                            http_proxy))

    def doGoogleSearch(self, query, start, maxResults, filter, restrict, safeSearch, language, inputencoding, outputencoding, http_proxy):
        #doGoogleSearch
        try:
            l_license_key = self.license
            google.setLicense(l_license_key)

            return self._doGoogleSearch(query,
                                        start,
                                        maxResults,
                                        filter,
                                        restrict,
                                        safeSearch,
                                        language,
                                        inputencoding,
                                        outputencoding,
                                        http_proxy,
                                        l_license_key)
        except faultType, error:
#            if (utils.utStringInString('Exception from service', error.faultstring)) or (utils.utStringInString('Invalid authorization key', error.faultstring)) or (self.utStringInString('Daily limit of 1000 queries exceeded', error.faultstring)):
#                return self.doGoogleSearch(query,
#                                           start,
#                                           maxResults,
#                                           filter,
#                                           restrict,
#                                           safeSearch,
#                                           language,
#                                           inputencoding,
#                                           outputencoding,
#                                           http_proxy)
#            else:
#                return ({}, [], 'err')
            self.error_log.raising(sys.exc_info())
            return ({}, [], 'err')
        except Timeout, error:
            self.error_log.raising(sys.exc_info())
            return ({}, [], 'err')
        except:
            self.error_log.raising(sys.exc_info())
            return ({}, [], 'err')

    def doSpellingSuggestion(self, phrase, http_proxy = None):
        google.setLicense( self.license )
        return google.doSpellingSuggestion(phrase, self.license, http_proxy)

    def doGetCachedPage(self, url, http_proxy = None):
        google.setLicense( self.license )
        return google.doGetCachedPage(url, http_proxy)


    #####################
    #   ALISS GOOGLE    #
    #####################
    def _google_search(self, name, filter, gserver, start, maxResults, g_filter, restrict, safeSearch,
                       language, inputencoding, outputencoding, http_proxy, search_type, pattern):
        #decide which Google server to use
        if gserver == 'main_srv':
            doGoogleSearch = self.doGoogleSearch
            qtype = 1
        elif gserver == 'box_srv':
            doGoogleSearch = self.doGoogleBoxSearch
            qtype = 0

        if search_type != 'all':
            #creates Google query
            query = self.createGoogleQuery(name, filter, search_type, pattern, qtype)
            #set match type
            google_match_type = search_type
            #do Google search
            results = doGoogleSearch(query,
                                     start,
                                     maxResults,
                                     filter,
                                     restrict,
                                     safeSearch,
                                     language,
                                     inputencoding,
                                     outputencoding,
                                     http_proxy)
        else:
            #creates Google query
            query = self.createGoogleQuery(name, filter, 'exact', pattern, qtype)
            #do Google search
            results = doGoogleSearch(query,
                                     start,
                                     maxResults,
                                     filter,
                                     restrict,
                                     safeSearch,
                                     language,
                                     inputencoding,
                                     outputencoding,
                                     http_proxy)
            if len(results[1]) or results[2]=='err':
                google_match_type = 'exact'
            else:
                #creates Google search
                query = self.createGoogleQuery(name, filter, 'medium', pattern, qtype)
                #do Google query
                results = doGoogleSearch(query,
                                         start,
                                         maxResults,
                                         filter,
                                         restrict,
                                         safeSearch,
                                         language,
                                         inputencoding,
                                         outputencoding,
                                         http_proxy)
                if len(results[1]) or results[2]=='err':
                    google_match_type = 'medium'
                else:
                    #creates Google search
                    query = self.createGoogleQuery(name, filter, 'weak', pattern, qtype)
                    #do Google query
                    results = doGoogleSearch(query,
                                             start,
                                             maxResults,
                                             filter,
                                             restrict,
                                             safeSearch,
                                             language,
                                             inputencoding,
                                             outputencoding,
                                             http_proxy)
                    google_match_type = 'weak'

        #return Google search result and match type
        return (results, google_match_type)


    #############
    #   OTHER   #
    #############
    def getDefaultGoogleList(self):
        #return the default google search settings
        return self.__getDefaultGoogleList()

    def getValueById(self, id):
        #return an default value by its ID
        return self.__getValueById(id)

    def createGoogleQuery(self, name, group, match_type, pattern, qtype):
        #create google query, if qtype is set to 1 will create the query for a SOAP interogation
        #if qtype is set to 0 a query for Google Box interogation will be created
        if pattern: l_pattern = 'inurl:%s' % pattern
        else:       l_pattern = pattern

        return {
          'exact'   : utils.utUrlEncode(('"%s" %s site:%s') % (name, l_pattern, group), qtype),
          'medium'  : utils.utUrlEncode(('%s %s site:%s') % (' '.join(self.filterStopWords(name)), l_pattern, group), qtype),
          'weak'    : utils.utUrlEncode(('%s %s site:%s') % (' OR '.join(self.filterStopWords(name)), l_pattern, group), qtype)
        }[match_type]

    def setLicense(self, license):
        self.license = license
