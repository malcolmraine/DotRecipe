APP_TITLE = "Malcolm & Ellie's Recipes"
APP_ICON = "resources/images/dot.png"

DEFAULT_IMAGE_PATH = "resources/images/chico.png"
RECIPE_IMAGE_SIZE = (480, 320)

DEFAULT_RECIPE_TITLE = "Untitled"
DEFAULT_SERVINGS_COUNT = 1
WEEKDAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

TOOLTIPS = {
    "new_recipe_button": "Add a new recipe",
    "save_recipe_button": "Save the selected recipe",
    "delete_recipe_button": "Delete the selected recipe",
    "add_ingredient_button": "Add an ingredient to the recipe",
    "remove_ingredient_button": "Remove the selected ingredient",
    "add_instruction_button": "Add an instruction to the recipe",
    "remove_instruction_button": "Remove the selected instruction",
    "save_meal_plan_button": "Save this meal plan",
    "reset_meal_plan_button": "Reset this meal plan",
    "default_image": "No image available",
}


def get_tooltip(key: str):
    return TOOLTIPS.get(key, "")
