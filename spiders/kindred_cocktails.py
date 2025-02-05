# https://kindredcocktails.com/
# Each page has links to "recent additions", and the links are all of the form
# https://kindredcocktails.com/cocktail/ followed by some name, so they can be
# filtered pretty easily. 

# The real attack vector here is the ingredients pages. https://kindredcocktails.com/info/ingredients
# has an alphabetical list of ingredients pages. Hit all the ingredient pages, 
# which have URLs like https://kindredcocktails.com/ingredient/allspice. Then 
# find the cocktails on those, especially the link to "Explore more (Ingredient 
# name) cocktails.". That page has more cocktails on it, and is paginated, so it's 
# https://kindredcocktails.com/cocktail?scope=0&ingredient%5B0%5D=Gin and then 
# https://kindredcocktails.com/cocktail?scope=0&ingredient%5B0%5D=Gin&page=5 to 
# get subsequent pages. 

# Plan of attack is to first write an ingredient spider, get all ingredient pages, 
# then write a spider that uses those to get all the cocktails. Pretty standard
# stuff, except I should probably start writing this stuff as reusable components. 

import requests
import json
from bs4 import BeautifulSoup

# Let's start with gin, because no good story ever started with drinking milk. 
start_url = "https://kindredcocktails.com/cocktail?scope=0&ingredient%5B0%5D=Gin"

# Set up a set for cocktails to handle, and cocktails we already handled
cktls_to_do = set()
cktls_done = set()

# Same, but for ingredients
ingrd_to_do = set()
ingrd_done = set()

# I feel like these checks are going to happen a lot...
def add_cocktail_url(url):
    if not url in cktls_done:
        cktls_to_do.add(url)

def add_ingredient_url(url):
    if not url in ingrd_done:
        ingrd_to_do.add(url)

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    return soup

# Given an ingredient page, handle it by hitting "next" until there isn't a next,
# and adding all the relevant cocktails to the cocktail "to do" list 
def parse_ingredient_page(url):
    soup = get_soup(url)

    # Get all the cocktail links, and add them to the todo list
    links = soup.find_all('a')
    # They're all relative, so filter to just get cocktails
    links = filter(lambda x: x['href'].startswith("/cocktail"), links)
    for link in links:
        add_cocktail_url("https://kindredcocktails.com" + link['href'])

    # Get the "next" link, and do a recursive call of this with it.
    next_link = soup.find('a', title="Go to next page")
    if not next_link is None:
        parse_ingredient_page('https://kindredcocktails.com/cocktail' + next_link['href'])
    
def parse_ingredient_base_page(url):
    soup = get_soup(url)
    # Get the link to the full ingredient page
    more_link = soup.find('div', class_="more-link")
    more_url = 'https://kindredcocktails.com' + more_link.find('a')['href']
    parse_ingredient_page(more_url)

# Given a cocktail page url, parse it to produce a cocktail json representation, 
# and add all the ingredients to the ingredients set. Also add all the cocktails
# that are similar to the cocktail "to do" list. 
def parse_cocktail_page(url):
    soup = get_soup(url)
    cocktail = {'ingredients':[], 'instructions':[]}
    ingreds = soup.find_all('div', property='schema:recipeIngredient')
    for ingred in ingreds:
        # Get the quantity and 
        qnty = ingred.find('span', class_='quantity-unit')
        unit = qnty.find('abbr', title=True)
        amount = qnty.text.replace(unit.text, '').strip()
        # Get the name
        name = ingred.find('span', class_='ingredient-name').text
        cocktail['ingredients'].append({"ingred_amount": amount, "ingred_unit": unit['title'], 'ingred_name': name})

    # Get the instructions, this is hacky as fuck. 
    instr = soup.find('div', property="schema:recipeInstructions")
    if not instr is None:
        cocktail['instructions'] = instr.text.split('\n')
    
    # Get the cocktail's name
    name = soup.find('span', property="schema:name", content=True, class_="hidden")['content']
    cocktail['name'] = name
    
    # Get all the cocktail links, and add them to the todo list
    links = soup.find_all('a')
    # They're all relative, so filter to just get cocktails
    for link in filter(lambda x: x['href'].startswith("/cocktail"), links):
        add_cocktail_url("https://kindredcocktails.com" + link['href'])
    for link in filter(lambda x: x['href'].startswith("/ingredient"), links):
        add_ingredient_url("https://kindredcocktails.com" + link['href'])

    return cocktail
    

parse_ingredient_page(start_url)
all_cocktails = []
while len(cktls_to_do) > 0 or len(ingrd_to_do) > 0:
    if len(ingrd_to_do) > 0:
        current_ingredient = ingrd_to_do.pop()
        ingrd_done.add(current_ingredient)
        parse_ingredient_base_page(current_ingredient)

    if len(cktls_to_do) > 0:
        current_cocktail = cktls_to_do.pop()
        cktls_done.add(current_cocktail)
        cktl = parse_cocktail_page(current_cocktail)
        all_cocktails.append(cktl)

        with open('kindred.json', 'w') as outfile:
            json.dump(all_cocktails, outfile, indent=4)

    print(f"Have {len(ingrd_to_do)} ingredients and {len(cktls_to_do)} cocktails to handle")