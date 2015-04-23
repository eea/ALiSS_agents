# URLSuck(url,timeout=2.5):
# Return page content from url in UTF8 and 
# wait for a specific amount of seconds (timeout).
# We could say that this is a multi-threaded version of urllib2.urlopen(url).
# by
# Antonio De Marinis
# antonio.de.marinis@eea.eu.int
#
# Library mainly made for getting a Report
# from Cocoon and a glossary box
# from glossary.eea.eu.int
# ver 1.4 with threads

import urllib2
from urllib import quote_plus
from threading import Thread
from threading import enumerate
from threading import currentThread
#from threading2 import Event

def URLEncodedFormat(s):
    return quote_plus(s)

def URLSuck(url,timeout=2.5):
    US=URLSucker(url)
    US.setName('URLSuckerThread')
    US.setDaemon(1) # The URLSucker is a daemonic thread, main thread doesn't wait for it.
    US.start()
    US.join(timeout) # we wait timeout seconds for the URLSucker to finish
    if US.isAlive():
        return '' # we could log here which url took so long time or wait more
    else:
        return US.getURLContent()

def activeThreads():
    names='Total active threads: '
    for t in enumerate():
        names=names+' '+t.getName()
    return names

class URLSucker(Thread):

     def __init__(self,url):
       Thread.__init__(self)
       self.url=url
       self.URLContent=''

     def setURL(self,url):
          self.url=url

     def setEvent(self,msg):
          self.notification=msg

     def run(self):
          self.suckURL(self.url)
           
     def suckURL(self,url):
          try:
           fd = urllib2.urlopen(url) #try to retrieve the url
           self.URLContent = unicode(fd.read(),'utf-8','replace')
           fd.close()
          except:
           self.URLContent = ''

     def getURLContent(self):
	  return self.URLContent
     
     

