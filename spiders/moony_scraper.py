#!/usr/bin/env python3

# Some drink recipe sites think their javascript is hot shit. 
# They are half right. 
# 
# This web scraper uses selenium to get the content of their pages.  
import json
from selenium import webdriver
import selenium
from selenium.webdriver.support.wait import WebDriverWait
import time
import random

def get_drink(url, driver):
    # Try for a page
    driver.get(url)

    #See if we got the Mr. Boston age verify screen
    buttons = driver.find_elements_by_id("verify-yes")
    if len(buttons) > 0:
        buttons[0].click()
        time.sleep(1)
    
    time.sleep(0.5 + random.random()*2)
    WebDriverWait(driver,3).until(lambda driver: driver.execute_script("return (document.readyState == 'complete' && jQuery.active == 0)"))

    try:
        drink_name = driver.find_element_by_class_name("recipe-name").text
    except:
        drink_name = None

    try:
        # Find the actual elements of the r:ecipe
        i = driver.find_elements_by_xpath("//li[@ng-repeat='ingredient in recipe.recipe_ingredient'][@itemprop='ingredients']")

        ingredients = []
        for ingred in i:
            ingredients.append(ingred.text)
    except selenium.common.exceptions.NoSuchElementException:
        ingredients = ["No ingredients found"]
    
    try:
        # Get the recipe text
        i = driver.find_elements_by_xpath("//span[@ng-bind-html='recipe.instructionsWithLinks']")
        instructions = []
        for instr in i:
            instructions.append(instr.text)
    except selenium.common.exceptions.NoSuchElementException:
        instructions = ["No instructions found"]

    try:
        i = driver.find_elements_by_xpath("//span[@ng-bind-html='recipe.glassHtml']")
        for instr in i:
            instructions.append(instr.text)
    except selenium.common.exceptions.NoSuchElementException:
        instructions.append("No recommended glass found.")

    # Format the recipe
    if drink_name is not None:
        data = {"name": drink_name, "ingredients": ingredients, "instructions": instructions }
    else:
        data = None

    # Get the outgoing recipe links and filter to only recipes
    links = driver.find_elements_by_tag_name('a')
    out_links = [l.get_property("href") for l in links if l.get_property("href").startswith("https://mrbostondrinks.com/recipes/")]

    return data, out_links

# Start a bot-operated browser
d = webdriver.Firefox()
d.set_page_load_timeout(10)

to_visit = set()
visited = set()

# Load up some likely spots
to_visit.add("https://mrbostondrinks.com/recipies/chi-chi")
to_visit.add("https://mrbostondrinks.com/list/tikitropical")
to_visit.add("https://mrbostondrinks.com/list/punches")
to_visit.add("https://mrbostondrinks.com/list/retrovintage")

#Create an output file
while len(to_visit) > 0:
    # Get a URL to visit and mark it as visited
    current_url = to_visit.pop()

    # Some pages have recipes, some don't
    recipe, new_urls = get_drink(current_url, d)
    if recipe is not None:
        with open("mr_boston.json", 'a') as outfile:
            outfile.write("{}\n".format(json.dumps(recipe)))

    # Add the URLs we haven't visited yet
    for url in new_urls:
        if not url in visited:
            to_visit.add(url)

    # Mark this one visited
    visited.add(current_url)

    print("Visited {}, now have {} to visit".format(current_url, len(to_visit)))
d.quit()