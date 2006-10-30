import google
from data import *

""" Simulate google.py for our tests. """

setLicense = google.setLicense

def doGoogleSearch( q, start = 0, maxResults = 10, filter = 1,
                    restrict='', safeSearch = 0, language = '',
                    inputencoding = '', outputencoding = '',\
                    license_key = None, http_proxy = None ):

    metadata = google.SearchResultsMetaData( GOOGLE_RESULTS['metadata'] )

    filter = ''
    pages=[]
    if 'site:' in q:
        idx = q.index('site:')
        filter = q[idx+5:]
        q = q[:idx].strip()

    dummyGroup={'id':'dummyfilter', 'name':'dummy',      'filter': filter, 'pattern':''}
    #TODO: check how q is to decide exact, medium or weak result
    #check if exact query

    if q.startswith('"') and q.endswith('"'):
        match_level='exact' 
        q = q.replace('"','')
        words = (q,)
        pages=getPagesByTermAndGroup(q,[dummyGroup,])
    elif '+' in q:
        match_level='medium' 
        #medium
        words=[word.strip() for word in q.split('+')
                              if word]

        pages=getPagesByWordsMedium(words,[dummyGroup,])
    elif q.find(' OR ')>-1:
        match_level='weak' 
        #weak
        q = q.replace(' OR ',' ')
        words = q.split(' ')
        pages=getPagesByWordsWeak(words,[dummyGroup,])
    else:
        match_level='undefined'
        #undefined search
        words='emptydummy'
 
    results = []

    if pages:
        for page in pages:
            if not filter or filter in page['URL']:
                results.append( google.SearchResult( page ))

    return google.SearchReturnValue( metadata, results )

def doSpellingSuggestion(phrase, license_key, http_proxy):
    """ Return a revers phrase as a suggestion. """
    return phrase[::-1]

def doGetCachedPage(url, http_proxy):
    return GOOGLE_CACHED_PAGE