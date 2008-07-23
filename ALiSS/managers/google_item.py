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

#Python imports

#Zope imports
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo
from BTrees.OOBTree import OOBTree

#Product imports
from Products.ALiSS.utils                 import getCurrentDate, utSortObjsListByAttr
from Products.ALiSS.constants             import *
from Products.ALiSS.content_filter        import safeXHTMLUnicode
from Products.ALiSS.managers.google_page  import GooglePage


class GoogleItem:
    """ GoogleItem contains information about what content group was used for the 
        google search and all results saved as GooglePage objects.

            >>> from Products.ALiSS.managers.google_item import GoogleItem
            >>> gItem = GoogleItem( id=             'gItem',
            ...                     elem_parent=    'eParent',
            ...                     center_parent=  'cParent',
            ...                     group_id=       'grpId',
            ...                     match_level=    'exact' )

        Let's check if our initiation of GoogleItem worked.

            >>> gItem.id
            'gItem'
            >>> gItem.elem_parent
            'eParent'
            >>> gItem.center_parent
            'cParent'
            >>> gItem.group_id
            'grpId'
            >>> gItem.match_level
            'exact'
            >>> gItem.google_enable
            1
            >>> gItem.google_error
            0
            >>> len(gItem.page_collection)
            0

        We have a clean GoogleItem with no pages(GooglePage) stored. Lets add some pages.

            >>> gItem.add_google_page(id=                   'pageId',
            ...                       google_parent=        'gParent',
            ...                       elem_parent=          'eParent',
            ...                       center_parent=        'cParent',
            ...                       g_server=             'gServer',
            ...                       page_title=           'pTitle',
            ...                       page_url=             'pUrl',
            ...                       page_snippet=         'pSnippet',
            ...                       page_directoryTitle=  'pDirTitle',
            ...                       page_cachedSize=      'pCachedSize',
            ...                       page_hostName=        'pHostName')

        We have added a page with id=pageId, let's try to retrieve it.

            >>> from Products.ALiSS.managers.google_page import GooglePage
            >>> ourPage = gItem.get_page_collection_item('pageId')
            >>> isinstance(ourPage , GooglePage)
            True

        Worked fine, there is not much more we can do here except delete the page :)

            >>> gItem.delete_google_page('pageId')
            >>> ourPage = gItem.get_page_collection_item('pageId2')
            >>> ourPage == None
            True

    """

    meta_type = METATYPE_ALISSGOOGLE
    def __init__(self, id, elem_parent, center_parent, group_id, match_level, google_enable=1, google_error=0):
        #identifiers
        self.id =               id
        self.elem_parent =      elem_parent
        self.center_parent =    center_parent
        self.last_updated =     getCurrentDate()

        #data
        self.group_id =         group_id
        self.match_level =      match_level
        self.google_enable =    google_enable
        self.google_error =     google_error
        self.page_collection =  OOBTree()


    #########################
    #   BASIC OPERATIONS    #
    #########################
    def add_google_page(self, id, google_parent, elem_parent, center_parent, g_server,
                        page_title, page_url, page_snippet, page_directoryTitle, page_cachedSize, page_hostName):
        #Google API sometimes return unicodes and sometimes strings
        f_page_title =      safeXHTMLUnicode(page_title)
        f_page_snippet =    safeXHTMLUnicode(page_snippet)

        #add a page
        page_rank = len(self.page_collection) + 1
        item = GooglePage(id, google_parent,
                          elem_parent,
                          center_parent,
                          g_server,
                          page_title,
                          page_url,
                          page_snippet,
                          page_directoryTitle,
                          page_cachedSize,
                          page_hostName,
                          page_rank)
        self.page_collection[id] = item

    def delete_google_page(self, page_id):
        #delete a page
        if self.page_collection.get(page_id):
            del self.page_collection[page_id]


    ###############
    #   GETTERS   #
    ###############
    def get_page_collection(self):
        #get the collection
        return self.page_collection

    def get_page_collection_objs(self):
        #get the objects list
        return utSortObjsListByAttr(self.page_collection.values(), 'page_rank')

    def get_page_collection_by_srv(self, srv):
        #return pages belonging to a server type
        results = []
        for item in self.get_page_collection_objs():
            g_server = getattr(item, 'g_server', srv)
            if g_server == srv: results.append(item)
        return results

    def get_page_collection_item(self, id):
        #get an item
        return self.page_collection.get(id, None)

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(GoogleItem)
