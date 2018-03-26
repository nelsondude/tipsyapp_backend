import nltk
import string
import copy
import json

from nltk import word_tokenize

import langid
langid.set_languages(['en', 'es'])

import re
regex = re.compile('[%s]' % re.escape(string.punctuation))

from .scrape import scrapeRecipe


def myDeepCopy(a):
    if (isinstance(a, list) or isinstance(a, tuple)):
        return [myDeepCopy(element) for element in a]
    else:
        return copy.copy(a)


class DescriptionLineDetails(object):
    def __init__(self, line, contain_title, proper_nouns, num_key_words, banned, is_layer):
        self.line           = line
        self.contain_title  = contain_title
        self.proper_nouns   = proper_nouns
        self.num_key_words  = num_key_words
        self.banned         = banned
        self.is_layer       = is_layer

def seperate_amount_from_ingredient(line):
    key_words = "or : of ) cup cups dash dashes drop drops oz ozs oz. ml mls ml. pack with teaspoon tsp tablespoon tablespoons teaspoons tbsp part parts bottle bottles gal. gallon gallons pint pints pinch pinches splash splashes".split(" ")
    latest_index = 0
    words = line.split(" ")
    for i in range(len(words)-1):
        word = words[i]
        for j in range(len(key_words)):
            key_word = key_words[j]
            if word.lower().endswith(key_word) or (len(word)>0 and word[-1] in string.digits):
                latest_index = i + 1

    amount = " ".join(words[:latest_index])
    ingredient = " ".join(words[latest_index:])
    if ingredient.lower().startswith('blue cura'):
        ingredient = 'Blue Curacao'
    result = [amount, ingredient.strip()]

    return result

def filter_recipe(recipe):
    return (len(recipe['title'])>2 and
            len(recipe['layers'])>0 and
            len(recipe['layers'][0]['ingredients'])>1 and
            len(recipe['title'].split(" "))<7)


def get_ingredients_from_description(description, title):
    chunks = get_description_chunks(description, title)
    detailed_info = score_chunks(chunks)
    recipes = []
    recipe =    {
                    "title": "",
                    "layers": [],
                    "language": "",
                    "layer": False
                }

    title = ""
    for i in range(len(detailed_info)):
        chunk, score, layer = detailed_info[i]
        # Score cap for valid recipe
        if score > 2:
            current_layer = {
                                "layer_title": layer,
                                "ingredients": [],
                            }
            for j in range(len(chunk)):
                obj = chunk[j]
                if j == 0 and not obj.is_layer:
                    title = obj.line.title()


                if j != 0 and not obj.is_layer:
                    line = myDeepCopy(seperate_amount_from_ingredient(obj.line))
                    if len(line[1])>0 and "=" not in line[1]:
                        current_layer["ingredients"].append(line)

            title = regex.sub('', title)
            if len(recipe['title'])==0:
                recipe['title'] = title

            if len(title)>0 and title != recipe['title']:
                if filter_recipe(recipe):
                    recipes.append(recipe)

                my_new_recipe = {
                    "title": title,
                    "layers": [],
                    "language": "",
                    "layer": False
                }

                recipe = my_new_recipe


            recipe['layers'].append(current_layer)
    # Only add recipe if criterion of filtering met
    if filter_recipe(recipe):
        recipes.append(recipe)
    return recipes

def getDescriptionLine(line, title):

    key_words = "layer splash part oz ml tequila rum vodka gin liqueur grenadine"
    banned_words = "find instagram angeles @ http contact email vlog channel outtakes preparation"

    contain_title = True if title.lower() in line.lower() else False
    text          = word_tokenize(line)
    tagged        = nltk.pos_tag(text)
    proper_nouns  = 0
    num_key_words = 0
    banned        = False
    is_layer      = False

    if 'layer' in line.lower() or (not line.isupper() and line.endswith(':')):
        is_layer = True

    for word, tag in tagged:
        if tag.startswith("NN"): proper_nouns += 1

    for key_word in key_words.split(" "):
        if key_word in line.lower(): num_key_words += 1

    for banned_word in banned_words.split(" "):
        if banned_word in line.lower(): banned = True

    details = DescriptionLineDetails(
                        line,
                        contain_title,
                        proper_nouns,
                        num_key_words,
                        banned,
                        is_layer,


                        )
    return details



def get_description_chunks(description, title):
    chunks = []
    current_chunk = []
    i = 0
    lines = description.splitlines()
    
    for line in lines:
        line = line.strip()

        # Use case for more recent videos that dont have recipe
        tipsy_url = "tipsybartender.com/recipe/"
        if tipsy_url in line:
            urls = list(filter(lambda x: tipsy_url in x, line.split(' ')))
            for url in urls:
                print("URL: ", url)
                url_chunk = []
                more_lines = scrapeRecipe(url).splitlines()
                for mline in more_lines:
                    details = getDescriptionLine(mline, title)
                    url_chunk.append(details)
                chunks.append(url_chunk)

        #     # get the chunk of text here
        details = getDescriptionLine(line, title)
        if ((i == 0) or (len(current_chunk[i-1].line)==0 and len(line)!=0)):
            # if chunk just reset or 
            chunks.append(current_chunk)
            current_chunk = []
            i = 0

        current_chunk.append(details)
        i += 1

    result = myDeepCopy(chunks)
    return result

def score_chunks(chunks):
    # scores = []
    detailed_info = []
    for chunk in chunks:
        layer = ""
        score = 0
        words = 0
        # title = ""
        all_lines = ""

        for obj in chunk:
            if len(obj.line.strip()) == 0: #remove all empty lines in a chunk
                chunk.remove(obj)
                continue
            all_lines = all_lines + obj.line + ' \n'

            if obj.is_layer:
                layer = obj.line

            words += len(obj.line.split(" "))
            score += obj.proper_nouns * 3 #weight for properNOUNd
            score += obj.num_key_words * 15 #weight for keywords
            if obj.contain_title: score += 30 #weight for Title
            if obj.banned: #if any banned words, score is 0
                score = 0
                break

        if words > 0 and score > 0: score = score/words #score per word
        if len(chunk) < 2: score = 0

        if score > 0 and len(all_lines) > 0:
            lang, lang_score = langid.classify(all_lines)
            if lang == 'es':
                score = 0



        detailed_info.append([chunk, score, layer])

    result = myDeepCopy(detailed_info)
    return result