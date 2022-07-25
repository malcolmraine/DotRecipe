from enum import Enum


class Unit(Enum):
    TBSP = "tbsp"
    TSP = "tsp"
    CUP = "cup"
    GRAM = "gram"
    POUND = "lb"
    COUNT = "cnt"
    LITER = "liter"
    GALLON = "gal"
    QUART = "qt"
    KILOGRAM = "kg"
    DEFAULT = ""

    def fullname(self):
        fullnames = {
            "lb": "pound",
            "lbs": "pounds",
            "gr": "pound",
            "lt": "pound",
            "tbsp": "pound",
            "tsp": "pound",
            "cup": "cup",
            "kg": "kilogram",
            "cnt": "count",
        }

        return fullnames.get(self.value, self.value)

    def titlecase(self):
        return str(self.value).title()

    def plural(self):
        plurals = {
            "gram": "grams",
            "lb": "lbs",
            "qt": "qt",
            "kg": "kg",
            "cnt": "cnt",
            "tsp": "tsp",
            "gal": "gal",
            "cup": "cups"
        }
        return plurals.get(self.value, self.value)

    def convert(self, qty, unit):
        ...


class UnitFactory(object):
    alternate_spellings = {
        "tablespoon": "tbsp",
        "tblespoons": "tbsp",
        "tablespn": "tbsp",
        "tablesp": "tbsp",
        "tablespon": "tbsp",
        "tablspoons": "tbsp",
        "talespoons": "tbsp",
        "tablespns": "tbsp",
        "tablesps": "tbsp",
        "tablespons": "tbsp",
        "talespoon": "tbsp",
        "tablepoons": "tbsp",
        "tablepoon": "tbsp",
        "table": "tbsp",
        "tables": "tbsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "teespoon": "tsp",
        "taspoon": "tsp",
        "teapoon": "tsp",
        "teaspon": "tsp",
        "tspoon": "tsp",
        "teespoons": "tsp",
        "taspoons": "tsp",
        "teapoons": "tsp",
        "teaspons": "tsp",
        "tspoons": "tsp",
        "pound": "lb",
        "pnd": "lb",
        "pond": "lb",
        "pund": "lb",
        "pounds": "lb",
        "pnds": "lb",
        "ponds": "lb",
        "punds": "lb",
        "cunt": "cnt",
        "cont": "cnt",
        "count": "cnt",
        "grm": "gram",
        "grams": "gram",
        "gr": "gram",
        "kilogram": "kg",
        "kilograms": "kg",
        "kilo": "kg",
        "kilos": "kg",
        "liter": "liter",
        "liters": "liter",
        "ltr": "liter",
        "gallon": "gal",
        "gallons": "gal",
        "galon": "gal",
        "cp": "cup",
        "cop": "cup",
        "cups": "cup",
        "quart": "qt",
        "quarts": "qt",
        "qwart": "qt",
        "qart": "qt"
    }

    @staticmethod
    def create(s):
        if s in UnitFactory.alternate_spellings:
            return Unit(UnitFactory.alternate_spellings[s])
        else:
            return Unit(s)
