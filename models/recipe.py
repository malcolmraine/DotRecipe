import json

from models.ingredient import Ingredient
from models.json_model import JsonModel
from models.recipe_instruction import RecipeInstruction
from models.recipe_category import RecipeCategory
from support.filter_collection import FilterCollection


class Recipe(JsonModel):
    def __init__(self):
        self.title = ""
        super().__init__()
        self.description = ""
        self.ingredients = FilterCollection()
        self.est_prep_time = 0
        self.est_cook_time = 0
        self._default_serving_qty = 1
        self.notes = ""
        self.image = ""
        self.instructions = FilterCollection()
        self.source = ""
        self.categories = FilterCollection()
        self.primary_category = None
        self.id = None
        self.dir = "resources/recipes"

    @property
    def default_serving_qty(self):
        return self._default_serving_qty

    @default_serving_qty.setter
    def default_serving_qty(self, value):
        if not value:
            self._default_serving_qty = 1
        else:
            self._default_serving_qty = int(value)

    def default_filename(self):
        if self.title:
            return self.title.lower().replace(" ", "_")
        else:
            return super().default_filename()

    def total_time_required(self):
        return self.est_prep_time + self.est_cook_time

    def to_dict(self) -> dict:
        return {
            **self.get_metadata_dict(),
            # "metadata": {
            #     "created_at": self.created_at,
            #     "updated_at": self.updated_at,
            # },
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.primary_category.value,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "est_prep_time": self.est_prep_time,
            "est_cook_time": self.est_cook_time,
            "default_serving_qty": self.default_serving_qty,
            "notes": self.notes,
            "image": self.image,
            "instructions": [str(instruction) for instruction in self.instructions],
            "source": self.source,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def from_dict(self, d):
        self.created_at = d["metadata"]["created_at"]
        self.updated_at = d["metadata"]["updated_at"]
        self.title = d["title"]
        self.description = d["description"]
        self.primary_category = RecipeCategory(d["category"])
        self.ingredients = [Ingredient().from_dict(s) for s in d["ingredients"]]
        self.est_prep_time = d["est_prep_time"]
        self.est_cook_time = d["est_cook_time"]
        self.default_serving_qty = d["default_serving_qty"]
        self.notes = d["notes"]
        self.image = d["image"]
        self.instructions = [RecipeInstruction(x) for x in d["instructions"]]
        self.source = d["source"]
        self.id = d["id"]
        self.unset_dirty()

    def from_json(self, s):
        self.never_saved = False
        obj = json.loads(s)
        self.from_dict(obj)

        return self
