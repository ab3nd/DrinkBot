Cocktail places to get more data from. 

https://www.allrecipes.com/recipes/133/drinks/cocktails/
Page has a bunch of links in it, of the form https://www.allrecipes.com/bunny-mary-recipe-8739310, as well as a set of links to categories of the form 
https://www.allrecipes.com/recipes/14975/drinks/cocktails/champagne-drinks/. The number changes, so you can't simply substitute the words at the end. 
However, getting every link with the string "drinks/cocktails" in it looks good. 

https://www.thekitchn.com/mixed-drinks-23105533 has drinks with a link that says "go to recipe". There are 13 drinks on the page. 
https://www.thekitchn.com/collection/cocktails has cocktails, but there doesn't appear to be a consistent way to determine if a link is for a cocktail
or for e.g. an article about a cocktail. There recipes do have "Recipes" as text in their link boxes. There are 14 pages of them, so that's a worthwhile
target. 4x18 grid of links on each page, so that's 72 chances to get a recipe per page. https://www.thekitchn.com/collection/cocktails?page=2 is the 
pagination format, should be pretty easy to automate. 

https://liquorlaboratory.com/cocktail-recipes/ has 40 recipes. They have a blog that has some recpies, but there doesn't seem to be a consistent page
structure that indicates the presence of a recipe (e.g. a div class for it). Disappointing in terms of ease of parsing.  

https://www.diffordsguide.com/cocktails I feel like I must have tried this already, need to check the laptop for other files. Cool page, but it's got a
"load more" button and having e.g. selenium drive it sounds... tedious. https://www.diffordsguide.com/cocktails/recipe/30187/continental-negroni is a 
typical cocktail recipe URL, number looks like it can just be incremented but the cocktail bit at the end is needed. They do have an infinite scroll, 
so it might behave better if it was handled in selenium. Scroll ended with a LOT of cocktails listed, so the selenium hacking will be worth it. 
Ingredients are in a table with the class "no-margin ingredients-table", instructions are in a list with the id "method-step-N" for N starting at 1. 

https://www.thecocktailproject.com/search-recipes is paginated like https://www.thecocktailproject.com/search-recipes?page=4, 24 per page, 21 pages. 

Epicurious has cocktails, does not seem to distinguish them from other recipes. 

Bartender.com has two levels of interstitial shit before getting to the drinks. 

https://www.themixer.com/en-us/recipes/ has a "load more" that must be requesting something from an API endpoint, I wonder if I can just MITM the request 
and get all the links that way instead of using selenium. 
