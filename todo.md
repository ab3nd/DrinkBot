# TODO

punchdrink.com
- Figure out their format
    - https://punchdrink.com/tag/cocktail-package/ has a bunch of links to pages like https://punchdrink.com/articles/all-the-ways-paloma-cocktail-recipe/, those go to pages where there are other links 
    - https://punchdrink.com/recipes/dove-dispatch/ is a typical link to a recipe page, it has an ingredient section and a sidebar of related recipes. 
    - Recipe pages have a javascript variable called dataLayer_content that has the recipe in it
    - Recipe itself is in <div class="save-recipe"> as well
    - Sub-ingredients show up in Editor's note, which is annoying, but can still be handled. 
- Write a spider 

cocktaillove.json
- handle ingredients that are count of pieces

cocktail_society.json
- Convert amounts to amounts, not strings

liquor_com_drinks.json
- some ingredients don't have an amount or unit and are like "Garnish: basil leaf"
- "ingred_name": "3 ounces club soda, chilled, to top", and similar, need 3 deleted

mybartender.json
- Split ingredients into amounts, units, names
    - Will be annoying because ingredients that are in dashes or as a garnish have that parenthetically at the end, but some things are just parenthetical asides, like "(for that deep almond taste)". 
    - Some ingredients don't have numbers or units (e.g. "Sugar Cube")
    - "Dashes" can go anywhere "2-3 dashes" vs "2 angostura (dashes)"
- Spacing is uneven ("2 oz" vs "2oz")
- Fractions vs decimals is uneven _even in the same drink_

themixer_drinks.json
- No unit for stuff that had no unit
- Has some 0 amounts, like "0 ice" for stuff that didn't have an amount. 
    - What's a legitimate way to handle this?
- Drop numbers from instructions, they're already in a list

webtender.json
- Split amounts and units
- Fractions into decimal amounts
- Some ingredients got split badly ("1/2 oz Bacardi" as the amount, "151 proof rum" as the ingredient)
- A lot of the cocktails sound fucking terrible, but there are 6215 of them...
- Some empty amounts ("Milk" in the "Colorado Bulldog")

All
- Normalize amounts as much as possible
- rename ingredient components to just "amount", "unit", "name"

# Done

beth_skwarecki_cocktails.json
- Largely done, there are a lot of ingredients that are "to fill"
- There are also ingredients that show up in instructions but not in the ingredient list
    - mint sprigs is a particularly common offender there
- maybe convert things with e.g. egg in to one piece? 

diffords.json
- Done
- Diffords.com may be minable for general class vs specific brand relationships
- The content of this file is very generic, to the point of having "bitter red liquer" instead of "Campari"
- The spider missed a _lot_ of units, if I ever re-crawl that, I need to test more before sending it. 

esquire_drinks.json
- Delete file, all the drinks only have one ingredient

esquire.json
- Done

kindred.json
- Done
- This file has a lot of things like "Ginger liqueur, Domaine de Canton" where the thing before the comma is the general class, and the thing after the comma is a more specific type or brand. 

liquor_com_first_run.json
- Lump in with the other file, then delete

martha_stewart.json
- Done, martha_stewart_cleaned.json is properly split

mr_boston.json
- Done, mr_boston_cleaned.json is properly split

cocktails.txt
- already processed into beth_skwarecki_cocktails.json