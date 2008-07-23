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

# -*- coding: latin1 -*-

#Python imports
import re


#################
#   FILTERS     #
#################

##########################################################
#
# Python's built in function str() and unicode() return a
# string representation of the object in byte string and
# unicode string respectively. This enhanced version
# of str() and unicode(): safe_unicode() and safe_str()
# can be used as handy functions
# to convert between byte string and unicode.
# This is especially useful in debugging when
# mixup of the string types is suspected.
#
# Usage Ex.:
#     unicode_text = safe_unicode(unicode_text)
#     utf8_text = unicode_text.encode('utf-8')
#
# Source and more info on usage:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/466341
#
##########################################################

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def safeUnicode(text):
    """ returns safe utf8 text """
    unicode_text = safe_unicode(text)
    utf8_text = unicode_text.encode('utf-8')
    return utf8_text

def safeXHTMLUnicode(text):
    """ returns safe utf8 text and simple parsing some tags to XHTML.
    Used for page snippet and term definition."""
    return parseHTMLTags(text)

def parseHTMLTags(expression):
    """ replace HTML tags with XHTML equivalent"""
    l_pattern = re.compile('<br>')
    expression = l_pattern.sub('<br />',expression)
    l_pattern = re.compile('<b>')
    expression = l_pattern.sub('<strong>',expression)
    l_pattern = re.compile('</b>')
    return l_pattern.sub('</strong>',expression)
