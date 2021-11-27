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

def parse_recipe(html):
    # Time to make the soup!
    bs = BeautifulSoup(html, "lxml")    
    
    recipe = {}

    # Get the drink name... more or less. Fucking Esquire doesn't put the 
    # title of the drink in the page. 
    try:
        title = bs.find("h1", {"class":"content-hed recipe-hed"}).text
        recipe["name"] = title
    except AttributeError:
        print("No title, returning...")
        return

    # Get the ingredients out of the soup 
    ingredients = bs.find("div", {"class":"ingredients"})
    ingred_list = []
    for ingredient in ingredients.findAll("div", {"class":"ingredient-item"}):
        try:
            amount = ingredient.find("span", {"class":"ingredient-amount"}).text
        except AttributeError:
            amount = ""
        
        ingred = ingredient.find("span", {"class":"ingredient-description"}).text
        ingred_list.append({"ingred_name": ingred, "ingred_amount": amount})
    recipe["ingredients"] = ingred_list

    # Get the directions 
    instructions = bs.find("div", {"class":"directions"})
    steps = []
    for step in instructions.findAll("li"):
        steps.append(step.text)
    recipe["instructions"] = steps

    with open("esquire_drinks.json", "a") as outfile:
        outfile.write("{}\n".format(json.dumps(recipe)))

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
    
    # Get the title of the page
    try:
        title = driver.find_element_by_xpath("//h1[@class='content-hed recipe-hed']").text
        recipe["name"] = title
    except NoSuchElementException:
        print("No title, returning...")
        driver.quit()
        return links

    # Get the drink ingredients
    ingredients = driver.find_element_by_xpath("//div[@class='ingredients']")
    ingred_list = []
    for ingredient in ingredients.find_elements_by_xpath("//div[@class='ingredient-item']"):
        try:
            amount = ingredient.find_element_by_xpath("//span[@class='ingredient-amount']").text
        except NoSuchElementException:
            amount = ""
        
        ingred = ingredient.find_element_by_xpath("//span[@class='ingredient-description']").text
        ingred_list.append({"ingred_name": ingred, "ingred_amount": amount})
    recipe["ingredients"] = ingred_list

    # Get the directions 
    instructions = ingredient.find_element_by_xpath("//div[@class='directions']")
    steps = []
    for step in instructions.find_elements_by_tag_name("li"):
        steps.append(step.text)
    recipe["instructions"] = steps

    with open("esquire_drinks.json", "a") as outfile:
        outfile.write("{}\n".format(json.dumps(recipe)))

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

        # Get the HTML for the current page
        print("Visiting {}".format(current_url))
        new_links = set(parse_recipe_selenium(current_url))
        visited.add(current_url)
        
        # Remove links that aren't into the base site (don't hit the whole web),
        # and add them to the future list if we haven't seen them yet
        if new_links is not None:
            for url in new_links:
                #Strip #searchoverlay and #sidebar links
                url = url.split("#")[0]
                if not re.match(base_matcher, url):        
                    visited.add(url)
                elif not url in visited:
                    to_visit.add(url)
                
        print("Now have {} to visit.".format(len(to_visit)))
        
        # Rate limit 
        time.sleep(random.random())
