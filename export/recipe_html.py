import dominate
from dominate.tags import *
from models.recipe import Recipe
import pdfkit
import os
import base64


class RecipeHtml(object):
    def __init__(self, recipe: Recipe):
        self.recipe = recipe
        self.doc = dominate.document(title=recipe.title)
        self.stylesheet = "styles.css"
        self.script = ""

    def generate(self):
        with self.doc.head:
            if self.stylesheet:
                link(rel="stylesheet", href=self.stylesheet)

            if self.script:
                script(type="text/javascript", src=self.script)

        with self.doc:
            with div(cls="row"):
                h1(self.recipe.title)
            with div(cls="row"):
                with div(cls="description_col"):
                    p(self.recipe.description)
                with div(cls="image_col"):
                    with open(self.recipe.image, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    # img(src=f"data:image/jpeg;base64,{encoded_string}")
                    img(src=self.recipe.image)

            with div(cls="row"):
                with div(cls="ingredients_col"):
                    hr()
                    with div(id="ingredients_list"):
                        h2("Ingredients")
                        with ol():
                            for ingredient in self.recipe.ingredients:
                                li(
                                    p(
                                        ingredient.qty.as_fraction_string()
                                        + " "
                                        + ingredient.name
                                    )
                                )

                with div(cls="instructions_col"):
                    hr()
                    with div(id="instructions_list"):
                        h2("Instructions")
                        with ol():
                            for instruction in self.recipe.instructions:
                                li(p(instruction))

        return str(self.doc)


r = Recipe()
r.from_file("../resources/recipes/cobb_salad.json")
test = RecipeHtml(r)


with open("test.html", "w") as file:
    value = test.generate()
    file.write(value)

    pdfkit.from_string(value, f"{r.title}.pdf")
    print(r.to_dict())
