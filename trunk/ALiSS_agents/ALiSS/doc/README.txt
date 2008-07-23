Codename: ALiSS
Keywords: "Link suggestions agent", "Link agent", Semantic web, RDF, SKOS


ALiSS stands for "Adaptive Links Suggestion Service".
The idea is to automate links relation between webpages via the use of taxonomies and thesauri in combination with the 
popularity of google search results.

The problem:
On a website there is a need to relate pages with eachother depending on the content. This task is normally done 
manually by experts or webmasters. It is an expensive task which requires a carefull attention and it is also 
technically difficult. The "link expert" is supposed to know basic html knowledge. Moreover the manual task of adding 
links leads after some time to a large ammount of links to be manually maintained and updated. This leads at the end to 
a unsustainable situation of many "broken links", website detoriation and finally visitors unsatisfaction. For this 
reason some website try to minimize the use of links, especially external links, reducing this way the basic feature of 
the web: links.

Goal:
The creation and maintenance of links/relations has to be done centrally and 
in a systematic way. If a page does not exist anymore, all the links to this page will be automatically removed by the 
"Link agent". If the page content change drastically than the link to that page should be reconsidered and re-evaluated 
if still of relevance. If we add a new page, with new fresh content, then all the link to older contents should be 
updated to the new fresh page "re-linked". All these tasks are very expensive for medium and large websites, and cannot 
be done manually. The "Link Agent" will take care of these tasks and only leave a small ammount of configuration tasks 
to the web administrator / webmaster.

Technical architecture:
ALiSS is based on the following technologies.

Programming language: python
Presentation / Template language: HTML, DTML, Page templates and CSS
Information language: XML (RDF/SKOS) and OO database objects
Information protocols: HTTP
Web service API: XML-RPC, SOAP
CMS: Zope


System requirements:
TODO: add minimal requirements and dependencies.

Example on how to use it:
ALiSS can be used both as a "taxonomy" server (A-Z index) and with a set of clients (Flash or Ajax)
 which display related links. See howto:s for more info on how to create your client.
TODO: add some real examples.

Contributors:

   Alexandru Ghica - Eau de Web
   Antonio De Marinis - EEA
   Sasha Vinčić - Systemvaruhuset