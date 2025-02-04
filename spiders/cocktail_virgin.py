# https://cocktailvirgin.blogspot.com/
# Entries are titled with the name of the cocktail, then ingredients, then 
# instructions, then a picture

# Next page link is of the form https://cocktailvirgin.blogspot.com/search?updated-max=2025-01-27T08:00:00-05:00&max-results=9
# but you can set the "max-results" to at least 90, but putting it to 900 doesn't
# pull down the entire blog. 

# <div class='post-body entry-content'> contains the recipe, but the formatting is 
# just <br> tags until you get to the image. The last line before the image is the
# instructions. I'll probably have to do the parse in a pretty loose way and then 
# go through and find the stuff with nonsense ingredients. 