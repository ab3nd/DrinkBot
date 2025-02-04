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

