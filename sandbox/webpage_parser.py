import json
import os
from random import randint

import requests
from PIL import Image
from bs4 import BeautifulSoup

from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipe_instruction import RecipeInstruction
from models.recipe_category import RecipeCategory
from support.string_helpers import *


def resize_image(path: str, save_path: str):
    img = Image.open(path)
    resized = img.resize((480, 320))
    resized.save(save_path)

    return save_path


def convert_fractions(u):
    parts = u.split(" ")
    final = ""
    print(parts)
    for part in parts:
        if "/" in part:
            numerator, denominator = convert_unicode(part).split("/")

            if numerator.isnumeric() and denominator.isnumeric():
                final += str(int(numerator) / int(denominator))
            else:
                final += part
        else:
            final += part
        final += " "
    print(final)
    return final


# page = requests.get('https://www.allrecipes.com/recipe/92462/slow-cooker-texas-pulled-pork/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/7097/chinese-pork-buns-cha-siu-bao/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/246562/thai-cucumber-salad-with-udon-noodles/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/8418832/carolina-style-whole-hog-barbecue-pork/?printview')
# page = requests.get('https://www.allrecipes.com/recipe/21694/marinated-grilled-shrimp/?printview')
page = requests.get(
    "https://www.allrecipes.com/recipe/8437697/california-roll-rice-noodle-bowl/?printview"
)

_soup = BeautifulSoup(
    page.content, "html.parser"
)  # Parsing content using beautifulsoup


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
                    with open(handler_path, "wb") as handler:
                        handler.write(img_data)
                    resize_image(
                        handler_path,
                        f"../resources/img/{recipe.title.lower().replace(' ', '_')}.jpg",
                    )
                    recipe.image = (
                        f"resources/img/{recipe.title.lower().replace(' ', '_')}.jpg"
                    )
                    os.remove(handler_path)

                recipe.description = item.get("description", "")
                recipe.source = str(page.url)
                # recipe.est_cook_time = item.get("cookTime", "")
                # recipe.est_prep_time = item.get("prepTime", "")
                recipe.default_serving_qty = item.get("yield", "").split(" ")[0]

                for s in item["recipeIngredient"]:
                    _s = convert_fractions(convert_unicode(s))
                    print(_s)
                    ingredient = Ingredient()
                    ingredient.qty.from_nl_string(" ".join(_s.split(" ")[:2]))
                    ingredient.name = " ".join(_s.split(" ")[2:])
                    recipe.ingredients.append(ingredient)

                for s in item["recipeInstructions"]:
                    instruction = RecipeInstruction()
                    instruction.text = convert_unicode(s["text"])
                    recipe.instructions.append(instruction)

                recipe.file = (
                    "../" + str(recipe.dir) + "/" + recipe.default_filename() + ".json"
                )
                recipe.never_saved = False
                recipe.id = randint(10, 1000)
                recipe.primary_category = RecipeCategory.OTHER
                recipe.save()
                break


all_recipes_parser(_soup)
