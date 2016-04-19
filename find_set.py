#!/usr/bin/python
import os
import re
import BeautifulSoup as bs
import pickle

#Normalize the drink recipes from the webtender into some format that can be
#used to determine which set of 5 liquids allows the largest drink set

#Some heuristics to trim the set: given five liquids, drinks with >5 ingredients are out
#For each of the remaining ingredients, see how many drinks it is in, 
#eliminate whichever one removes the fewest drinks? This may end up eliminating drinks
#that would have been good to have. 
#For one pump, the largest drink set is whatever the most common ingredient is. 
#Then recalculate the most common ingredient and add it to the next pump. 
#Repeat 5 times, and you should have the the largest set of drinks that can be made with 5 ingredients.

#Find the most common ingredient
#For each drink that contains it, find the next most common ingredient
#Repeat untill all are assigned



def mostCommonIngredient(drinkList):
	counts = {}
	maxCount = None
	maxItem = None
	for drink in drinkList:
		ingredients = drinkToIngredient[drink]
		#print ingredients
		for item in ingredients:
			#Increment the count for this ingredient
			if item in counts.keys():
				counts[item] += 1
			else:
				counts[item] = 1
			#Check if we have a new max
			if counts[item] > maxCount:
				maxCount = counts[item]
				maxItem = item
				
	return maxItem, counts


#Load the existing data from pickle files
with open("drinksToIngredients.pkl", 'r') as drinksFile, open("ingredientsToNames.pkl", 'r') as namesFile:
	drinkToIngredient = pickle.Unpickler(drinksFile).load()
	ingredientToName = pickle.Unpickler(namesFile).load()

	#Now we have a table of ingredients to drinks, drinks to ingredients, and ingredient names
	#Build a list of all drinks with five or fewer ingredients
	shortDrinks = []
	maxIngredientCount = 5
	for drink in drinkToIngredient.keys():
		if len(drinkToIngredient[drink]) <= maxIngredientCount:
			shortDrinks.append(drink)
	print "{0} drinks with {1} or fewer ingredients".format(len(shortDrinks), maxIngredientCount)

	pumps = 0
	while pumps <= maxIngredientCount and len(shortDrinks) > 0 and len(drinkToIngredient) > 0:
		#From the five-or-fewer-ingredient list, get a count of each ingredient
		maxItem, counts = mostCommonIngredient(shortDrinks)

		#Report and move to the next pump
		print "{0} is in {1} drinks".format(ingredientToName[maxItem], counts[maxItem])
		print "Pump {0} gets {1}".format(pumps, ingredientToName[maxItem])
		pumps += 1

		#Throw out all the drinks that don't have the most common ingredient in them
		cutList = []
		for drink in shortDrinks:
			if maxItem in drinkToIngredient[drink]:
				cutList.append(drink)

		#That's our new working list	
		shortDrinks = cutList
		#Report on list length
		print "{0} drinks remaining.".format(len(shortDrinks))

		#Strip out all instances of the most common ingredient from the ingredient dictionary
		scratchDTI = {}
		for drink in shortDrinks:
			ingredients = drinkToIngredient[drink]
			scratchDTI[drink] = [x for x in ingredients if x != maxItem]
			
		#Update drinkToIngredient from scratchDTI, throwing away empty drinks
		drinkToIngredient = {key: value for key, value in scratchDTI.items() if value != []}

		#Update drink list to reflect deletion of empty drinks
		shortDrinks = [d for d in shortDrinks if d in drinkToIngredient.keys()]


