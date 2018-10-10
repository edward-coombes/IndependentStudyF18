import json
from bs4 import BeautifulSoup
import re
import unicodedata
class Card(object):
    def __init__(self,soup,muid):
     	self.attrs = ["name","effects","flavor","manaCost","types","rarity"]
        self.attr = dict.fromkeys(self.attrs)
        self.soup = soup;
        self.assign("muid",muid)
	self.verbose = True;
    def store(self,verbose=False):
        #store the data in a json file
        labels = self.getLabels()
        self.fillIn(labels)
        if(self.verbose):
            self.printThe()
	    jsonString = json.dumps(self.attr,ensure_ascii=False,encoding="utf-8")
	    db = open("../data/cardDB.json","ab")
	    db.write(jsonString.encode('utf-8'))
	    db.write("\n")
	    db.close()

    def printThe(self):
        #print out every attribute of the card
    	print "\n\n\n\t\tCard Info (" + str(self.attr["muid"]) + "): "
    	print(self.attr["name"])
    	print(self.attr["manaCost"])
    	print(self.attr["types"])
    	print(self.attr["effects"])
    	print(self.attr["flavor"])
    	print(self.attr["rarity"])

    def assign(self,key,value):
        #assign a value to the attr diction
        self.attr[key] = value

    def getLabels(self):
        #parse through the soup, looking for tags of class label
    	labels = list()
    	for tag in self.soup.find_all(class_="label"):
    		labels.append(tag)
    	return labels

    def fillIn(self, labels):
        #using a list of labels (as received from getLabels)
        #fill in all of the attributes of the attr dictionary
    	cardName = re.compile(r".*Card Name:")
    	manaCost = re.compile(r".*Mana Cost:")
    	convManaCost = re.compile(r".*Converted Mana Cost:")
    	types = re.compile(r".*Types:")
    	cardText = re.compile(r".*Card Text:")
    	flavorText = re.compile(r".*Flavor Text:")
    	rarity = re.compile(r".*Rarity:")
    	for label in labels:
            # loop thru all the labels
            # store the values associated with the labels in card
    		if cardName.match(unicode(repr(label.string))):
    			sibling = label.find_next_sibling(class_="value")
    			self.assign("name",sibling.string.strip())
    		elif manaCost.match(unicode(repr(label.string))) and not convManaCost.match(unicode(repr(label.string))):
    			manaString = " "
    			sibling = label.find_next_sibling(class_="value")
    			for manaIcon in sibling.find_all('img'):
    				manaString += manaIcon["alt"] + " "
    			self.assign("manaCost",manaString)
    		elif types.match(unicode(repr(label.string))):
    			sibling = label.find_next_sibling(class_="value")
    			typestr = sibling.string.strip()
    			self.assign("types",typestr)
    		elif cardText.match(unicode(repr(label.string))):
    			eff = self.handleCardText(label.find_next_sibling(class_="value"))
    			self.assign("effects", eff)
    		elif flavorText.match(unicode(repr(label.string))):
    			sibling = label.find_next_sibling(class_="value")
    			flav = ""
    			for string in sibling.stripped_strings:
    				flav += string
    			self.assign("flavor",flav )
    		elif rarity.match(unicode(repr(label.string))):
    			sibling = label.find_next_sibling(class_="value")
    			self.assign("rarity",sibling.span.string)

    def handleCardText(self,soup):
    # receiving a value div for effects
    # loop thru all of the text boxes
    # if there are no images the text can be read as a singke item
    # otherwise, replace images with text and return the effects
    	effectString = u""
    	for effect in soup.find_all(class_="cardtextbox"):
    		if len(effect.find_all('img')) is 0:
    			#There are no activated abilities
    			effectString += " " + unicode(effect.string)#effect.string.encode('utf-8')
    		else:
    	#this effect is an activated ability (or maybe it gives mana who knows)
    			for icon in effect.find_all('img'):
    				icon.replace_with(" " + icon["alt"] + " ")
    			for string in effect.strings:
    				effectString += " " + unicode(string)
    	return effectString
