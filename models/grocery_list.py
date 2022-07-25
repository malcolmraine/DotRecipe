from models.json_model import JsonModel
from support.filter_collection import FilterCollection


class GroceryList(JsonModel):
    def __init__(self):
        super().__init__()
        self.items = FilterCollection()

    def to_dict(self):
        pass

    def from_json(self, s):
        pass
