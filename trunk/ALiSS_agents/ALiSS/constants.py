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

from Globals import package_home

#Python imports
from os.path import join


#Produc name
ALISS_PRODUCT_NAME = 'ALiSS'
ALISS_PRODUCT_PATH = package_home( globals() )
ALISS_STOPWORDS_ID = 'AlissStopwords'

#Meta types
METATYPE_ALISS=             'ALiSS'
METATYPE_ALISSCENTER =      'ALiSS Center'
METATYPE_ALISSAGENT =       'ALiSS Agent Server'
METATYPE_ALISSCATALOG =     'ALiSS Catalog'
METATYPE_ALISSELEMENT =     'ALiSS Element'
METATYPE_ALISSGROUP =       'ALiSS Content Group'
METATYPE_ALISSGOOGLE =      'ALiSS Google'
METATYPE_ALISSPAGE =        'ALiSS Page'
METATYPE_ALISSLICENSE =     'ALiSS License'
METATYPE_ALISSSTOPWORD =    'ALiSS Stopword'
METATYPE_ALISSSTOPWORDS =   'ALiSS Stopwords'

METATYPE_CATALOGED = [METATYPE_ALISSCENTER, METATYPE_ALISSELEMENT, METATYPE_ALISSGOOGLE, METATYPE_ALISSPAGE]

#Prefixes
PREFIX_ALISS       = 'alis'
PREFIX_ALISSCENTER = 'alisCen'
PREFIX_ALISSAGENT  = 'alisSAg'

#Catalog related
ALISS_CATALOG_ID    = 'ALiSS_catalog'
ALISS_CATALOG_TITLE = 'ALiSS catalog'
ALISS_LEXICON_REMOVE_SW =            'ALiSS: Remove listed stop words only'
ALISS_LEXICON_REMOVE_SW_AND_SINGLE = 'ALiSS: Remove listed and single char words'

#Stopword related
ALISS_STOPWORDS_PATH =      join(CLIENT_HOME, ALISS_PRODUCT_NAME)
ALISS_STOPWORDS_FILENAME =  'aliss_stopwords.xliff'
ALISS_STOPWORDS_FILE =      join(ALISS_STOPWORDS_PATH, ALISS_STOPWORDS_FILENAME)


#default indexes
ALISS_INDEXES = {  'id'                 :('FieldIndex', '', '', ''),  #identifier
                   'meta_type'          :('FieldIndex', '', '', ''),  #identifier
                   'center_parent'      :('FieldIndex', '', '', ''),  #identifier
                   'elem_parent'        :('FieldIndex', '', '', ''),  #identifier
                   'group_id'           :('FieldIndex', '', '', ''),  #identifier
                   'google_parent'      :('FieldIndex', '', '', ''),  #identifier
                   'center_uid'         :('FieldIndex', '', '', ''),  #identifier
                   'g_server'           :('FieldIndex', '', '', ''),  #identifier

#                   'path'               :('PathIndex', '', '', ''),  #not used
                   'name'               :('FieldIndex', '', '', ''),  #element info
                   'getName'            :('FieldIndex', '', '', ''),  #element info
                   'name_suggest'       :('ZCTextIndex', 'name',         'Okapi BM25 Rank', 'Lexicon'),   #element info
                   'id_suggest'         :('ZCTextIndex', 'name',         'Okapi BM25 Rank', 'LexiconID'), #element info
                   'definition'         :('ZCTextIndex', 'definition',   'Okapi BM25 Rank', 'Lexicon'),   #element info
                   'url'                :('FieldIndex', '', '', ''),  #element info

                   'google_error'       :('FieldIndex', '', '', ''),  #google info
                   'google_enable'      :('FieldIndex', '', '', ''),  #google info

                   'page_url'           :('FieldIndex', '', '', ''),  #page info
                   'page_snippet'       :('ZCTextIndex', 'page_snippet', 'Okapi BM25 Rank', 'Lexicon'), #page info
                   'page_title'         :('ZCTextIndex', 'page_title',   'Okapi BM25 Rank', 'Lexicon')
                   }

#Google related
ALISS_DEFAULT_GOOGLE = {  'start'           :0,
                          'maxResults'      :10,
                          'filter'          :1,
                          'restrict'        :'',
                          'safeSearch'      :0,
                          'language'        :'',
                          'inputencoding'   :'UTF-8',
                          'outputencoding'  :'UTF-8',
                          'http_proxy'      :None}
