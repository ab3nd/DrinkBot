# TODO

beth_skwarecki_cocktails.json
- Largely done, there are a lot of ingredients that are "to fill"
- There are also ingredients that show up in instructions but not in the ingredient list
    - mint sprigs is a particularly common offender there
- maybe convert things with e.g. egg in to one piece? 

cocktaillove.json
- This file is the older version, has unicode escapes
- Convert ingredient amounts into numbers
- Split ingredients into amounts, units, names

cocktail_society.json
- Convert amounts to amounts, not strings

cocktails.txt
- already processed into beth_skwarecki_cocktails.json

diffords.json
- Split ingredients into amounts, units, names

esquire_drinks.json
- Delete file, all the drinks only have one ingredient

esquire.json
- Split ingredients into amounts, units, names

kindred.json
- Clean empty instructions elements, newlines, unicode escapes

liquor_com_drinks.json
- Clean newlines, convert ascii fractions into numbers, unicode escapes

liquor_com_first_run.json
- newlines, has some spots where ingredients start with "ounces"
- some ingredients don't have an amount or unit and are like "Garnish: basil leaf"
- "ingred_name": "3 ounces club soda, chilled, to top", and similar, need 3 deleted

martha_stewart.json
- Done, martha_stewart_cleaned.json is properly split

mr_boston.json
- Done, mr_boston_cleaned.json is properly split

mybartender.json
- Split ingredients into amounts, units, names
    - Will be annoying because ingredients that are in dashes or as a garnish have that parenthetically at the end, but some things are just parenthetical asides, like "(for that deep almond taste)". 
    - Some ingredients don't have numbers or units (e.g. "Sugar Cube")
    - "Dashes" can go anywhere "2-3 dashes" vs "2 angostura (dashes)"
- Unicode escapes
- Spacing is uneven ("2 oz" vs "2oz")
- Fractions vs decimals is uneven _even in the same drink_

themixer_drinks.json
- No unit for stuff that had no unit
- Has some 0 amounts, like "0 ice" for stuff that didn't have an amount. 
    - What's a legitimate way to handle this?
- Drop numbers from instructions, they're already in a list
- Unicode escapes

webtender.json
- Split amounts and units
- Fractions into decimal amounts
- Some ingredients got split badly ("1/2 oz Bacardi" as the amount, "151 proof rum" as the ingredient)
- A lot of the cocktails sound fucking terrible, but there are 6215 of them...
- Some empty amounts ("Milk" in the "Colorado Bulldog")

All
- Normalize amounts as much as possible
