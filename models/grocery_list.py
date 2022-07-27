import json

from models.json_model import JsonModel
from support.filter_collection import FilterCollection
from models.ingredient import Ingredient


class GroceryList(JsonModel):
    def __init__(self):
        super().__init__()
        self.items = FilterCollection()
        self.file = "resources/grocery_list.json"

    def add_items(self, items):
        for item in items:
            existing_item = self.items.where("name", item.name).first()
            if existing_item is not None:
                existing_item.qty += item.qty
            else:
                self.items.append(item)

    def has_item(self, item):
        return self.items.where("name", item.name).exists()

    def to_dict(self):
        return {
            **self.get_metadata_dict(),
            "items": [item.to_dict() for item in self.items]
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def from_json(self, s):
        d = json.loads((s))
        self.created_at = d["metadata"]["created_at"]
        self.updated_at = d["metadata"]["updated_at"]
        self.items = FilterCollection([Ingredient().from_dict(s) for s in d["items"]])

