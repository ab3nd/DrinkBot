# DrinkBot
Control code and drink planning for a robot that serves booze. 

The .pkl files are python pickle files that the other files work with. 
Since pickle isn't secure, you really shouldn't run the scripts on them unless you feel like taking my word for it that they are fine. 

Parse_drinks.py reads a bunch of html files and creates the pickle files. 
The html files are not available from this repo, because they are the content of [The Webtender](http://www.webtender.com/). 
If you want to download them, you might try [something like this](http://gizmosmith.com/2012/10/09/drinking-with-robots/)

Find_set.py uses the pickle files from parse_drinks.py to generate a list of the ingredients you can use and the drinks that you can make with them. 
For the curious, the set of ingredients that this algorithm finds are vodka, orange juice, cranberry juice, peach schnapps, and everclear. 
The algorithm is greedy. 
It finds the most common ingredient in all drinks, cuts the list of drinks down to those that include the most common ingredient, removes that ingredient, and repeats until either it hits more than five ingredients (my robot only has 5 pumps), or the drink list gets cut down to nothing. 
It is possible that this is not the best algorithim, because, for example, the sum of tequila and rum drinks along with four other ingredients could be more than the total number of vodka drinks with those four other ingredients, but the greedy algorithim wouldn't detect that. 
There are 510 ingredients, and so 510 + (510! / (2! (510 - 2)!)) + (510! / (3! (510 - 3)!)) + (510! / (4! (510 - 4)!)) + (510! / (5! (510 - 5)!)) = 510 + 129795 + 21978620 + 2785790085 + 281921956602 = 284,729,855,612 or about 284 billion combinations of ingredients possible (without duplication, so no cocktail that's 5 instances of vodka). 
It may be that a dynamic programming approach would be more successful, but I haven't determined if this problem has optimal substructure. 
