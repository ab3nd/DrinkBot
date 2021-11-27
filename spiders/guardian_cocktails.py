#!/usr/bin/env python3
import requests
import json
from bs4 import BeautifulSoup
import time
import random
import re

def parse_guardian_drink(url):
    print("   parsing {}".format(url))
    req = requests.get(url)
    bs = BeautifulSoup(req.text)

    # Collect the drinks from the Guardian's drink recipe page
    main_pg = bs.find("div", id="maincontent")

    try:
        # There's one, and it's the drink name    
        drink_name = main_pg.find('h2').text
    except AttributeError:
        # Parse it out of the headline instead
        headline = bs.find("div", {"data-gu-name":"headline"})
        drink_name = headline.find("h1").text.split(":")[1]

    # Get the paragraph tags, 3 is the ingredients, 4 is the instructions
    paras = main_pg.findAll('p')

    # Find the first paragraph that has a number followed by "ml" in it. 
    # That's the ingredients, and the paragraph after it is instructions. 
    amount_re = re.compile("[0-9]+ml")
    for idx in range(len(paras)):
        if amount_re.search(paras[idx].text):
            ingredients = paras[idx].findAll("strong")

            # Sometimes there's an empty paragraph with the ID "sign-in gate",
            # hopefully this kicks past it. 
            instructions = paras[idx+1].text
            if instructions == "":
                instructions = paras[idx+2].text
     
            # The ingredients are in strong tags, although not all in their own 
            # strong tags, so there's some parsing that needs to happen.         
            ingredient_list = []    
            for ingredient in ingredients:
                # replace the br tags inside a strong tag with more strong tags
                ingred_subset = str(ingredient).replace("<br/>","</strong><strong>")
                ingreds = BeautifulSoup(ingred_subset)
                ingredient_list.extend(ingreds.findAll("strong"))

            ingredients = [i.text for i in ingredient_list]    
        
            return {"name": drink_name, "ingredients": ingredients, "instructions": instructions }

    return None

url = "https://www.theguardian.com/food/series/the-good-mixer"

while True:
    print("Getting {}".format(url))
    bs = BeautifulSoup(requests.get(url).text)

    # Get all the drink links
    drink_links = bs.findAll('a', {"class":"u-faux-block-link__overlay js-headline-text"})

    # Get each drink
    for link in drink_links:
        recipe = parse_guardian_drink(link["href"])
        if recipe is None:
            print("Failed on {}".format(link))
        else:
            with open("guardian.json", 'a') as outfile:
                outfile.write("{}\n".format(json.dumps(recipe)))

        # rate limit/evade detection
        time.sleep(1+ random.random()*2)

    # On to the next
    url = bs.find("a", rel="next")["href"]
    if url is None:
        print("We're done here!")
        break
