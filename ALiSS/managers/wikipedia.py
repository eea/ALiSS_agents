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
import sgmllib
import sys

from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO
from types import StringType, UnicodeType

#Product imports
from Products.ALiSS.utils import utUrlEncode

############
#   Info:
#     - http://www.mediawiki.org/wiki/API
#     - http://en.wikipedia.org/w/api.php
################################################

MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/jpe', 'image/svg', 'image/svg+xml', 'image/png']

#Get MediaWiki data in XML format
class mediawiki_handler(ContentHandler):
    """ """

    def __init__(self):
        """constructor """
        self.__images = []

        self.__thumbs = []
        self.__origs = []
        self.__mimes = []

    def get_images(self):
        return self.__images

    def set_images(self, url):
        self.__images.append(url)


    def get_thumbs(self):
        return self.__thumbs

    def set_thumbs(self, url):
        self.__thumbs.append(url)

    def get_origs(self):
        return self.__origs

    def set_origs(self, url):
        self.__origs.append(url)

    def get_mimes(self):
        return self.__mimes

    def set_mimes(self, url):
        self.__mimes.append(url)


    def get_urls(self):
        res = {}
        if len(self.get_thumbs())==len(self.get_origs()):
            for k in range(len(self.get_thumbs())):
                if self.__mimes[k] in MIME_TYPES:
                    res[k] = {'thumb': self.__thumbs[k], 'orig': self.__origs[k]}
        return res


    def startElement(self, name, attrs):
        if name == 'im':
            for attr in attrs.keys():
                if attr == 'title':
                    self.set_images(attrs[attr])
        if name == 'ii':
            for attr in attrs.keys():
                if attr == 'thumburl':
                    self.set_thumbs(attrs[attr])
                if attr == 'descriptionurl':
                    self.set_origs(attrs[attr])
                if attr == 'mime':
                    self.set_mimes(attrs[attr])


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

#Get MediaWiki data in HTML format
class ParserWikipedia(sgmllib.SGMLParser):
    """ """

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.images = []
        self.thumbs = []
        self.origs = []
        self.mimes = []
        self.inside_span_element = 0

    def start_span(self, attributes):
        self.inside_span_element = 1

    def end_span(self):
        self.inside_span_element = 0

    def start_a(self, attributes):
        for name, value in attributes:
            if name == "href":
                if ('upload.wikimedia.org' in value) and ('thumb' in value): self.thumbs.append(value)
                if 'commons.wikimedia.org' in value: self.origs.append(value)

    def get_images(self):
        return self.images

    def get_urls(self):
        res = {}
        if len(self.thumbs)==len(self.origs):
            for k in range(len(self.thumbs)):
                if self.mimes[k] in MIME_TYPES:
                    res[k] = {'thumb': self.thumbs[k], 'orig': self.origs[k]}
        return res

    def handle_data(self, data):
        if self.inside_span_element:
            if 'Image:' in data:
                self.images.append(data)
            if 'image/' in data:
                self.mimes.append(data)

    def parse(self, s):
        self.feed(s)
        self.close()


class WikipediaImages:
    """ """

    def __init__(self, titles):
        """ """
        self.titles = titles

    def getImages(self, height, width, number, host):
        """ """
        res = {}
        s = ''

        #TODO: the DIV with google custom search jumps if few data on page
        #TODO: to decide display location on page and to move CSS for MW widget from aliss_agent_concept.zpt

        #TODO: maybe to cache the images or at least URLs retreived from WikiMedia

        #Get images list
        try:
            f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=images&imlimit=%s&format=xml" % 
                                    (host, utUrlEncode(self.titles), number))
            s = f.read()
        except:
            self.error_log.raising(sys.exc_info())

        parser = mediawiki_parser()
        images_info = parser.parseHeader(s)

        ###For HTML format
        #images_info = ParserWikipedia()
        #images_info.parse(s)

        #Get image(s) url
        images_list = images_info.get_images()
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

        ###For HTML format
        #urls_info = ParserWikipedia()
        #urls_info.parse(s)

        return urls_info.get_urls()
