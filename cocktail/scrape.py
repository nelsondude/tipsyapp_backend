from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError


quote_page = "https://tipsybartender.com/recipe/blonde-headed-slut-shot/"



def scrapeRecipe(url="https://tipsybartender.com/recipe/blonde-headed-slut-shot/"):
	req = Request(url, headers={'User-Agent': "Chrome 41.0.2228.0"})
	try:
		page =  urlopen(req)
	except HTTPError:
		return ''
	soup = BeautifulSoup(page, 'html.parser')
	full_recipe = soup.find('span', attrs={'itemprop': 'recipeInstructions'})
	if full_recipe:
		ingredients = full_recipe.find('p')
		if ingredients:
			return ingredients.get_text(separator="\n")
	return ''