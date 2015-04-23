# -*- coding: ISO-8859-1 -*-
# Copyright (C) 2000-2005 Juan David Ib��ez Palomar <jdavid@itaapy.com>
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


"""
Localizer

This module provides several localized classes, that is, classes with the
locale attribute. Currently it only defines the classes LocalDTMLFile and
LocalPageTemplateFile, which should be used instead of DTMLFile and
PageTemplateFile.
"""

# Import from the Standard Library
import os

# Import from itools
from itools import get_abspath
from itools.gettext import domains

# Import Zope modules
from Globals import DTMLFile

# Import from iHotfix
from Products.iHotfix import DomainAware


class LocalDTMLFile(DTMLFile):

    def __init__(self, name, _prefix=None, **kw):
        apply(LocalDTMLFile.inheritedAttribute('__init__'),
              (self, name, _prefix), kw)

        domain = get_abspath(_prefix, 'locale')
        self.class_domain = domain
        domains.register_domain(domain, domain)


    def _exec(self, bound_data, args, kw):
        # Add our gettext first
        bound_data['gettext'] = self.gettext
        bound_data['ugettext'] = self.gettext  # XXX backwards compatibility
        return apply(LocalDTMLFile.inheritedAttribute('_exec'),
                     (self, bound_data, args, kw))


    def gettext(self, message, language=None):
        return DomainAware.gettext(message, language, self.class_domain)



# Zope Page Templates (ZPT)
# XXX Deprecated, use the i18n namespace instead.
try:
    from Products.PageTemplates.PageTemplateFile import PageTemplateFile
except ImportError:
    # If ZPT is not installed
    class LocalPageTemplateFile:
        pass
else:
    class LocalPageTemplateFile(PageTemplateFile):

        def __init__(self, name, _prefix=None, **kw):
            apply(LocalPageTemplateFile.inheritedAttribute('__init__'),
                  (self, name, _prefix), kw)

            domain = get_abspath(_prefix, 'locale')
            self.class_domain = domain
            domains.register_domain(domain, domain)


        def _exec(self, bound_data, args, kw):
            # Add our gettext first
            bound_data['gettext'] = self.gettext
            bound_data['ugettext'] = self.gettext # XXX backwards compatibility
            return apply(LocalPageTemplateFile.inheritedAttribute('_exec'),
                         (self, bound_data, args, kw))


        def gettext(self, message, language=None):
            return DomainAware.gettext(message, language, self.class_domain)
