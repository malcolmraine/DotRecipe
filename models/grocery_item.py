import json

from models.json_model import JsonModel
from models.quantity import Quantity


class GroceryItem(JsonModel):
    def __init__(self):
        super().__init__()
        self.name = ""
        self._qty = Quantity(1)

    def formatted(self):
        return f"{self._qty.as_fraction_string()} {self.name}"

    def to_dict(self):
        return {"name": self.name, "qty": self._qty.as_fraction_string()}

    def from_json(self, s):
        obj = json.loads(s)
        self.name = obj.get("name", "")
        self._qty.from_nl_string(obj.get("qty", "1"))
