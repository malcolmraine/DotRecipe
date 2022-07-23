import json

from data_models.json_model import JsonModel
from data_models.quantity import Quantity, Unit


class Ingredient(JsonModel):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.qty: Quantity = Quantity()
        self.description = ""
        self.category = None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "qty": self.qty
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(self, d):
        self.name = d["name"]
        self.qty.from_nl_string(str(d["qty"]))
        self.description = d["description"]

        return self

    def from_json(self, s):
        obj = json.loads(s)
        self.from_dict(obj)

        return self

    def formatted_amount(self):
        return str(self.qty)
