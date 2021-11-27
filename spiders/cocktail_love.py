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

# Computer, take the wheel!
d = webdriver.Firefox()
d.set_page_load_timeout(10)

d.get("https://www.cocktaillove.com/recipes/")

# Let it load
time.sleep(0.5 + random.random()*2)
WebDriverWait(d,3).until(lambda driver: driver.execute_script("return (document.readyState == 'complete')"))

#Hit the list button
button = d.find_element_by_xpath("//button[@data-id='basic-list']")
button.click()
WebDriverWait(d,3).until(lambda driver: driver.execute_script("return (document.readyState == 'complete')"))

#Get the whole list
recipe_list = d.find_element_by_id("recipe-matches")
recipes = recipe_list.find_elements_by_tag_name('a')
urls = []
for recipe in recipes:
    urls.append(recipe.get_attribute('href'))

#Ok, now we just have a straight list of all the drink URLs. 
for url in urls:
    d.get(url)
    time.sleep(0.5 + random.random()*2)
    WebDriverWait(d,3).until(lambda driver: driver.execute_script("return (document.readyState == 'complete')"))

    print("Handling {}".format(url))
    # Get the name of the drink
    drink_name = d.find_element_by_xpath("//h1[@class='recipe-name']").text
    
    # Get the ingredients
    ing_list = d.find_element_by_xpath("//dl[@class='ingredient-list']")
    amounts = ing_list.find_elements_by_xpath("//dt[@class='ingredient-amount']")
    ingredients = ing_list.find_elements_by_tag_name('dd')
    ing_list = ["{} {}".format(a, b) for a, b in zip([amt.text for amt in amounts], [ing.text for ing in ingredients])]
    
    # Get the directions
    inst_list = d.find_element_by_xpath("//ol[@class='recipe-steps mb-6']")
    steps = [step.text for step in inst_list.find_elements_by_tag_name('li')]
    
    recipe = {"name": drink_name, "ingredients": ing_list, "instructions": steps }
    with open("cocktaillove.json", 'a') as outfile:
        outfile.write("{}\n".format(json.dumps(recipe)))

d.quit()
