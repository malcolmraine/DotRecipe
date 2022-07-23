from support.string_helpers import trim, condense_ws
from enum import Enum
from fractions import Fraction
import math


class Unit(Enum):
    TBSP = "tbsp"
    TSP = "tsp"
    CUP = "cup"
    GRAM = "gram"
    POUND = "lb"
    COUNT = "cnt"
    DEFAULT = ""

    def titlecase(self):
        return str(self.value).title()

    def plural(self):
        return self.value + "s"


class UnitFactory(object):
    alternate_spellings = {
        "tablespoon": "tbsp",
        "teaspoon": "tsp",
        "pound": "lb",
        "count": "cnt"
    }

    @staticmethod
    def create(s):
        if s in UnitFactory.alternate_spellings:
            return Unit(UnitFactory.alternate_spellings[s])
        else:
            return Unit(s)


class Quantity(object):
    def __init__(self):
        self._qty = 0
        self._unit: Unit = Unit.DEFAULT
        self.mode = "us"

    def __str__(self):
        return f"{self.float_to_fraction(self._qty)} {self._unit.value}"

    def __mul__(self, other):
        result = Quantity()
        result._qty = self._qty * other
        result._unit = self._unit
        result.mode = self.mode

    @staticmethod
    def fraction_to_float(s: str) -> float:
        all_parts = condense_ws(s).split(" ")
        whole = all_parts[0]

        if len(all_parts) == 1:
            return int(whole)
        else:
            frac = all_parts[1]

        frac_parts = trim(frac.split("/"))

        if 1 >= len(frac_parts) < 2:
            raise Exception("Missing numerator or denominator")
        elif len(frac_parts) == 0:
            decimal_part = 0
        else:
            decimal_part = float(frac_parts[0]) / float(frac_parts[1])

        if whole:
            return float(whole) + decimal_part
        else:
            return decimal_part

    @staticmethod
    def float_to_fraction(f: float) -> str:
        frac, whole = math.modf(f)
        frac = Fraction(frac).limit_denominator()

        if frac == 0:
            return str(int(whole))

        return f"{int(whole)} {frac.numerator}/{frac.denominator}"

    def convert(self, factor):
        return self._qty * factor

    def from_nl_string(self, s: str):
        """
        Parse from a string that follows a set format.

        [int|float]

        :param s:
        :return:
        """
        # Convert all whitespace to " "
        s = s.replace("\t", "")\
            .replace("\n", " ")\
            .replace("\r", " ")

        # Convert to lowercase and split at each space character
        parts = trim(s.lower().split(" "))
        print(parts)

        qty_str = parts[0]

        if len(parts) > 1 and "/" in parts[1]:
            qty_str += " " + parts[1]

        if len(parts) > 2:
            unit_str = " ".join(parts[2:])
        elif not parts[-1].isnumeric():
            unit_str = parts[-1]
        else:
            unit_str = ""

        self._qty = Quantity.fraction_to_float(qty_str)
        self._unit = UnitFactory.create(unit_str)

        return Quantity.fraction_to_float(qty_str), unit_str


# print(Quantity.float_to_fraction(1.25))
# print(Quantity.from_nl_string("1 1/4"))