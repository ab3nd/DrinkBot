#!/usr/bin/env python3
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import json

visited = set()
to_visit = set()

all_cocktails = []

def parse_recipe_selenium(url):
    
    # Start a bot-operated browser
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(100)
    driver.get(url)

    recipe = {"name":""}

    # Scroll to the end of the page (from https://stackoverflow.com/questions/32391303/how-to-scroll-to-the-end-of-the-page-using-selenium-in-python)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(0.5)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    # Get all the links in the page
    links = [l.get_attribute('href') for l in driver.find_elements_by_tag_name("a")]
    
    # Get the soup and find the script tag
    bs = BeautifulSoup(driver.page_source, "lxml") 
    json_tag = bs.find("script", id="json-ld")
    if json_tag is None:
        print(f"No JSON for {url}")
        driver.quit()
        return links
    data = json.loads(json_tag.text)

    if type(data) is list:
        data = data[0]

    cocktail = {}
    if 'recipeInstructions' in data.keys():
        cocktail["instructions"] = []
        for instr in data["recipeInstructions"]:
            cocktail["instructions"].append(instr['text'])     
    if 'recipeIngredient' in data.keys():
        cocktail['ingredients'] = data['recipeIngredient']
    if 'name' in data.keys():
        cocktail['name'] = data['name']
    
    all_cocktails.append(cocktail)

    driver.quit()
    return links

if __name__ == '__main__':
    base_url = "https://www.esquire.com/food-drink/drinks/recipes"
    base_matcher = re.compile("https://www\.esquire\.com/food-drink/drinks/recipes")
    
    to_visit.add("https://www.esquire.com/food-drink/drinks/recipes/a3764/french-75-drink-recipe/")
    to_visit.add("https://www.esquire.com/cocktail-recipes/")

    while len(to_visit) > 0:
        # Get a URL to visit and mark it as visited
        current_url = to_visit.pop()
        
        if not current_url.startswith("http"):
            print("Ignoring non-web link {}".format(current_url))
            continue

        # Visit the page with selenium
        print("Visiting {}".format(current_url))
        new_links = set(parse_recipe_selenium(current_url))
        visited.add(current_url)
        
        # Remove links that aren't into the base site (don't hit the whole web),
        # and add them to the future list if we haven't seen them yet
        if new_links is not None:
            for url in new_links:
                if url is None:
                    continue
                #Strip #searchoverlay and #sidebar links
                url = url.split("#")[0]
                if not re.match(base_matcher, url):        
                    visited.add(url)
                elif not url in visited:
                    to_visit.add(url)
                
        print("Now have {} to visit.".format(len(to_visit)))

        # Save progress
        with open("esquire.json", 'w') as outfile:
            json.dump(all_cocktails, outfile, indent=4)   

        # Rate limit 
        time.sleep(random.random())
