# -*- coding:utf-8 -*-

import urllib2
import Card
from bs4 import BeautifulSoup

class Spider(object):
    def  __init__(self,muid):
        self.urlString = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid="
        self.muid = muid
        self.errc = 0
        self.tmpmuid = muid
        self.debug = True
    def crawl(self):
        """"crawl through each page of the mtg card database"""
        more = True
        while(more):
            #Open a connection
            connection = urllib2.urlopen(self.urlString + str(self.muid))
            #parse it with beautiful soup
            soup = BeautifulSoup(connection.read(),"html5lib",from_encoding="utf-8")
            if(self.debug):
                print("Downloading...")
            #check if the page is valid card data
            if not self.endSearch(soup.title.string):
                #and if it is, then create the card object and store the data
     	        card = Card.Card(soup,self.muid)
    	        card.store()
            else:
                #If the last error card was not the preceding card then reset the error count
                # (we're checking mostly for )
                if self.tmpmuid is not self.muid-1:
                    self.errc = 0
                self.errc +=1
                self.tmpmuid = self.muid
                if errc > 1000:
                    more = False
            self.muid += 1

            #Close out the stuff we opened
            soup.decompose()
            connection.close()
        if(self.debug):
            print("Done.")


    def endSearch(self,title):
        #The title is always 34 characters for a valid card page
    	if len(title) is not 34:
    		return False
    	else:
    		print "no card here..."
    		return True

    def squirrel(muid, soup):
    	#much like my favourite animal, this will grab and store nuts
    	#or json formatted card data :)
     	card = Card(soup,muid)
    	card.store()
