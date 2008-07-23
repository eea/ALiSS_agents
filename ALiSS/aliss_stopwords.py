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
from OFS.SimpleItem                             import SimpleItem
from Globals                                    import InitializeClass
from AccessControl                              import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile    import PageTemplateFile
from AccessControl.Permissions                  import view_management_screens, view

#Product imports
from Products.ALiSS             import utils
from Products.ALiSS.constants   import *
from Products.ALiSS.managers.stopwords_manager import StopWordManager


class ALiSSStopwords(SimpleItem):
    """ ALiSS Stopwords object """

    meta_type = METATYPE_ALISSSTOPWORDS
    icon = 'misc_/ALiSS/ALiSSStopwords.gif'

    manage_options = (
        (
            {'label':  'Stopwords',
             'action': 'manage_alissStopwords',
             'help':   ('ALiSS','AlissStopwords-management.stx')},

            {'label':  'Management',
             'action': 'manage_alissEdit',
             'help':   ('ALiSS','AlissStopwords-properties.stx')},
        )
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        #constructor
        self.id =               id
        self.title =            title
        self.description =      description
        self.stopword_manager = StopWordManager()


    ########################
    #   STOPWORDS RELATED  #
    ########################
    def checkDuplicate(self, word):
        #return True if a duplicate is found
        return self.stopword_manager.check_duplicate(word)

    security.declareProtected(view_management_screens, 'manage_add_stopword_item')
    def manage_add_stopword_item(self, id=None, stopword='', REQUEST=None):
        """ add stopword """
        if self.checkDuplicate(stopword):
            param = 'err=Duplicate entry !'
        else:
            if not id: id = utils.utGenRandomId()
            self.stopword_manager.add_stopword_item(id, stopword)
            param = 'save=ok'
        if REQUEST: REQUEST.RESPONSE.redirect('manage_alissStopwords?%s' % param)

    security.declareProtected(view_management_screens, 'manage_update_stopword_item')
    def manage_update_stopword_item(self, id='', stopword='', p_start='', REQUEST=None):
        """ update stopword """
        if self.checkDuplicate(stopword):
            param = 'err=Duplicate entry !'
        else:
            self.stopword_manager.update_stopword_item(id, stopword)
            param = 'save=ok'
        if REQUEST: REQUEST.RESPONSE.redirect('manage_alissStopwords?%s&start=%s' % (param, p_start))

    security.declareProtected(view_management_screens, 'manage_delete_stopwords')
    def manage_delete_stopwords(self, ids=[], p_start='', REQUEST=None):
        """ delete stopword """
        del_ids = utils.utConvertToList(ids)
        if REQUEST.get('delete_all'):
            del_ids = self.stopword_manager.get_stopwords_collection().keys()
        self.stopword_manager.delete_stopword_item(del_ids)
        if REQUEST: REQUEST.RESPONSE.redirect('manage_alissStopwords?save=ok&start=%s' % p_start)

    security.declareProtected(view_management_screens, 'getStopwordItemData')
    def getStopwordItemData(self):
        """ return a stopword based on its ID """
        return self.stopword_manager.get_stopword_item_data( self.REQUEST.get('id', None))

    security.declareProtected(view_management_screens, 'getStopwordList')
    def getStopwordsList(self, p_start):
        """ return all stopwords """
        results = []
        res_per_page = 10
        results.extend(self.stopword_manager.get_stopwords_list())

        #batch related
        batch_obj = utils.batch_utils(res_per_page, len(results), p_start)
        if len(results) > 0:
            paging_informations = batch_obj.butGetPagingInformations()
        else:
            paging_informations = (-1, 0, 0, -1, -1, 0, res_per_page, [0])
        return (paging_informations, results[paging_informations[0]:paging_informations[1]])

    security.declareProtected(view_management_screens, 'getStopwordList')
    def exportStopwords(self, REQUEST=None):
        """ export stopwords """
        REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
        REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="aliss.xliff"')
        orig_url = self.absolute_url(1)
        return self.stopword_manager.export_stopwords(orig_url)

    security.declareProtected(view_management_screens, 'importStopwords')
    def importStopwords(self, file, add_type, REQUEST=None):
        """ import stopwords from XLIFF """
        if file:    msg_err = self.stopword_manager.xliff_import(file, add_type)
        else:       msg_err = 'Please select a file to be imported!'
        if msg_err: param_msg = 'op=import&amp;err=%s' % msg_err
        else:       param_msg = 'op=import&amp;save=ok'
        if REQUEST: REQUEST.RESPONSE.redirect('manage_alissStopwords?%s' % param_msg)


    #########################
    #   PROPERTIES ACTIONS  #
    #########################
    security.declareProtected(view_management_screens, 'manageProperties')
    def manageProperties(self, title='', description='', REQUEST=None):
        """ manage basic properties """
        self.title =            title
        self.description =      description
        if REQUEST: REQUEST.RESPONSE.redirect('manage_alissEdit?save=ok')


    #################
    #   ZMI PAGES   #
    #################
    manage_alissStopwords = PageTemplateFile('zpt/ALiSSStopwords/aliss_stopwords_management', globals())
    manage_alissEdit =      PageTemplateFile('zpt/ALiSSStopwords/aliss_stopwords_edit', globals())

InitializeClass(ALiSSStopwords)
