import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
import json
import os
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.recipe_instruction import RecipeInstruction
from recipe_category import RecipeCategory
from random import randint


def resize_image(path: str, save_path: str):
    img = Image.open(path)
    resized = img.resize((480, 320))
    resized.save(save_path)

    return save_path


def unicode_convert(u):
    conversions = {
        "\u00bd": "0.5",
        "\u00bc": "0.25",
        "\u00be": "0.75",
        "\u2009": "."
    }
    _u = u
    for key in conversions:
        _u = _u.replace(key, conversions[key])
        print(key, " - ", _u)

    return _u.replace(".0.", ".")


#page = requests.get('https://www.allrecipes.com/recipe/92462/slow-cooker-texas-pulled-pork/?printview')
#page = requests.get('https://www.allrecipes.com/recipe/7097/chinese-pork-buns-cha-siu-bao/?printview')
#page = requests.get('https://www.allrecipes.com/recipe/246562/thai-cucumber-salad-with-udon-noodles/?printview')
page = requests.get('https://www.allrecipes.com/recipe/8418832/carolina-style-whole-hog-barbecue-pork/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/92462/slow-cooker-texas-pulled-pork/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/92462/slow-cooker-texas-pulled-pork/?printview')

_soup = BeautifulSoup(page.content, 'html.parser')  # Parsing content using beautifulsoup


def all_recipes_parser(soup):
    for script in soup.findAll(type="application/ld+json"):
        obj = json.loads("".join(script.contents))
        for item in obj:
            if item["@type"] == "Recipe":
                recipe = Recipe()
                image = item.get("image").get("url")
                recipe.title = item.get("name", "")

                if image is not None:
                    img_data = requests.get(image).content
                    handler_path = f"{recipe.title.lower().replace(' ', '_')}.jpg"
                    with open(handler_path, 'wb') as handler:
                        handler.write(img_data)
                    resize_image(
                        handler_path,
                        f"../resources/images/{recipe.title.lower().replace(' ', '_')}.jpg"
                    )
                    recipe.image = f"resources/images/{recipe.title.lower().replace(' ', '_')}.jpg"
                    os.remove(handler_path)

                recipe.description = item.get("description", "")
                recipe.source = str(page.url)
                # recipe.est_cook_time = item.get("cookTime", "")
                # recipe.est_prep_time = item.get("prepTime", "")
                recipe.default_serving_qty = item.get("yield", "").split(" ")[0]

                for s in item["recipeIngredient"]:
                    print(s)
                    ingredient = Ingredient()
                    ingredient.qty.from_nl_string(" ".join(unicode_convert(s).split(" ")[:2]))
                    ingredient.name = " ".join(unicode_convert(s).split(" ")[2:])
                    recipe.ingredients.append(ingredient)

                for s in item["recipeInstructions"]:
                    instruction = RecipeInstruction()
                    instruction.text = s["text"]
                    recipe.instructions.append(instruction)

                recipe.file = "../" + str(recipe.dir) + "/" + recipe.default_filename() + ".json"
                recipe.never_saved = False
                recipe.id = randint(10, 1000)
                recipe.primary_category = RecipeCategory.OTHER
                recipe.save()
                break


all_recipes_parser(_soup)