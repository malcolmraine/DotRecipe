from typing import List, Optional
from models.recipe import Recipe
from recipe_category import RecipeCategory


class Collection(object):
    def __init__(self, item_type):
        self._data: List[item_type] = []

    def __contains__(self, item):
        return item in self._data

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        ...

    def __delslice__(self, i, j):
        ...


class RecipeCollection(Collection):
    def __init__(self):
        super().__init__(Recipe)
        self._data: List[Recipe] = [] # Redeclare to get type hints

    def get_titles(self):
        return [recipe.title for recipe in self._data]

    def get_categories(self):
        categories = [recipe.categories for recipe in self._data]
        unique_categories = []

        for category in categories:
            if category not in unique_categories:
                unique_categories.append(category)

        return unique_categories

    def find_by_name(self, name: str) -> Optional[Recipe]:
        for recipe in self._data:
            if recipe.title == name:
                return recipe
        return None

    def get_idx_by_name(self, name: str) -> int:
        for idx, recipe in enumerate(self._data):
            if recipe.title == name:
                return idx
        return -1

    def find_by_category(self, category: RecipeCategory) -> Optional[Recipe]:
        for recipe in self._data:
            if recipe.primary_category == category:
                return recipe
        return None

    def get_idx_by_category(self, category: RecipeCategory) -> int:
        for idx, recipe in enumerate(self._data):
            if recipe.primary_category == category:
                return idx
        return -1

    def get_sorted_list(self, order="asc") -> List[Recipe]:
        ...

    def sort_by_category(self):
        ...

    def sort_by(self, key: str, order="asc"):
        ...

    def clear(self):
        self._data.clear()

    def add(self, recipe: Recipe):
        self._data.append(recipe)

    def remove_by_name(self, name: str) -> bool:
        recipe = self.find_by_name(name)
        self._data.remove(recipe)

    def remove(self, recipe: Recipe) -> bool:
        self._data.remove(recipe)

