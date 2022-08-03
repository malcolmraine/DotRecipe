from models.grocery_list import GroceryList
from models.ingredient import Ingredient


class GroceryListHtml(object):
    def __init__(self, grocery_list: GroceryList):
        self.grocery_list = grocery_list
