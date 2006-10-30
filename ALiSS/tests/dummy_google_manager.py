from data import *
from Products.ALiSS.managers.google_box_manager import GBoxImport
from Products.ALiSS.managers.google_manager     import GoogleManager

""" Simulate google box results for our tests. """

def dummyDoGoogleBoxSearch(self, query, start = 0, maxResults = 10, filter = 1, restrict = '', safeSearch = 0, language = '', inputencoding = 'UTF-8', outputencoding = 'UTF-8', http_proxy=None):
    #dummy _doGoogleBoxSearch
    return GoogleManager()._formatGoogleData(GBoxImport(GOOGLE_BOX_RDF))





