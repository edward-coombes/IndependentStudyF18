# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import unicode
#compile(r".*Rarity:")


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
	effectString = " "
	for effect in soup.find_all(class_="cardtextbox"):
		if len(effect.find_all('img')) is 0:
			#There are no activated abilities
			effectString += str(effect.string)
		else:
	#this effect is an activated ability (or maybe it gives mana who knows)
			for icon in effect.find_all('img'):
				icon.replace_with(" " + icon["alt"] + " ")
			for string in effect.strings:
				effectString += " " + str(string)
	return effectString

def printThe(card):
	print "\n\n\n\n\n\n\n\t\tCard Info: "
	print(card["name"])
	print(card["manaCost"])
	print(card["types"])
	print(card["effects"])
	print(card["flavor"])
	print(card["rarity"])

def storeThe(card):
	jsonString = json.dumps(card,ensure_ascii=False,encoding="utf-8")
	db = open("cardDB.json","a")
	db.write(jsonString)
	db.write("\n")
	db.close()

def assign(card, attribute, value):
	card[attribute] = value

def main():
 	card = dict.fromkeys(["effects","flavor"])
	#Not every card has an effect, and not every card has a flavor
	#This ensures we have a None value there
	fp = open("tmpCard.html",'r')	
	soup = BeautifulSoup(fp,"html5lib",from_encoding="utf-8")
	fp.close()
	labels = getLabels(soup)
	fillIn(card,labels)
	printThe(card)
	storeThe(card)

if __name__ == "__main__":
	main()
