# -*- coding: utf-8 -*-
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
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Alexandru Ghica - Finsiel Romania
# Antonio De Marinis - EEA
# Sasha Vinčić - Systemvaruhuset

#Python imports
import string
from whrandom import choice
import operator

#constants
bad_chars = ' ,+&;()[]{}\xC4\xC5\xC1\xC0\xC2\xC3' \
    '\xE4\xE5\xE1\xE0\xE2\xE3\xC7\xE7\xC9\xC8\xCA\xCB' \
    '\xC6\xE9\xE8\xEA\xEB\xE6\xCD\xCC\xCE\xCF\xED\xEC' \
    '\xEE\xEF\xD1\xF1\xD6\xD3\xD2\xD4\xD5\xD8\xF6\xF3' \
    '\xF2\xF4\xF5\xF8\x8A\x9A\xDF\xDC\xDA\xD9\xDB\xFC' \
    '\xFA\xF9\xFB\xDD\x9F\xFD\xFF\x8E\x9E'

good_chars= '___________AAAAAA' \
    'aaaaaaCcEEEE' \
    'EeeeeeIIIIii' \
    'iiNnOOOOOOoo' \
    'ooooSssUUUUu' \
    'uuuYYyyZz'

TRANSMAP = string.maketrans(bad_chars, good_chars)


def utCleanupId(p_id=''):
    """ cleanup """
    return p_id.translate(TRANSMAP)

def utGenRandomId(p_length=10, p_chars=string.digits):
    """ generate a random numeric id """
    return ''.join([choice(p_chars) for i in range(p_length)])

def utSortObjsListByAttr(p_list, p_attr, p_desc=1):
    """ sort a list of objects by an attribute values """
    l_len = len(p_list)
    l_temp = map(None, map(getattr, p_list, (p_attr,)*l_len), xrange(l_len), p_list)
    l_temp.sort()
    if p_desc:
        l_temp.reverse()
    return map(operator.getitem, l_temp, (-1,)*l_len)

def utConvertToList(something):
    """ convert to list """
    ret = something
    if type(something) is type(''):
        ret = [something]
    return ret