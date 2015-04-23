# -*- coding: ISO-8859-1 -*-
# Copyright (C) 2000-2004  Juan David Ib��ez Palomar <jdavid@itaapy.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# Import from the Standard Library
from urllib import quote
from time import time

# Import from Zope
from AccessControl import ClassSecurityInfo
import Globals

# Import from Localizer
from LanguageManager import LanguageManager
from LocalAttributes import LocalAttribute, LocalAttributesBase
from LocalFiles import LocalDTMLFile


# XXX
# For backwards compatibility (<= 0.8.0): other classes import 'LocalProperty'
LocalProperty = LocalAttribute


class LocalPropertyManager(LanguageManager, LocalAttributesBase):
    """
    Mixin class that allows to manage localized properties.
    Somewhat similar to OFS.PropertyManager.
    """

    security = ClassSecurityInfo()

    # Metadata for local properties
    # Example: ({'id': 'title', 'type': 'string'},)
    _local_properties_metadata = ()

    # Local properties are stored here
    # Example: {'title': {'en': ('Title', timestamp), 'es': ('T�tul', timestamp)}}
    _local_properties = {}

    # Useful to find or index all LPM instances
    isLocalPropertyManager = 1


    def getLocalPropertyManager(self):
        """
        Returns the instance, useful to get the object through acquisition.
        """
        return self


    def manage_options(self):
        """ """
        if self.need_upgrade():
            # This instance needs to be upgraded
            options = ({'label': u'Upgrade', 'action': 'manage_upgradeForm',
                        'help': ('Localizer', 'LPM_upgrade.stx')},)
        else:
            options = ()

        return options \
               + ({'label': u'Local properties',
                   'action': 'manage_localPropertiesForm',
                   'help': ('Localizer', 'LPM_properties.stx')},
                   {'label': u'Translate properties',
                   'action': 'manage_transPropertiesForm',
                   'help': ('Localizer', 'LPM_translate.stx')},) \
               + LanguageManager.manage_options


    security.declarePublic('hasLocalProperty')
    def hasLocalProperty(self, id):
        """Return true if object has a property 'id'"""
        for property in self._local_properties_metadata:
            if property['id'] == id:
                return 1
        return 0


    security.declareProtected('View management screens',
                              'manage_localPropertiesForm')
    manage_localPropertiesForm = LocalDTMLFile('ui/LPM_properties', globals())

    security.declareProtected('View management screens',
                              'manage_transPropertiesForm')
    manage_transPropertiesForm = LocalDTMLFile('ui/LPM_translations', globals())


    security.declarePublic('get_batch_size')
    def get_batch_size(self):
        """
        Returns the size of the batch for the web interface.
        For now it's a constant value.
        """
        return 5


    security.declarePublic('get_batch_size')
    def get_batch_start(self, start, index):
        """
        Returns the right batch_start, used in the web interfaces.
        """
        # Get the size of the batch
        size = self.get_batch_size()

        start2 = index - size + 1
        if start2 < 0:
            start2 = 0

        if start < start2:
            return start2

        return start


    security.declarePublic('get_url')
    def get_url(self, url, batch_start, batch_index, lang_hide, **kw):
        """
        Used in the 'localPropertiesForm' to generate the urls.
        """
        params = []
        for key, value in kw.items():
            params.append('%s=%s' % (key, quote(value)))

        params.extend(['batch_start:int=%d' % batch_start,
                       'batch_index:int=%d' % batch_index])

        for lang in lang_hide:
            params.append('lang_hide:tuple=%s' % lang)


        return url + '?' + '&amp;'.join(params)


    security.declareProtected('Manage properties', 'set_localpropvalue')
    def set_localpropvalue(self, id, lang, value):
        # Get previous value
        old_value, timestamp = self.get_localproperty(id, lang)
        if old_value is None:
            old_value = ''
        # Update value only if it is different
        if value != old_value:
            properties = self._local_properties.copy()
            if not properties.has_key(id):
                properties[id] = {}

            properties[id][lang] = (value, time())

            self._local_properties = properties


    def get_localproperty(self, name, language):
        if name not in self._local_properties:
            return None, None
        property = self._local_properties[name]
        if language not in property:
            return None, None
        value = property[language]
        if isinstance(value, tuple):
            return value
        return value, None


    security.declareProtected('Manage properties', 'set_localproperty')
    def set_localproperty(self, id, type, lang=None, value=None):
        """Adds a new local property"""
        if not self.hasLocalProperty(id):
            self._local_properties_metadata += ({'id': id, 'type': type},)
            setattr(self, id, LocalProperty(id))

        if lang is not None:
            self.set_localpropvalue(id, lang, value)


    security.declareProtected('Manage properties', 'del_localproperty')
    def del_localproperty(self, id):
        """Deletes a property"""
        # Update properties metadata
        p = [ x for x in self._local_properties_metadata if x['id'] != id ]
        self._local_properties_metadata = tuple(p)

        # delete attribute
        try:
            del self._local_properties[id]
        except KeyError:
            pass

        try:
            delattr(self, id)
        except KeyError:
            pass


    # XXX Backwards compatibility
    _setLocalPropValue = set_localpropvalue
    _setLocalProperty = set_localproperty
    _delLocalProperty = del_localproperty



    security.declareProtected('Manage properties', 'manage_addLocalProperty')
    def manage_addLocalProperty(self, id, type, REQUEST=None, RESPONSE=None):
        """Adds a new local property"""
        self.set_localproperty(id, type)

        if RESPONSE is not None:
            url = "%s/manage_localPropertiesForm?manage_tabs_message=Saved changes." % REQUEST['URL1']
            RESPONSE.redirect(url)


    security.declareProtected('Manage properties', 'manage_editLocalProperty')
    def manage_editLocalProperty(self, REQUEST, RESPONSE=None):
        """Edit a property"""
        def_lang = self.get_default_language()

        form = REQUEST.form
        for prop in self.getLocalProperties():
            name = prop['id']
            if form.has_key(name):
                value = form[name].strip()
                self.set_localpropvalue(name, def_lang, value)

        if REQUEST is not None:
            url = "%s/%s?manage_tabs_message=Saved changes." \
                  % (REQUEST['URL1'], REQUEST['destination'])
            REQUEST.RESPONSE.redirect(url)


    security.declareProtected('Manage properties', 'manage_delLocalProperty')
    def manage_delLocalProperty(self, ids=[], REQUEST=None, RESPONSE=None):
        """Deletes a property"""
        for id in ids:
            self.del_localproperty(id)

        if RESPONSE is not None:
            url = "%s/manage_localPropertiesForm?manage_tabs_message=Saved changes." % REQUEST['URL1']
            RESPONSE.redirect(url)


    security.declareProtected('Manage properties', 'manage_transLocalProperty')
    def manage_transLocalProperty(self, id, code, value, REQUEST,
                                  RESPONSE=None):
        """Translate a property."""
        self.set_localpropvalue(id, code, value.strip())

        if RESPONSE is not None:
            url = "%s/%s?lang=%s&prop=%s&manage_tabs_message=Saved changes." \
                  % (REQUEST['URL1'], REQUEST['destination'], code, id)
            RESPONSE.redirect(url)


    security.declareProtected('Manage properties', 'isObsolete')
    def is_obsolete(self, prop, lang):
        default_language = self.get_default_language()

        value, t0 = self.get_localproperty(prop, default_language)
        value, t1 = self.get_localproperty(prop, lang)

        if t0 is None:
            return False
        if t1 is None:
            return True
        return t1 < t0


    security.declarePublic('getTargetLanguages')
    def get_targetLanguages(self):
        """Get all languages except the default one."""
        def_lang = self.get_default_language()
        all_langs = self.get_languages_mapping()
        for record in all_langs:
            if def_lang == record['code']:
                all_langs.remove(record)
        return all_langs


    security.declarePublic('getLocalProperties')
    def getLocalProperties(self):
        """Returns a copy of the properties metadata."""
        return tuple([ x.copy() for x in self._local_properties_metadata ])


    security.declarePublic('getLocalAttribute')
    def getLocalAttribute(self, id, lang=None):
        """Returns a local property"""
        # No language, look for the first non-empty available version
        if lang is None:
            lang = self.get_selected_language(property=id)

        value, timestamp = self.get_localproperty(id, lang)
        if value is None:
            return ''
        return value

    # XXX For backwards compatibility (<= 0.8.0)
    getLocalProperty = getLocalAttribute


    # Languages logic
    security.declarePublic('get_available_languages')
    def get_available_languages(self, **kw):
        """ """
        languages = self.get_languages()
        id = kw.get('property', None)
        if id is None:
            # Is this thing right??
            return languages
        else:
            if id in self._local_properties:
                property = self._local_properties[id]
                return [ x for x in languages if property.get(x, None) ]
            else:
                return []


    security.declarePublic('get_default_language')
    def get_default_language(self):
        """ """
        if self._default_language:
            return self._default_language

        languages = self.get_languages()
        if languages:
            return languages[0]

        return None


    # Upgrading..
    security.declarePublic('need_upgrade')
    def need_upgrade(self):
        """ """
        return hasattr(self.aq_base, 'original_language')
        

    manage_upgradeForm = LocalDTMLFile('ui/LPM_upgrade', globals())
    def manage_upgrade(self, REQUEST=None, RESPONSE=None):
        """ """
        # In version 0.7 the language management logic moved to the
        # mixin class LanguageManager, as a consequence the attribute
        # "original_language" changes its name to "_default_language".
        if hasattr(self.aq_base, 'original_languge'):
            self._default_language = self.original_language
            del self.original_language

        # XXX With version 1.1.0b5 (as of patch 14) the '_local_properties'
        # data structure keeps a timestamp to mark obsolete translations.
        # The upgrade code below must be activated once the new upgrade
        # framework is deployed, something that should happen for the 1.2
        # release.
##        from types import TupleType
##        for k, v in self._local_properties.items():
##            for i, j in v.items():
##                if type(j) is not TupleType:
##                    # XXX add the timestamp for every property
##                    self._local_properties[k][i] = (j, time())
##        self._p_changed = 1

        if REQUEST is not None:
            return self.manage_main(self, REQUEST)


    # Define <id>_<lang> attributes, useful for example to catalog
    def __getattr__(self, name):
        try:
            index = name.rfind('_')
            id, lang = name[:index], name[index+1:]
            property = self._local_properties[id]
        except:
            raise AttributeError, "%s instance has no attribute '%s'" \
                                  % (self.__class__.__name__, name)

        return self.getLocalAttribute(id, lang)
 


Globals.InitializeClass(LocalPropertyManager)
