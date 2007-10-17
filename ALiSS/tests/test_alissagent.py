import os, sys
import difflib
import glob
import re

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Load fixture
import aliss_test_case
from Products.ALiSS.aliss_center import manage_addAlissCenter
from Products.ALiSS.aliss_agent import manage_addAlissAgent
from data import *
from Products.ALiSS import utils


class ALiSSAgentTest(aliss_test_case.ALiSSTestCase):

    def afterSetUp(self):
        aliss_test_case.ALiSSTestCase.afterSetUp(self)

        #add an ALiSSCenter
        manage_addAlissCenter(self.aliss, ALISS_CENTER['id'], 
                                          ALISS_CENTER['title'], 
                                          ALISS_CENTER['description'], 
                                          ALISS_CENTER['gloss_url'], 
                                          ALISS_CENTER['gloss_skos'])
        self.center = getattr(self.aliss, ALISS_CENTER['id'])
        
        manage_addAlissAgent(self.aliss,  ALISS_AGENT['id'], 
                                          ALISS_AGENT['title'], 
                                          ALISS_AGENT['description'])
        self.agent = getattr(self.aliss, ALISS_AGENT['id'])
        self.addContentGroups()
        self.addLicenses()
        self.center.manageBasicUpdate()
        self.contentGrpId1 = CONTENT_GROUPS[0]['id'] #aaa.com
        self.contentGrpId2 = CONTENT_GROUPS[1]['id'] #bbb.gov
        self.aliss.googleUpdate(self.center.center_uid, [ self.contentGrpId1,self.contentGrpId2], ['main_srv'])


    def test_initialSetup(self):
        agent = self.agent
        self.failIf(agent == None)

        #check the initial values
        self.assertEquals(agent.title, ALISS_AGENT['title']) 
        self.assertEquals(agent.description, ALISS_AGENT['description'])

    def test_manageContentGroups(self):
        agent = self.agent
        
        #test with one content group
        agent.manageContentGroups([self.contentGrpId1])
        
        #check the initial values
        self.assertEquals(agent.content_groups, [self.contentGrpId1]) 


    def test_getTermsForPage(self):
        agent = self.agent
        
        #associate to one content group and center where we have content
        self.agent.manageContentGroups([self.contentGrpId1,])
        self.agent.manageAlissCenters([self.center.center_uid,])
        
        
        #testing with not existing page
        pageURL='http://URL.notexisting.DUMMY'
        terms = agent.getTermsForPage(pageURL)
        self.assertEquals(terms, [])
        
        #testing with existing page
        pageURL=PAGES[0]['URL']

        expectedTerms =getTermsForPage(pageURL,[CONTENT_GROUPS[0],])
        expected=[]
        for tmpterm in  expectedTerms:   
            term=self.center.element_manager.get_element_item(TERMSID_BY_NAME[tmpterm])
            expected.append({'ElementId':term.id,'ElementName':term.name, 'ElementDefinition':term.definition, 'ElementURL':term.url})
            
       
        terms = agent.getTermsForPage(pageURL)
        self.assertEquals(terms.sort(),expected.sort())
        
        #TODO: complete this test with no groups assigned, when we know if groups should be considered or not 
        #test with no groups associated
        #self.agent.manageContentGroups([])
        #terms = agent.getTermsForPage(pageURL)
        #self.assertEquals(terms,[])
        
         
    def test_getTopPagesForTerms(self):
        agent = self.agent
        contentGrp=CONTENT_GROUPS[0]
        
        #associate to one content group and center where we have content
        self.agent.manageContentGroups([contentGrp['id'],])
        self.agent.manageAlissCenters([self.center.center_uid,])
        
        
        #test with one non existing term
        terms='notexistingtermDUMMY'
        pages=agent.getTopPagesForTerms(terms)
        self.assertEquals(pages, [])
        
        #test with one existing term
        term1=TERM_NAMES[0]
        term1_id=TERMSID_BY_NAME[term1]
        term1_list=[term1]
        exppages=[]
        
        term_def = self.center.getElements(term1_id)[0]['definition']
        for tmppage in getPagesByTermAndGroup(term1, [contentGrp,]):
              exppages.append({'url': tmppage['URL'], 'title': tmppage['title'],'preview_img':'','snippet':tmppage['snippet']})
     
        expected=[{'MatchType': 'exact', 
                   'GroupID': contentGrp['id'],
                                   'GroupName': contentGrp['name'], 
                                   'ElementID': term1_id,'ElementName':term1,'ElementDefinition':term_def,'Pages':exppages}]
                                   
        pages=agent.getTopPagesForTerms(term1)
        
        self.assertEquals(pages, expected)
        #test as list
        pages=agent.getTopPagesForTerms(term1_list)
        self.assertEquals(pages,  expected)
     
        #test with two existing terms as string
        terms=TERMSID_BY_NAME.keys()[0]+','+TERMSID_BY_NAME.keys()[1]
        terms_list=[TERMSID_BY_NAME.keys()[0],TERMSID_BY_NAME.keys()[1]]
        
        expected=[]
        for tmpterm in terms_list:
         tmpterm_id=TERMSID_BY_NAME[tmpterm]
         term_def = self.center.getElements(tmpterm_id)[0]['definition']
         exppages=[]
         for tmppage in getPagesByTermAndGroup(tmpterm, [contentGrp]):
              exppages.append({'url': tmppage['URL'], 'title': tmppage['title'],'preview_img':'','snippet':tmppage['snippet']})
         expected.append({'MatchType': 'exact',  'GroupID': contentGrp['id'],'GroupName': contentGrp['name'],'ElementID': tmpterm_id,'ElementName':tmpterm,'ElementDefinition':term_def,'Pages':exppages})
        
        pages=agent.getTopPagesForTerms(terms)
        self.assertEquals(pages, expected)
        #test as list
        pages=agent.getTopPagesForTerms(terms_list)
        self.assertEquals(pages, expected)
        
        #test with two terms (one existing, and one not) as string
        existing_term=TERM_NAMES[0]
        terms=existing_term+',Dummmy Not Existing Term'
        terms_list=[existing_term,'Dummmy Not Existing Term']
        term_id=TERMSID_BY_NAME[existing_term]
        term_def = self.center.getElements(term_id)[0]['definition']

        exppages=[]
        for tmppage in getPagesByTermAndGroup(existing_term, [contentGrp]):
              exppages.append({'url': tmppage['URL'], 'title': tmppage['title'],'preview_img':'','snippet':tmppage['snippet']})
     
        expected=[{'MatchType': 'exact', 
                                   'GroupID': self.contentGrpId1, 'GroupName': contentGrp['name'],
                                   'ElementID': term_id,'ElementName':existing_term,'ElementDefinition':term_def,'Pages':exppages}]

        pages=agent.getTopPagesForTerms(terms)
        self.assertEquals(pages,  expected)
        #test as list
        pages=agent.getTopPagesForTerms(terms_list)
        self.assertEquals(pages, expected)

        #test with no groups associated
        self.agent.manageContentGroups([])
        #test as list
        pages=agent.getTopPagesForTerms(terms_list)
        self.assertEquals(pages, [])
        
    def test_getRelatedPagesForPageSimilar(self):
        agent = self.agent
        #associate to content groups and centers
        self.agent.manageContentGroups([self.contentGrpId1,self.contentGrpId2])
        self.agent.manageAlissCenters([self.center.center_uid,])
        haverelated=0
        
        #the page with want to get relations on.
        for page in PAGES:
            pageURL=page['URL']
            #pageURL='aaa.com/0'
            #we get test data terms for pageURL
            terms=getTermsForPage(pageURL,[CONTENT_GROUPS[0],CONTENT_GROUPS[1]])
            #debug: 
            #print '%s, %s, %s, %s' %(pageURL,terms,CONTENT_GROUPS[0],CONTENT_GROUPS[1])
            #prepare expected pages, note only exact matches are expected
            exppages=[]
            for term_name in terms:
                #get term definition to use as relation description
                term_id=TERMSID_BY_NAME[term_name]
                term_def = self.center.getElements(term_id)[0]['definition']
                tmp_relation_group={'RelationLabel':term_name,'RelationDescription':term_def,'RelationType':'SimilarPage','RelationID':term_id,'MatchType':'exact','Pages':[]}
                tmp_pages=[]
                for tmppage in getPagesByTermAndGroup(term_name,[CONTENT_GROUPS[0],CONTENT_GROUPS[1]]):
                    #we filter out the page we ask for, we do not want same page.
                    if tmppage['URL']!=pageURL :
                       tmp_pages.append({'url': tmppage['URL'], 'title': tmppage['title'],'preview_img':'','snippet':tmppage['snippet']})
                if len(tmp_pages)>0:
                   tmp_relation_group['Pages']=tmp_pages
                   exppages.append(tmp_relation_group)
                   haverelated=1
                   
            gotPages=agent.getRelatedPagesForPage(pageURL,'SimilarPage')
            
            #test for similar pages, if we have same result pages in expected results
            for rgroup in gotPages:
                for egroup in exppages:
                     if egroup['RelationLabel']==rgroup['RelationLabel']:
                         #do we have same number of pages
                         self.assertEquals(len(egroup['Pages']),len(rgroup['Pages']))
                         #ok same number, now let's check if all are the same,do not test order
                         for page in egroup['Pages']:
                             self.failUnless(page in rgroup['Pages'])
                         #do we have all keys and values
                         self.assertEquals(egroup.keys(),rgroup.keys())
                         #ok, all keys there, do we have same values, skip pages already checked.
                         for key in egroup.keys():
                             if key!='Pages':
                                self.assertEquals(egroup[key],rgroup[key])
                                
            #test for simila pages, if we have same exppages in results
            for egroup in exppages:
                for rgroup in gotPages:
                     if egroup['RelationLabel']==rgroup['RelationLabel']:
                         #do we have same number of pages
                         self.assertEquals(len(egroup['Pages']),len(rgroup['Pages']))
                         #ok same number, now let's check if all are the same,do not test order
                         for page in egroup['Pages']:
                             self.failUnless(page in rgroup['Pages'])
                         #do we have all keys and values
                         self.assertEquals(egroup.keys(),rgroup.keys())
                         #ok, all keys there, do we have same values, skip pages already checked.
                         for key in egroup.keys():
                             if key!='Pages':
                                self.assertEquals(egroup[key],rgroup[key])
                         
            #do we have same number of relation groups (same common elements)
            self.assertEquals(len(gotPages),len(exppages))
            
        
        #test we got at least one relation among pages
        self.assertEquals(haverelated, 1)
        
        #test with no groups associated
        self.agent.manageContentGroups([])
        gotPages=agent.getRelatedPagesForPage(pageURL)
        self.assertEquals(gotPages,[])
         
    """ TO BE ENABLED ASAP  """ 
    def test_getRelatedPagesForPageBroader(self):
        agent = self.agent
        #associate to content groups and centers
        self.agent.manageContentGroups([self.contentGrpId1,self.contentGrpId2])
        self.agent.manageAlissCenters([self.center.center_uid,])
        haverelated=0
        
        #the page with want to get relations on.
        pageURL='aaa.com/0'
        #we get test data terms for pageURL
        terms=getTermsForPage(pageURL,[CONTENT_GROUPS[0],CONTENT_GROUPS[1]])
        #debug: 
        #print '%s, %s, %s, %s' %(pageURL,terms,CONTENT_GROUPS[0],CONTENT_GROUPS[1])
        #prepare expected pages, note only exact matches are expected
        """ Dynamic retrival of expected data
        exppages=[]
        for term_name in terms:
            #get broader terms for term
            bterms=getRelatedTermsForTerm(term_name,'BroaderTerm')
            #get pages for broader terms
            for bterm in bterms:
                tmp_relation_group={'RelationType':'BroaderPage','RelationLabel':term_name,'MatchType':'exact','Pages':[]}
                tmp_pages=[]
                for tmppage in getPagesByTermAndGroup(term_name,[CONTENT_GROUPS[0],CONTENT_GROUPS[1]]):
                #we filter out the page we ask for, we do not want same page.
                if tmppage['URL']!=pageURL :
                   tmp_pages.append({'url': tmppage['URL'], 'title': tmppage['title'],'snippet':tmppage['snippet']})
            if len(tmp_pages)>0:
               tmp_relation_group['Pages']=tmp_pages
               exppages.append(tmp_relation_group)
               haverelated=1
               """
               
         
        # expected broader terms (where to get top pages) for aaa.com/0 
        broader_terms=['term AA label2','term label1']
         
        #test with other relation types
        gotPages=agent.getRelatedPagesForPage(pageURL,'BroaderPage')
        for pagegroup in gotPages:
            self.failUnless(pagegroup['RelationLabel'] not in broader_terms)

    def test_getTermSuggestions(self):
        agent = self.agent
        
        #associate to one content group and center where we have content
        self.agent.manageContentGroups([self.contentGrpId1,])
        self.agent.manageAlissCenters([self.center.center_uid,])
        
        term_ids = TERMSID_BY_NAME.values()
        term_names = TERMSID_BY_NAME.keys()
        
        # Get one term by it's name
        terms = agent.getTermSuggestions(term_names[0])
        self.assertEquals(len(terms), 1)
        self.assertEquals(terms[0], term_names[0])
        
        # Get suggestions for 'term'
        search = '%s*' % term_names[0][:3]
        terms = agent.getTermSuggestions(search)
        self.assertEquals(len(terms), len(term_names))
        self.assertEquals(terms.sort(), term_names.sort() )
        
        # test extended
        search = '%s*' % term_names[0][:3]
        terms = agent.getTermSuggestions(search,True)
        self.failUnless('concept_url' in terms[1].keys())

def test_suite():
    import unittest

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ALiSSAgentTest))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
