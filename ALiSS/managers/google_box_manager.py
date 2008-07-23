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
from cStringIO  import StringIO
from types      import UnicodeType, StringType
from xml.sax    import make_parser, handler, InputSource, ContentHandler

#Product imports
from Products.ALiSS           import utils
from Products.ALiSS.constants import *


#Google Box retrieve data
def GBoxImport(file):
    """ """
    elements_list = {}
    parser = GBoxParser()

    #parse the xml information
    chandler = parser.parseContent(file)

    #return data
    if chandler is None or chandler == 'err':
        return 'err'
    return chandler


#Google Box parser
_GBOX_TAGS = ['T', 'S', 'TM', 'Q', 'U', 'S']

class GBoxMeta:
    """ Google Box meta """

    def __init__(self):
        """ constructor """
        self.searchQuery =                  ''  #SET
        self.searchTime =                   ''  #SET
        self.documentFiltering =            ''  #NOT SET YET
        self.searchComments =               ''  #NOT SET YET
        self.estimatedTotalResultsCount =   ''  #NOT SET YET
        self.estimateIsExact =              ''  #NOT SET YET
        self.startIndex =                   ''  #NOT SET YET
        self.endIndex =                     ''  #NOT SET YET
        self.searchTips =                   ''  #NOT SET YET
        self.directoryCategories =          ''  #NOT SET YET


class GBoxResult:
    """ Google Box result """

    def __init__(self):
        """ constructor """
        self.URL =                         ''   #SET
        self.title =                       ''   #SET
        self.snippet =                     ''   #SET
        self.cachedSize =                  ''   #SET
        self.relatedInformationPresent =   ''   #NOT SET YET
        self.hostName =                    ''   #NOT SET YET
        self.directoryCategory =           ''   #NOT SET YET
        self.directoryTitle =              ''   #NOT SET YET
        self.summary =                     ''   #NOT SET YET


class GBoxHandler(ContentHandler):
    """ """

    def __init__(self):
        """ """
        self.__currentTag = ''
        self.__data = []
        self.__current_language = ''

        self.__current_elem = None
        self.meta = None
        self.results = []

    def startElement(self, name, attrs):
        """ """
        self.__currentTag = name

        #parse the meta data
        if name == 'TM':
            self.meta = GBoxMeta()

        if name == 'Q':     pass

        #parse the results
        if name == 'R':
            self.__current_elem = GBoxResult()

        if name == 'U':     pass
        if name == 'T':     pass
        if name == 'S':     pass

        if name == 'C':
            self.__current_elem.cachedSize = attrs['SZ']

    def endElement(self, name):
        """ """
        #parse the meta data
        if name == 'TM':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.meta.searchTime = content

        if name == 'Q':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.meta.searchQuery = content

        #parse the results
        if name == 'U':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.__current_elem.URL = content

        if name == 'T':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.__current_elem.title = content

        if name == 'S':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.__current_elem.snippet = content

        if name == 'R':
            self.results.append(self.__current_elem)
            self.__current_elem = None

        self.__currentTag = ''

    def characters(self, content):
        currentTag = self.__currentTag
        if currentTag in _GBOX_TAGS:
            self.__data.append(content)

class GBoxParser:

    def __init__(self):
        """ """
        pass

    def parseContent(self, file):
        # Create a parser
        try:
            parser = make_parser()
            chandler = GBoxHandler()
            # Tell the parser to use our handler
            parser.setContentHandler(chandler)
            # Don't load the DTD from the Internet
            parser.setFeature(handler.feature_external_ges, 0)
            inputsrc = InputSource()

            gbox_content = utils.utRead(file)
            inputsrc.setByteStream(StringIO(gbox_content))
            parser.parse(inputsrc)
        except:
            return 'err'
        return chandler
