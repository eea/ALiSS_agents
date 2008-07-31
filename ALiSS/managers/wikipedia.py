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

#Python imports
import urllib2
import sys

from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO
from types import StringType, UnicodeType

#Zope imports
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo

#Product imports
from Products.ALiSS.utils import utUrlEncode

############
#   Info:
#     - http://www.mediawiki.org/wiki/API
#     - http://en.wikipedia.org/w/api.php
#   Examples:
#     - http://en.wikipedia.org/w/api.php?action=query&titles=water&prop=images&imlimit=3&format=xml
#     - http://en.wikipedia.org/w/api.php?action=query&titles=Image%3A200407-sandouping-sanxiadaba-4.med.jpg%7CImage%3A3D%20model%20hydrogen%20bonds%20in%20water.jpg%7CImage%3ABay%20of%20Fundy%20High%20Tide.jpg&&prop=imageinfo&iiprop=url|size|mime&iiurlheight=200&iiurlwidth=200&format=xml
################################################

# Mime Types we use
MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/jpe', 'image/svg', 'image/svg+xml', 'image/png']
# Image IDs to be ignored. Remeber to replace any '_' with ' ' in the image ID.
WIKI_LOGOS = ['Image:Commons-logo.svg', 'Image:Disambig gray.svg', 'Image:Wiktionary-logo-en.png', 'Image:Wikisource-logo.svg', 'Image:Ambox content.png']

#Get MediaWiki data in XML format
class WikiImage:
    """ """

    def __init__(self, title=''):
        """ constructor """
        self.title          = ''
        self.size           = ''
        self.width          = ''
        self.height         = ''
        self.thumburl       = ''
        self.thumbwidth     = ''
        self.thumbheight    = ''
        self.url            = ''
        self.descriptionurl = ''
        self.mime           = ''

    def set_properties(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(WikiImage)

class mediawiki_handler(ContentHandler):
    """ """

    def __init__(self):
        """ constructor """
        self.__images = []
        self.__ids = []
        self.__wikiimg = None

    def get_ids(self):
        return self.__ids

    def set_ids(self, url):
        if url not in WIKI_LOGOS and url not in self.__ids:
             self.__ids.append(url)

    def get_images(self):
        res = []
        for img in self.__images:
            if img.mime in MIME_TYPES:
                res.append(img)
        return res

    def startElement(self, name, attrs):
        if name == 'im':
            for attr in attrs.keys():
                if attr == 'title':
                    self.set_ids(attrs[attr])
        if (name == 'page') and 'pageid' not in attrs.keys():
            self.__wikiimg = WikiImage(attrs['title'])
        if name == 'ii' and self.__wikiimg is not None:
            self.__wikiimg.set_properties(attrs)

    def endElement(self, name):
        if name == 'ii':
            if self.__wikiimg is not None:
                self.__images.append(self.__wikiimg)
            self.__wikiimg = None

class mediawiki_parser:
    """ """

    def __init__(self):
        """ """
        pass

    def parseContent(self, xml_string):
        """ """
        chandler = mediawiki_handler()
        parser = make_parser()
        parser.setContentHandler(chandler)
        parser.setFeature(handler.feature_external_ges, 0)
        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(xml_string))
        try:
            parser.parse(inpsrc)
            return chandler
        except:
            return None

    def parseHeader(self, file):
        parser = make_parser()
        chandler = mediawiki_handler()
        parser.setContentHandler(chandler)
        try:    parser.setFeature(handler.feature_external_ges, 0)
        except: pass
        inputsrc = InputSource()

        try:
            if type(file) is StringType:
                inputsrc.setByteStream(StringIO(file))
            else:
                filecontent = file.read()
                inputsrc.setByteStream(StringIO(filecontent))
            parser.parse(inputsrc)
            return chandler
        except:
            return None

class WikipediaImages:
    """ """

    def __init__(self, titles):
        """ """
        self.titles = titles

    def getImages(self, height, width, number, host):
        """ """
        res = []
        s = ''

       #Get images list
        try:
            f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=images&imlimit=%s&format=xml" % 
                                    (host, utUrlEncode(self.titles), number))
            s = f.read()
        except:
            self.error_log.raising(sys.exc_info())

        parser = mediawiki_parser()
        images_info = parser.parseHeader(s)

        #Get image(s) url
        images_list = images_info.get_ids()
        s = ''

        if len(images_list) > 0:
            param = '|'.join(images_list)
            try:
                f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=url|size|mime&iiurlheight=%s&iiurlwidth=%s&format=xml" % 
                                        (host, utUrlEncode(param), height, width))
                s = f.read()
            except:
                self.error_log.raising(sys.exc_info())

        parser = mediawiki_parser()
        urls_info = parser.parseHeader(s)

        if urls_info: res = urls_info.get_images()
        return res
