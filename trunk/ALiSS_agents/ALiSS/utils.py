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
import re
import operator
import string
import urllib
from whrandom   import choice
from copy       import deepcopy

#Zope imports
from DateTime                              import DateTime
from Products.ALiSS.managers.timeoutsocket import setDefaultSocketTimeout
from Products.PythonScripts.standard       import url_quote

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

def utGenRandomId(p_length=10, p_chars=string.digits):
    """ generate a random numeric id """
    return ''.join([choice(p_chars) for i in range(p_length)])

def utGenerateSKOSId(p_string):
    """ generate the IDs for SKOS elements """
    res = string.strip(p_string)
    res = res.split('http://')[-1]
    return res.replace('/', '_')

def utCleanupId(p_id=''):
    """ cleanup """
    return p_id.translate(TRANSMAP)

def utElimintateDuplicates(p_objects, p_attr='id'):
    """ eliminate duplicates from a list of objects (with ids) """
    dict = {}
    for l_object in p_objects:
        dict[getattr(l_object, p_attr).lower()] = l_object
    return dict.values()

def utInsensitiveSort(inlist, minisort=True):
    """ Case Insensitive Sort """
    #returns (unicode, number_index, brain)
    sortlist = []
    newlist = []
    sortdict = {}
    for entry in inlist:
        try:
            lentry = entry[0].lower()
        except AttributeError:
            sortlist.append((lentry, entry[1], entry[2]))
        else:
            try:
                sortdict[lentry].append(entry)
            except KeyError:
                sortdict[lentry] = [entry]
                sortlist.append((lentry, entry[1], entry[2]))

    sortlist.sort()
    for entry in sortlist:
        try:
            thislist = sortdict[entry[0]]
            if minisort: thislist.sort()
            newlist = newlist + thislist
        except KeyError:
            newlist.append(entry)
    return newlist

def utSortObjsListByAttr(p_list, p_attr, p_desc=0):
    """ sort a list of objects by an attribute values """
    res = []
    l_len = len(p_list)
    l_temp = map(None, map(getattr, p_list, (p_attr,)*l_len), xrange(l_len), p_list)
    res.extend(utInsensitiveSort(l_temp))
    #if p_desc: res.reverse() #not used
    return map(operator.getitem, res, (-1,)*l_len)

def utSortListByLen(p_list, p_desc=1):
    """ sort a list of strings based on strings length """
    l_len = len(p_list)
    l_temp = map(None, map(len, p_list), p_list)
    if p_desc:
        l_temp.reverse()
    return map(operator.getitem, l_temp, (-1,)*l_len)

def utIsListType(p_list):
    """ test if is a list """
    return type(p_list) == type([])

def utConvertToList(something):
    """ convert to list """
    ret = something
    if type(something) is not type([]):
        ret = [something]
    return ret

def utRemoveFromList(l, v):
    """Return a new list, after removing values from v"""
    res = deepcopy(l)
    for k in utConvertToList(v):
        try: res.remove(v)
        except: pass
    return res

def getCurrentDate():
    """ reurn current date """
    return DateTime()

def utRead(file):
    """ read file """
    if 'http' in file:
        #we set timeout socket a bit higher in case we have slower servers or large files
        setDefaultSocketTimeout(200)
        opener = urllib.FancyURLopener()
        f = opener.open(file)
    else:
        f = open(file,'rb+')
    return f.read()

def futRead(p_path, p_flag='r'):
    """ read file """
    return open(p_path, p_flag).read()

def isEmptyString(str):
    """ return true if string is empty: contains only spaces and control chars. """
    str = utToUTF8(str)
    if len(str)>0:
         transtab = string.maketrans('', '')
         idx = string.translate(str, transtab, string.whitespace)
         if len(idx) < 1: return 1
         else:            return 0
    else:
         return 1

    return re.compile(match).search(source,0)

def utStringInString(match, source):
    """ search if a string contains a given string """
    return re.compile(match).search(source,0)

def utShowDateTime(p_date):
    """date is a DateTime object. This function returns a string 'dd month_name yyyy'"""
    try: return p_date.strftime('%d %b %Y - %H:%M')
    except: return ''

def utSplitToList(something, separator='/'):
    """Get a string like value1<separator>value2..., and returns a list [value1, values...]"""
    if something == '': return []
    else:               return str(something).split(separator)

def joinToList(l):
    """Gets a list and returns a comma separated string"""
    return string.join(l, ',')

def utUrlEncode(p_string, qtype=0):
    """Encode a string using url_quote"""
    if qtype: return p_string
    else:     return url_quote(utToUTF8(p_string))

def compareLetter(letter1, letter2):
    """ comapare two letters """
    return string.lower(letter1) == string.lower(letter2)

def formatString(p_string):
    l_tmp = utToUTF8(p_string)
    return string.lower(l_tmp.strip())

def getLettersUpper():
    """ returns all uppercase letters """
    return string.uppercase

def getLettersLower():
    """ returns all lowercase letters """
    return string.lowercase

def getDigits():
    """ returns all digits """
    return string.digits

def isNumeric(param):
    """ test param type """
    param = str(param)
    return param in getDigits() or param =='num'

def merge_top_results(terms_main, terms_box, maxres):
    """ merge results from two lists containing GoolePages objects """
    rank = -1
    for box_term in terms_box:
        if not(len([l_url for l_url in terms_main if l_url.page_url == box_term.page_url]) >0):
            rank += 2
            if len(terms_main) >= rank:
                terms_main.insert(rank, box_term)
            else:
                terms_main.append(box_term)
    return terms_main[:maxres]

def utToUTF8(p_string):
    """ convert a string to UTF-8 """
    if isinstance(p_string, unicode): return p_string.encode('utf-8')
    else: return str(p_string)

def ut_to_unicode(p_string):
    """ convert to unicode """
    if not isinstance(p_string, unicode):
        return unicode(p_string, 'utf-8')
    else:
        return p_string

def utToUnicode(p_data):
    """ convert to unicode """
    if utIsListType(p_data):
        return [ut_to_unicode(k) for k in p_data]
    else:
        return ut_to_unicode(p_data)

def utXmlEncode(p_string):
    """ encode some special chars """
    l_tmp = utToUTF8(p_string)
    l_tmp = l_tmp.replace('&', '&amp;')
    l_tmp = l_tmp.replace('<', '&lt;')
    l_tmp = l_tmp.replace('"', '&quot;')
    l_tmp = l_tmp.replace('\'', '&apos;')
    l_tmp = l_tmp.replace('>', '&gt;')
    return l_tmp


class batch_utils:
    """ batch related class """
    def __init__(self, p_num_result, p_nbr_row, p_cur_position):
        """ """
        self.num_result =   int(p_num_result)
        self.nbr_row =      int(p_nbr_row)
        self.cur_position = int(p_cur_position)

    def __getNumberOfPages(self):
        """ """
        l_number_pages, l_remainder = divmod(self.nbr_row, self.num_result)
        if l_remainder != 0:
            l_number_pages = l_number_pages + 1
        return l_number_pages

    def __getCurrentPage(self):
        """ """
        l_current_page, l_remainder = divmod(self.cur_position * self.__getNumberOfPages(), self.nbr_row)
        return l_current_page

    def __getPagesArray(self):
        """ """
        l_pages = []
        l_current_page = self.__getCurrentPage()
        l_pages_number = self.__getNumberOfPages()
        for i in range(max(0, l_current_page - self.num_result + 1), l_current_page):
            l_pages.append(i)
        for i in range(l_current_page, min(l_current_page + self.num_result, l_pages_number)):
            l_pages.append(i)
        return l_pages

    def butGetPagingInformations(self):
        """ """
        l_start = self.cur_position
        if self.cur_position + self.num_result >= self.nbr_row:
            l_stop = self.nbr_row
            l_next = -1
        else:
            l_stop = self.cur_position + self.num_result
            l_next = self.cur_position + self.num_result
        l_total = self.nbr_row
        if self.cur_position != 0:
            l_prev = self.cur_position - self.num_result
        else:
            l_prev = -1
        l_pages = self.__getPagesArray()
        l_current_page = self.__getCurrentPage()
        l_records_page = self.num_result
        return (l_start, l_stop, l_total, l_prev, l_next, l_current_page, l_records_page, l_pages)