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
from Products.ALiSS.utils import utUrlEncode

############
#   Info:
#     - http://www.mediawiki.org/wiki/API
#     - http://en.wikipedia.org/w/api.php
################################################

MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/jpe', 'image/svg', 'image/svg+xml', 'image/png']

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

        #TODO: for 'bacteria' query the images are SVG and/or PNG ... same as Wiki logos (e.g. abatement). We need a way to separate them.

        #TODO: use format=XML to grt/parse data
        #TODO: the DIV with google custom search jumps if few data on page
        #TODO: to decide display location on page and to move CSS for MW widget from aliss_agent_concept.zpt

        #TODO: maybe to cache the images or at least URLs retreived from WikiMedia

        #Get images list
        try:
            f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=images&imlimit=%s" % 
                                    (host, utUrlEncode(self.titles), number))
            s = f.read()
        except:
            self.error_log.raising(sys.exc_info())

        images_info = ParserWikipedia()
        images_info.parse(s)

        #Get image(s) url
        images_list = images_info.get_images()
        s = ''

        if len(images_list) > 0:
            param = '|'.join(images_list)
            try:
                f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=url|size|mime&iiurlheight=%s&iiurlwidth=%s" % 
                                        (host, utUrlEncode(param), height, width))
                s = f.read()
            except:
                self.error_log.raising(sys.exc_info())

        urls_info = ParserWikipedia()
        urls_info.parse(s)

        return urls_info.get_urls()
