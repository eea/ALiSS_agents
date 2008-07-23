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
from Products.ALiSS.utils           import utRead, utGenerateSKOSId, isEmptyString
from Products.ALiSS.content_filter  import safeUnicode
from Products.ALiSS.constants       import *


#skos import
def SkosImport(file):
    """ """
    elements_list = {}
    parser = SkosParser()

    #parse the xml information
    chandler = parser.parseContent(file)

    #return data
    if chandler is None or chandler == 'err':
        return 'err'
    return chandler.content


#skos parser
_SKOS_TAGS = ['skos:prefLabel', 'skos:definition']

class SkosStruct:
    """ """
    def __init__(self, id, url):
        """ """
        self.id = id
        self.url = url
        self.name = ''
        self.definition = ''
        self.translations = {}


class SkosHandler(ContentHandler):
    """ """

    def __init__(self):
        """ """
        self.__currentTag = ''
        self.__data = []
        self.__current_language = ''

        self.__current_elem = None
        self.content = {}

    def startElement(self, name, attrs):
        """ """
        self.__currentTag = name

        if name == 'rdf:RDF':  pass

        if name in ('rdf:Description','skos:Concept'):
            self.__current_elem = SkosStruct(utGenerateSKOSId(safeUnicode(attrs['rdf:about'])),
                                             safeUnicode(attrs['rdf:about']))

        if name == 'skos:prefLabel':
            if attrs.has_key('xml:lang'): 
                self.__current_language = safeUnicode(attrs['xml:lang'])
            else:
                #if language attribute not found then set it to default language English.
                self.__current_language = 'en'

        if name == 'skos:definition':  pass

    def endElement(self, name):
        """ """
        if name == 'skos:prefLabel':
            content = ''.join(self.__data).strip()
            if self.__current_language == 'en':
                self.__current_elem.name = content
            else:
                #set translations if language != EN
                if not isEmptyString(content): self.__current_elem.translations[self.__current_language] = content
            self.__data = []

        if name == 'skos:definition':
            content = ''.join(self.__data).strip()
            self.__data = []
            self.__current_elem.definition = content

        #Some skos files start concept element with rdf:Description
        if name in ('rdf:Description','skos:Concept'):
            self.content[self.__current_elem.id] = self.__current_elem
            self.__current_elem = None

        if name == 'rdf:RDF':  pass

        self.__currentTag = ''

    def characters(self, content):
        currentTag = self.__currentTag
        if currentTag in _SKOS_TAGS:
            self.__data.append(content)

class SkosParser:

    def __init__(self):
        """ """
        pass

    def parseContent(self, file):
        # Create a parser
        try:
            parser = make_parser()
            chandler = SkosHandler()
            # Tell the parser to use our handler
            parser.setContentHandler(chandler)
            # Don't load the DTD from the Internet
            parser.setFeature(handler.feature_external_ges, 0)
            inputsrc = InputSource()

            skos_content = utRead(file)
            inputsrc.setByteStream(StringIO(skos_content))
            parser.parse(inputsrc)
        except:
            return 'err'

        return chandler
