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
import urllib2
import sys

from xml.sax.handler    import ContentHandler
from xml.sax            import *
from cStringIO          import StringIO
from types              import StringType, UnicodeType

#Zope imports
from Globals        import InitializeClass
from AccessControl  import ClassSecurityInfo
from DateTime       import DateTime

#Product imports
from Products.ALiSS.utils import utUrlEncode

############
#   Info:
#     - http://www.mediawiki.org/wiki/API
#     - http://en.wikipedia.org/w/api.php
#   Examples:
#     - http://en.wikipedia.org/w/api.php?action=query&titles=water&prop=images&imlimit=3&format=xml
#     - http://commons.wikimedia.org/w/api.php?action=query&titles=Image:Capillarity.svg&prop=imageinfo|categories|revisions&iiprop=timestamp|user|comment|url|size|sha1|mime|metadata|archivename|bitdepth&iiurlheight=200&iiurlwidth=200&rvprop=content&format=xml
#   Example of our query:
#     - http://commons.wikimedia.org/w/api.php?action=query&titles=Image:Cuisson%20des%20pates.jpg|Image:Capillarity.svg|Image:Blue%20Linckia%20Starfish.JPG|Image:Bay%20of%20Fundy%20Low%20Tide.jpg|Image:200407-sandouping-sanxiadaba-4.med.jpg|Image:3D%20model%20hydrogen%20bonds%20in%20water.jpg|Image:Bay%20of%20Fundy%20High%20Tide.jpg&prop=imageinfo|revisions&iiprop=timestamp|user|url|size|mime|metadata&iiurlheight=200&iiurlwidth=200&rvprop=content&format=xml
################################################

# Mime Types we use
MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/jpe', 'image/svg', 'image/svg+xml', 'image/png']
# Image IDs to be ignored. Remeber to replace any '_' with ' ' in the image ID.
WIKI_LOGOS = ['Image:Commons-logo.svg', 'Image:Disambig gray.svg', 'Image:Wiktionary-logo-en.png',
              'Image:Wikisource-logo.svg', 'Image:Ambox content.png', 'Image:Wikibooks-logo.svg',
              'Image:Wikinews-logo.svg', 'Image:Wikiquote-logo.svg', 'Image:Wikiversity-logo-Snorky.svg',
              'Image:Wikiquote-logo-en.svg', 'Image:Wiki_letter_w.svg', 'Image:Wikispecies-logo.svg',
              'Image:Wiktionary-logo-en.svg', 'Image:Wikipedia-logo.png', 'Image:Padlock-silver-medium.svg',
              'Image:Disambig.svg','Image:Globe_important.svg']

#Get MediaWiki data in XML format
class WikiImage:
    """ """

    def __init__(self, title=''):
        """ constructor """
        self.title          = title
        self.size           = ''
        self.width          = ''
        self.height         = ''
        self.thumburl       = ''
        self.thumbwidth     = ''
        self.thumbheight    = ''
        self.url            = ''
        self.descriptionurl = ''
        self.mime           = ''
        self.timestamp      = ''
        self.comment        = ''

    def set_properties(self, data={}):
        for key, value in data.items():
            setattr(self, key, value)

    def get(self, prop): return getattr(self, prop, '').encode('utf-8')

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
        self.__data = []

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
        if name == 'page':
            self.__wikiimg = WikiImage(attrs['title'])
        if name == 'ii' and self.__wikiimg is not None:
            self.__wikiimg.set_properties(attrs)
        if name == 'metadata' and self.__wikiimg is not None:
            self.__wikiimg.set_properties(attrs)

    def endElement(self, name):
        if name == 'ii':
            if self.__wikiimg is not None:
                self.__images.append(self.__wikiimg)
            self.__wikiimg = None
        if name == 'rev':
            data = u''.join(self.__data).strip()
            self.__images[-1].set_properties({'revision': data})
        self.__data = []

    def characters(self, content):
        self.__data.append(content)

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

    def getDescription(self, desc):
        """ """
        res = ''
        start = desc.find('|Description')
        if start > -1: start += 12
        end =   desc.find('|Source')
        desc =  desc[start:end]

        while 1:
            span = (desc.find('{{'), desc.find('}}'))
            if not -1 in span:
                res += desc[span[0]+2:span[1]] + '<br />'
                desc = desc[span[1]+2:]
            else:
                break

        return res

    def get_wiki_images(self, number, host="http://commons.wikimedia.org"):
        try:
            f = urllib2.urlopen("%s/w/api.php?action=query&titles=%s&prop=images&imlimit=%s&format=xml&redirects" % 
                                    (host, utUrlEncode(self.titles), number))
            s = f.read()
        except:
            pass

        parser = mediawiki_parser()
        images_info = parser.parseHeader(s)
        images_list = images_info.get_ids()
        return images_list

    def getImages(self, height, width, number, host):
        """ """
        res = []
        s = ''
        images_list = self.get_wiki_images(number)

        if len(images_list) == 0:
            images_list = self.get_wiki_images(number, 'http://en.wikipedia.org')

        if len(images_list) > 0:
            param = '|'.join(images_list)
            try:
                f = urllib2.urlopen("http://commons.wikimedia.org/w/api.php?action=query&titles=%s&prop=imageinfo|revisions&iiprop=timestamp|user|comment|url|size|mime|metadata&iiurlheight=%s&iiurlwidth=%s&rvprop=content&format=xml" % 
                                        (utUrlEncode(param), height, width))
                s = f.read()
            except:
                pass

        parser = mediawiki_parser()
        urls_info = parser.parseHeader(s)

        if urls_info: res = urls_info.get_images()
        return res

    def getFeed(self, height, width, number, host, REQUEST=None):
        """ """
        ###RSS Header
        res = """<?xml version='1.0' encoding='UTF-8'?>
<rss xmlns:media='http://search.yahoo.com/mrss/' version='2.0'>
  <channel>
    <lastBuildDate>%s</lastBuildDate>
    <title>SlideShow feed from Wikimedia Commons</title>
    <description>These are a sampling of free images from Wikimedia Commons. See disclaimer 
http://commons.wikimedia.org/wiki/Commons:General_disclaimer</description>
    <link>http://commons.wikimedia.org</link>
    <image>
      <url>http://commons.wikimedia.org/wiki/Image:Commons-logo-en.png</url>
      <title>Wikimedia Commons</title>
      <link>http://commons.wikimedia.org</link>
    </image>
    <managingEditor>info-en@wikimedia.org</managingEditor>
              """ % (DateTime())

        ###RSS Body
        images = self.getImages(height, width, number, host)
        for img in images:
            if img.get('thumburl') != '':

                user = img.get('Artist')
                if user == '': user = img.get('user')

                description = self.getDescription(img.get('revision'))
                if description == '': description = img.get('ImageDescription')

                res += """
    <item>
      <guid isPermaLink='false'>%(descriptionurl)s</guid>
      <pubDate>%(timestamp)s</pubDate>
      <title>%(title)s</title>
      <link>%(descriptionurl)s</link>
      <media:group>
        <media:title type='plain'>%(title)s</media:title>
        <media:description type='plain'><![CDATA[%(description)s]]></media:description>
        <media:keywords>%(metadata)s</media:keywords>
        <media:content
            url='%(url)s'
            height='%(height)s' width='%(width)s' type='%(mime)s'
            medium='image'>
        </media:content>
        <media:thumbnail
            url='%(thumburl)s'
            height='%(thumbheight)s' width='%(thumbwidth)s'>
        </media:thumbnail>
        <media:credit>%(user)s</media:credit>
      </media:group>
    </item>
                   """ % {'descriptionurl': img.get('descriptionurl'),
                          'timestamp': img.get('timestamp'),
                          'title': img.get('title'),
                          'description': description,
                          'metadata': img.get('metadata'),
                          'url': img.get('url'),
                          'height': img.get('height'),
                          'width': img.get('width'),
                          'mime': img.get('mime'),
                          'thumburl': img.get('thumburl'),
                          'thumbheight': img.get('thumbheight'),
                          'thumbwidth': img.get('thumbwidth'),
                          'user': user}

        ###RSS Footer
        res += """
  </channel>
</rss>
               """
        return res
