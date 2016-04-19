#!/usr/bin/python
import os
import re
import BeautifulSoup as bs
import pickle

#Walk the directory tree that contains all the HTML pages from the webtender, 
#and generate a set of pickle files containing all the ingredients and the drinks they are in
#Iterate over all the files
	#Parse out the ingredients (and their links/IDs)
	#Build a dictionary of IDs to ingredient names
	#Build a dictionary of IDs to drink numbers
	#Build a dictionary of drink numbers to ingredient IDs
	#Pickle all that data

endNumbers = re.compile("[0-9]*$")

drinkToIngredient = {}
ingredientToDrink = {}
ingredientToName = {}

def addDictList(key, value, toDict):
	if key in toDict.keys():
		toDict[key].append(value)
	else:
		toDict[key] = [value]

def addPair(drinkID, ingredientID):
	addDictList(drinkID, ingredientID, drinkToIngredient)
	addDictList(ingredientID, drinkID, ingredientToDrink)

for root, dirs, files in os.walk("./html"):
	#It's only one directory deep at the moment, so root and dirs are not interesting
	for file in sorted(files):
		with open(root + os.sep + file, "r") as infile:
			print "Processing {0}".format(file)
			recipe = bs.BeautifulSoup(infile)
			ingredients = recipe.findAll('a', href=re.compile("^\/db\/ingred"))
			
			for ingredient in ingredients:
				ingredientID = re.search(endNumbers, ingredient['href'])
				if ingredientID:
					addPair(file, ingredientID.group(0))
					import pdb; pdb.set_trace()
					ingredientToName[ingredientID.group(0)] = ingredient.text

	#Dump everything for debugging
	with open("ingredientsToNames.pkl", 'w') as outfile:
		pickle.dump(ingredientToName, outfile)
	with open("ingredientsToDrinks.pkl", 'w') as outfile:
		pickle.dump(ingredientToDrink, outfile)
	with open("drinksToIngredients.pkl", 'w') as outfile:
		pickle.dump(drinkToIngredient, outfile)