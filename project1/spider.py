# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import unicodedata
import re
import json

def main():
	urlString = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid="
#	muid = "433296" #ramos
#	muid = "229968" #army of the damned
#	muid = "600"   #black lotus
#	muid = "83807" #copy enchantment
#	muid = "666"	#lich 
	muid = 121495
	more = True
	errc = 0
	tmpmuid = muid
	while more:
#		print "downloading..."
		connection  = urllib2.urlopen(urlString + str(muid))
		soup = BeautifulSoup(connection.read(),"html5lib",from_encoding="utf-8")
		if not endSearch(soup.title.string):
			squirrel(muid,soup)
		else:
			if tmpmuid is not muid-1:
				errc = 0
			errc += 1
			tmpmuid = muid
			if errc > 1000:	
				more = False
		muid += 1
#		print "done"

def getLabels(soup):
	labels = list()
	for tag in soup.find_all(class_="label"):
		labels.append(tag)
	return labels
def fillIn(card,labels):
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
			assign(card,"name",sibling.string.strip())
		elif manaCost.match(unicode(repr(label.string))) and not convManaCost.match(unicode(repr(label.string))):
			manaString = " "
			sibling = label.find_next_sibling(class_="value")
			for manaIcon in sibling.find_all('img'):
				manaString += manaIcon["alt"] + " "
			assign(card,"manaCost",manaString)
		elif types.match(unicode(repr(label.string))):
			sibling = label.find_next_sibling(class_="value")
			typestr = sibling.string.strip()
			assign(card,"types",typestr)
		elif cardText.match(unicode(repr(label.string))):
			eff = handleCardText(label.find_next_sibling(class_="value"))
			assign(card, "effects", eff)
		elif flavorText.match(unicode(repr(label.string))):
			sibling = label.find_next_sibling(class_="value")
			flav = ""
			for string in sibling.stripped_strings:
				flav += string
			assign(card,"flavor",flav )
		elif rarity.match(unicode(repr(label.string))):
			sibling = label.find_next_sibling(class_="value")
			assign(card,"rarity",sibling.span.string)

def handleCardText(soup):
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

def printThe(card):
	print "\n\n\n\t\tCard Info (" + str(card["muid"]) + "): "
	print(card["name"])
	print(card["manaCost"])
	print(card["types"])
	print(card["effects"])
	print(card["flavor"])
	print(card["rarity"])

def storeThe(card):
	jsonString = json.dumps(card,ensure_ascii=False,encoding="utf-8")
	db = open("cardDB.json","ab")
	db.write(jsonString.encode('utf-8'))
	db.write("\n")
	db.close()

def assign(card, attribute, value):
	card[attribute] = value

def endSearch(title):
	if len(title) is not 34:
		return False
	else:
		print "no card here..."
		return True

def squirrel(muid, soup):
	#much like my favourite animal, this will grab and store nuts
	#or json formatted card data :)
 	card = dict.fromkeys(["name","effects","flavor","manaCost","types","rarity"])
	assign(card,"muid",muid)
	#Not every card has an effect, and not every card has a flavor
	#This ensures we have a None value there
#	soup = BeautifulSoup(treeString,"html5lib",from_encoding="utf-8")
	labels = getLabels(soup)
	fillIn(card,labels)
	printThe(card)
	storeThe(card)
if __name__ == "__main__":
	main()
