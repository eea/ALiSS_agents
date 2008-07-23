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
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo

#Product imports
from Products.ALiSS.constants import *


class GooglePage:
    """ A Google page is one page from the result in a google search. 
        It's used to objectify the page and connect it to a term (ElementItem) and a google search (GoogleItem).

            >>> from Products.ALiSS.managers.google_page import GooglePage
            >>> gPage = GooglePage( id=                     'gPage', 
            ...                     google_parent=          'gParent',
            ...                     elem_parent=            'eParent',
            ...                     center_parent=          'cParent',
            ...                     g_server=               'gServer',
            ...                     page_title=             'pTitle',
            ...                     page_url=               'pUrl',
            ...                     page_snippet=           'pSnippet',
            ...                     page_directoryTitle=    'pDirTitle',
            ...                     page_cachedSize=        'pCachedSize',
            ...                     page_hostName=          'pHostName',
            ...                     page_rank=              'pRank')

        We have now created a google page and stored it in gPage. Let's check if the values are ok.

            >>> gPage.id
            'gPage'
            >>> gPage.google_parent
            'gParent' 
            >>> gPage.elem_parent
            'eParent'
            >>> gPage.center_parent
            'cParent'
            >>> gPage.g_server
            'gServer'
            >>> gPage.page_title
            'pTitle'
            >>> gPage.page_url
            'pUrl'
            >>> gPage.page_snippet
            'pSnippet'
            >>> gPage.page_directoryTitle
            'pDirTitle'
            >>> gPage.page_cachedSize
            'pCachedSize'
            >>> gPage.page_hostName
            'pHostName'
            >>> gPage.page_rank
            'pRank'
            
        Now we call the preview image method. It returns the iamge url of a page thumbnail.
        It should be empty since we have no real page url here.
            >>> gPage.getPreviewImageUrl()
            ''
            
        Seams ok :)

        """


    meta_type = METATYPE_ALISSPAGE
    def __init__(self, id, google_parent, elem_parent, center_parent, g_server, page_title, page_url,
                 page_snippet, page_directoryTitle, page_cachedSize, page_hostName, page_rank):
        #identifiers
        self.id =                   id
        self.google_parent =        google_parent
        self.elem_parent =          elem_parent
        self.center_parent =        center_parent
        self.g_server =             g_server

        #data
        self.page_title =           page_title
        self.page_url =             page_url
        self.page_snippet =         page_snippet
        self.page_directoryTitle =  page_directoryTitle
        self.page_cachedSize =      page_cachedSize
        self.page_hostName =        page_hostName
        self.page_rank =            page_rank

    def getPreviewImageUrl(self):
        """ returns an image url representing the preview for this page content. 
        returns empty string if no preview image exists. """
        #TODO: generalise the code. The solution below is
        # not the most elegant. Now it is specific to EEA web structure. 
        # Constants strings to look-up, could be defined on Aliss settings.
        if self.page_url.find('http://reports.eea.eu.int/')==0:
            return self.page_url+'/aliss_preview.jpg'
        elif self.page_url.find('/indicators/')>0 or self.page_url.find('/ISpecs/ISpecification')>0:
            return self.page_url+'/aliss_preview.gif'
        else:
            return ''

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(GooglePage)
