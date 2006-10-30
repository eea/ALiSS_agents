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

from Globals import package_home

#Produc name
EEAALISS_PRODUCT_NAME = "EEAALiSS"
EEAALISS_PRODUCT_PATH = package_home( globals() )

#Meta types
METATYPE_EEAALISS = 'EEA ALiSS'
METATYPE_ALISSLICENSE = 'ALiSS License'
METATYPE_ALISSGROUP = 'ALiSS Content Group'

#Prefixes
PREFIX_EEAALISS = 'eea'
PREFIX_ALISS = 'alis'

#Default data
ALISS_CATALOG_ID    = 'ALiSS_catalog'

#Temporary 'Google Licences'
ALISS_GOOGLE_KEYS = [{'id':'1000000001', 'license':'CLHCQF9QFHIOsnLzC0g4Y01vGCOHGF7Q'},
                     {'id':'1000000002', 'license':'0Uvp9vVQFHKYecyrhLsTf7DPL0HLHY7P'}]

#EEA Google Box
ALISS_GOOBLE_BOX = 'http://google.eea.eu.int'

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

DEFAULT_CONTENT_GROUPS = [{'id':'1000000001', 'name':'EIONET',      'filter':'eionet.eu.int',               'pattern':''},
                          {'id':'1000000002', 'name':'CHM',         'filter':'biodiversity-chm.eea.eu.int', 'pattern':''},
                          {'id':'1000000003', 'name':'EEA',         'filter':'eea.eu.int',                  'pattern':''},
                          {'id':'1000000004', 'name':'REPORTS',     'filter':'reports.eea.eu.int',          'pattern':''},
                          {'id':'1000000005', 'name':'THEMES',      'filter':'themes.eea.eu.int',           'pattern':''},
                          {'id':'1000000006', 'name':'EEA ORG',     'filter':'org.eea.eu.int',              'pattern':''},
                          {'id':'1000000007', 'name':'DATASERVICE', 'filter':'dataservice.eea.eu.int',      'pattern':''},
                          {'id':'1000000008', 'name':'EWINDOWS',    'filter':'ewindows.eu.org',             'pattern':''}]