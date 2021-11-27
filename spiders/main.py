#!/usr/bin/env python3
import time
import random
import requests
from bs4 import BeautifulSoup
import re
import json

visited = set()
to_visit = set()


def get_links(html):
    bs = BeautifulSoup(html)
    links = bs.find_all("a")
    linkset = set()
    for link in links:
        try:
            if link["href"].startswith("http"):
                linkset.add(link["href"])
        except:
            print("Link with no href. Weird. ")
    return linkset

def parse_recipe_liquor_com(html):
    # Time to make the soup!
    bs = BeautifulSoup(html)    
    
    # Get the ingredients out of the soup 
    ingred = bs.find(id="structured-ingredients_1-0")
    if ingred is None:
        return

    ingred_list = []
    for ingredient in ingred.find_all("p"):
        # Get the ingredient info
        quantity = ingredient.find("span", {"data-ingredient-quantity":"true"})
        unit = ingredient.find("span", {"data-ingredient-unit":"true"})
        # Case of things like garnishes: "marischino cherry or lemon twist"
        if unit is None and quantity is None:
            name = ingredient.text
            ingred_list.append({"ingred_name": name})
        # Case of a number of something: "6 mint leaves"
        elif unit is None:
            name = ingredient.text.split()[1:]
            " ".join(name)
            ingred_list.append({"ingred_name": name, "ingred_amount": quantity.text})
        # Case of unitless quantity: "A drizzle"
        elif quantity is None:
            name = ingredient.text.split()[1:]
            " ".join(name)
            ingred_list.append({"ingred_name": name, "ingred_unit": unit.text})
        else:
            # Names aren't always in a span, so the name is everything that isn't the 
            # amount and the unit
            name = ingredient.text.split()[2:]
            name = " ".join(name)
            ingred_list.append({"ingred_name": name, "ingred_amount": quantity.text, "ingred_unit": unit.text})
 
    # Get the instructions out of the soup 
    steps = bs.find(id="structured-project__steps_1-0")
    step_list = []
    for step in steps.find_all("p"):
        step_list.append(step.text)
    
    # Get the drink name
    drink_name = bs.find("h1", {"class":"heading__title"}).text

    data = {"name": drink_name, "ingredients": ingred_list, "instructions": step_list}

    with open("liquor_com_drinks.json", "a") as outfile:
        outfile.write("{}\n".format(json.dumps(data)))


def parse_recipe_martha_stewart(html):
    soup = BeautifulSoup(html, "lxml")
    json_script = soup.find("script", type="application/ld+json")

    # If we got the content
    if json_script is not None:
        script_content = json.loads(json_script.text)
        try:
            # If the last thing in the navigation is "Cocktail Recipes"
            if ("Cocktail Recipes" == script_content[0]['itemListElement'][-1]['item']['name']):
                script_content = json.loads(json_script.text)
                drink_name = script_content[1]['name']
                ingredients = script_content[1]["recipeIngredient"]
                instr = script_content[1]["recipeInstructions"]

                step_list = []
                for step in instr:
                    step_list.append(step["text"])

                with open("martha_stewart.json", 'a') as outfile:
                    data = {"name": drink_name, "ingredients": ingredients, "instructions": step_list}
                    outfile.write("{}\n".format(json.dumps(data)))

        except KeyError:
            print("Couldn't find one of the keys in the script, continuing")
        else:
            print("Not a cocktail")
    else:
        print("No script found")

def parse_recipe_cocktaillove(html):
    bs = BeautifulSoup(html)
    drink_name = bs.find("h1", attrs={"class": "recipe-name"}).text


if __name__ == '__main__':
    # req = requests.get("https://www.liquor.com/recipes/lights-out-punch/")
    # parse_recipe(req.text)

    # Blacklist some pages
    #visited.add("https://www.liquor.com/recipes/lights-out-punch/") # Has a defective ingredient (simple syrup)
    #base_url = "https://www.liquor.com"
    #base_matcher = re.compile("www\.liquor\.com")
    
    #Martha stewart has a lot of bad pages
    # base_url = "https://www.marthastewart.com"
    # base_matcher = re.compile("(http|https)://www\.marthastewart\.com")
    # # Blacklist a bad URL on one of the pages
    # visited.add("https://www.marthastewart.comhttps://www.marthastewart.com/1537508/cucumber-salad-herbs-kumquats-and-sumac-dressing")
    # visited.add("https://www.marthastewart.comhttps://www.marthastewart.com/275152/dishwasher-dos-and-donts/")
    # # blacklist some sort of redirect loop
    # visited.add("http://www.marthastewart.com/1533446/applique-kung-fu-shoes")
    # # This link hangs requests (?!)
    # visited.add("http://www.marthastewart.com/node/1082546")
    # visited.add("https://www.marthastewart.com/1084358/poaching-eggs")

    base_url = "https://www.cocktaillove.com/recipes"
    base_matcher = re.compile("(http|https)://www\.marthastewart\.com")
    
    to_visit.add(base_url)

    while len(to_visit) > 0:
        # Get a URL to visit and mark it as visited
        current_url = to_visit.pop()
        
        if not current_url.startswith("http"):
            print("Ignoring non-web link {}".format(current_url))
            continue

        # Get the HTML for the current page
        print("Visiting {}".format(current_url))
        req = requests.get(current_url)
        
        # Check it for a recipe
        parse_recipe_cocktaillove(req.text)        
        visited.add(current_url)
        
        # Remove links that aren't into the base site (don't hit the whole web)
        new_links = get_links(req.text)
        for url in new_links:
            if not re.match(base_matcher, url):        
                visited.add(url)
            # Skip martha stewart garbage URLs
            if re.search("comhttps", url):
                visited.add(url)
        
        # Get links from the current page that haven't been visited yet
        to_visit = to_visit.union(new_links.difference(visited))
        print("Now have {} to visit.".format(len(to_visit)))
        
        # Rate limit 
        time.sleep(random.random())
