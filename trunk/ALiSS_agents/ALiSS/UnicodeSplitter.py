###from utils import classImplements
from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory

import re
enc = 'utf-8'

class Splitter:

    __implements__ = ISplitter

    rx_L = re.compile(r"\w+", re.LOCALE)
    rxGlob_L = re.compile(r"\w+[\w*?]*", re.LOCALE)

    rx_U = re.compile(r"\w+", re.UNICODE)
    rxGlob_U = re.compile(r"\w+[\w*?]*", re.UNICODE)

    def process(self, lst):
        result = []
        for s in lst:
            # This is a hack to get the word splitting working with
            # non-unicode text.
            try:
                if not isinstance(s, unicode):
                    s = unicode(s, enc)
            except (UnicodeDecodeError, TypeError):
                # Fall back to locale aware splitter
                result += self.rx_L.findall(s)
            else:
                words = self.rx_U.findall(s)
                result += [w.encode(enc) for w in words]
        return result

    def processGlob(self, lst):
        result = []
        for s in lst:
            # This is a hack to get the word splitting working with
            # non-unicode text.
            try:
                if not isinstance(s, unicode):
                    s = unicode(s, enc)
            except (UnicodeDecodeError, TypeError):
                # Fall back to locale aware splitter
                result += self.rxGlob_L.findall(s)
            else:
                words = self.rxGlob_U.findall(s)
                result += [w.encode(enc) for w in words]
        return result

###classImplements(Splitter, Splitter.__implements__)

try:
    element_factory.registerFactory('Word Splitter',
        'Unicode Whitespace splitter', Splitter)
except ValueError:
    # In case the splitter is already registered, ValueError is raised
    pass

class CaseNormalizer:

    def process(self, lst):
        result = []
        for s in lst:
            # This is a hack to get the normalizer working with
            # non-unicode text.
            try:
                if not isinstance(s, unicode):
                    s = unicode(s, enc)
            except (UnicodeDecodeError, TypeError):
                result.append(s.lower())
            else:
                result.append(s.lower().encode(enc))
        return result

try:
    element_factory.registerFactory('Case Normalizer',
        'Unicode Case Normalizer', CaseNormalizer)
except ValueError:
    # In case the normalizer is already registered, ValueError is raised
    pass
