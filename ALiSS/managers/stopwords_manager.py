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

# -*- coding: utf8 -*-

#Python imports
import os

#Zope imports
from Globals            import InitializeClass
from AccessControl      import ClassSecurityInfo
from persistent.mapping import PersistentMapping

#Product imports
from Products.ALiSS                         import utils
from Products.ALiSS.constants               import *
from Products.ALiSS.managers.xliff_manager  import xliff_parser


class StopWord:
    """ Stopwords used by catalog and queries.

            >>> from Products.ALiSS.managers.stopwords_manager import StopWord
            >>> sWord = StopWord( id=       'swordId',
            ...                   stopword= 'swordData')

        We have now created a stopword item and stored it in sWord. Let's check if the values are ok.

            >>> sWord.id
            'swordId'
            >>> sWord.stopword
            'swordData'

        Seams ok :)

        """

    meta_type = METATYPE_ALISSSTOPWORD

    def __init__(self, id, stopword):
        self.id =       id
        self.stopword = stopword

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(StopWord)


class StopWordManager:
    """ StopWordManager contains the stopwords list """

    def __init__(self):
        self.__stopwords_collection = PersistentMapping()

    def __add_stopword_item(self, id, stopword):
        #create a new item
        item = StopWord(id, stopword)
        self.__stopwords_collection[id] = item

    def __update_stopword_item(self, id, stopword):
        #modify an item
        item = self.__stopwords_collection.get(id)
        if item is not None:
            item.stopword = stopword
            self.__stopwords_collection[id] = item

    def __delete_stopword_item(self, id):
        #delete an item
        try:    del(self.__stopwords_collection[id])
        except: pass

    def __write_stopwords(self):
        #save stopwords to 'aliss_stopwords.txt'
        if not os.path.isdir(ALISS_STOPWORDS_PATH):
            os.mkdir(ALISS_STOPWORDS_PATH)

        sw_file = open(ALISS_STOPWORDS_FILE, 'w')
        f_write = sw_file.write
        f_write("# language = english\n")
        for w in self.get_stopwords_list():
            f_write("%s\n" % w.stopword)
        sw_file.close()


    #################
    #   BASIC API   #
    #################
    def add_stopword_item(self, id, stopword):
        #create a new item
        self.__add_stopword_item(id, stopword)
        self.__write_stopwords()

    def update_stopword_item(self, id, stopword):
        #modify an item
        self.__update_stopword_item(id, stopword)
        self.__write_stopwords()

    def delete_stopword_item(self, ids):
        #delete 1 or more items
        map(self.__delete_stopword_item, ids)
        self.__write_stopwords()


    #################
    #   GETTERS     #
    #################
    def get_stopwords_collection(self):
        #get the collection
        return self.__stopwords_collection

    def get_stopwords_list(self):
        #get a list with all items
        return utils.utSortObjsListByAttr(self.__stopwords_collection.values(), 'stopword')

    def get_stopword_item(self, id):
        #get an item
        try:    return self.__stopwords_collection[id]
        except: return None

    def get_stopword_item_data(self, id):
        #get an item data
        item = self.get_stopword_item(id)
        if item is not None: 
            return ['update', item.id, item.stopword]
        else:
            return ['add', '', '']

    def check_duplicate(self, word):
        #return True if a duplicate is found
        l_word = utils.formatString(word)
        for k in self.get_stopwords_list():
            if l_word == utils.formatString(k.stopword):
                return 1
        return 0


    ##############
    #   EXPORT   #
    ##############
    def export_stopwords(self, orig_url):
        #create exported stopwords XML
        r = []
        ra = r.append

        #XLIFF header
        ra('<?xml version="1.0" encoding="UTF-8"?>')
        ra('<!DOCTYPE xliff SYSTEM "http://www.oasis-open.org/committees/xliff/documents/xliff.dtd">')
        ra('<!-- XLIFF Format Copyright © OASIS Open 2001-2003 -->')
        ra('<xliff version="1.0">')
        ra('<file original="%s"' % orig_url)
        ra(' product-name="ALiSS"')
        ra(' product-version="0.9.0"')
        ra(' datatype="plaintext"')
        ra(' source-language="English"')
        ra(' target-language="English"')
        ra(' date="%s">' % utils.getCurrentDate().HTML4())
        ra('<body>')

        #XLIFF content
        for sword in self.get_stopwords_list():
            ra('<trans-unit id="%s">' % sword.id)
            ra('<source>%s</source>' % utils.utXmlEncode(sword.stopword))
            ra('<target>%s</target>' % utils.utXmlEncode(sword.stopword))
            ra('</trans-unit>')

        #XLIFF footer
        ra('</body>')
        ra('</file>')
        ra('</xliff>')
        return ''.join(r)


    ##############
    #   IMPORT   #
    ##############
    def xliff_import(self, file, add_type):
        """ XLIFF is the XML Localization Interchange File Format
            designed by a group of software providers.
            It is specified by www.oasis-open.org
        """

        msg_err = ''
        parser = xliff_parser()

        #parse the xliff information
        chandler = parser.parseHeader(file)

        if chandler is None:
            msg_err = 'Unable to parse XLIFF file'

        if not msg_err:
            #delete old stopwords
            if add_type == 'forced_add':
                self.__delete_stopword_item(self.get_stopwords_collection().keys())

            header_info = chandler.getFileTag()
            #get the target language
            target_language = [x for x in header_info if x[0]=='target-language'][0][1]

            body_info = chandler.getBody() #return a dictionary {id: (source, target)}

            for sword_id, sword in body_info.items():
                l_data = sword['target']
                if not self.check_duplicate(l_data):
                    if not sword_id: sword_id = utils.utGenRandomId()
                    self.__add_stopword_item(sword_id, sword['target'])
            self.__write_stopwords()

        return msg_err
