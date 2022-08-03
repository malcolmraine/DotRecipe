import json

from models.json_model import JsonModel
from models.quantity import Quantity, Unit
from copy import deepcopy


class Ingredient(JsonModel):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.qty: Quantity = Quantity()
        self.description = ""
        self.category = None

    def __copy__(self):
        result = Ingredient()
        result.qty = deepcopy(self.qty)
        result.description = self.description
        result.category = deepcopy(self.category)
        return result

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "qty": self.qty.as_fraction_string(),
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

    def save(self):
        pass
