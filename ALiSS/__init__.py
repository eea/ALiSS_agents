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

#Zope imports
from ImageFile      import ImageFile
from AccessControl  import ModuleSecurityInfo
from Products.ZCTextIndex.PipelineFactory import element_factory
from Products.ZCTextIndex.Lexicon import StopWordRemover

#Product imports
from Products.ALiSS.constants import *
import Products.ALiSS.aliss
import Products.ALiSS.aliss_stopwords


def initialize(context):
    """ initialize the ALiSS component """

    #add ALiSS Stopwords
    app = context._ProductContext__app
    global Stopwords

    if hasattr(app, ALISS_STOPWORDS_ID):
        Stopwords = getattr(app, ALISS_STOPWORDS_ID)
    else:
        try:
            oStopwords = aliss_stopwords.ALiSSStopwords(ALISS_STOPWORDS_ID, 'ALiSS Stopwords', '')
            app._setObject(ALISS_STOPWORDS_ID, oStopwords)
            transaction().get().note('Added ALiSS Stopwords')
            transaction().commit()
        except:
            pass
        Stopwords = getattr(app, ALISS_STOPWORDS_ID)
    assert Stopwords is not None

    #ALiSS
    context.registerClass(
        aliss.ALiSS,
        constructors = (aliss.manage_addALiSS_html, aliss.manage_addALiSS),
        icon = 'images/ALiSS.gif'
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')

misc_ = {
    #zope object incons
    'ALiSS.gif':            ImageFile('images/ALiSS.gif', globals()),
    'ALiSSCenter.gif':      ImageFile('images/ALiSSCenter.gif', globals()),
    'ALiSSAgent.gif':       ImageFile('images/ALiSSAgent.gif', globals()),
    'ALiSSCatalog.gif':     ImageFile('images/ALiSSCatalog.gif', globals()),
    'ALiSSConcept.gif':     ImageFile('images/ALiSSCenter.gif', globals()),
    'ALiSSStopwords.gif':   ImageFile('images/ALiSSStopwords.gif', globals()),
    #aliss main css
    'aliss.css':            ImageFile('css/aliss.css', globals()),
    'open_quote.gif':            ImageFile('images/open_quote.gif', globals()),
    #flash client
    'flashclient.swf':          ImageFile('client/flash/distribution/flashclient.swf', globals()),
    'swfobject.js':           ImageFile('client/flash/distribution/js/swfobject.js', globals()),
    'BrowserLayoutManager.js':  ImageFile('client/flash/distribution/js/BrowserLayoutManager.js', globals()),
    'flash_client.css':         ImageFile('client/flash/distribution/css/flash_client.css', globals()),
    'standardicon.gif':         ImageFile('images/ALiSSCenter.gif', globals()),
    #google update info icons
    'red.gif':              ImageFile('images/red.gif', globals()),
    'green.gif':            ImageFile('images/green.gif', globals()),
    'googleprogress.gif':   ImageFile('images/googleprogress.gif', globals()),
    #gfslideshow
    'gfslideshow.js':  ImageFile('managers/gfslideshow.js', globals()),
    }

ModuleSecurityInfo('Products.ALiSS.utils').declarePublic('joinToList')
ModuleSecurityInfo('Products.ALiSS.utils').declarePublic('utShowDateTime')
ModuleSecurityInfo('Products.ALiSS.utils').declarePublic('utUrlEncode')
ModuleSecurityInfo('Products.ALiSS.utils').declarePublic('utToUnicode')
ModuleSecurityInfo('Products.ALiSS.utils').apply(globals())


###################################
#   ZCTextIndex Lexicon related   #
###################################
lang_reg = re.compile('#\s*language\s*=\s*([\w]+)')

def read_stopwords():
    res = {}
    language = None

    lines = open(ALISS_STOPWORDS_FILE).readlines()

    for l in lines:
        if not l.strip(): continue

        mo = lang_reg.match(l)
        if mo:
            language = mo.group(1)
            continue

        if l.startswith('#'): continue

        word = l.strip().lower()
        res[word] = None

    return {'stopwords': res, 'language': language}

class ALiSSStopWordRemover:

    dict = read_stopwords()['stopwords']

    try:
        from Products.ZCTextIndex.stopper import process as _process
    except ImportError:
        def process(self, lst):
            has_key = self.dict.has_key
            return [w for w in lst if not has_key(w)]
    else:
        def process(self, lst):
            return self._process(self.dict, lst)

try:
    element_factory.registerFactory('Stop Words',
                                    ALISS_LEXICON_REMOVE_SW,
                                    ALiSSStopWordRemover)
except:
    pass

class ALiSSStopWordAndSingleCharRemover(StopWordRemover):

    dict = read_stopwords()['stopwords']
    for c in range(255):
        dict[chr(c)] = None

try:
    element_factory.registerFactory('Stop Words',
                                    ALISS_LEXICON_REMOVE_SW_AND_SINGLE,
                                    ALiSSStopWordAndSingleCharRemover)
except:
    pass
