from support.string_helpers import trim, condense_ws
from enum import Enum
from fractions import Fraction
import math
from models.unit import Unit, UnitFactory
from typing import Union


class Quantity(object):
    def __init__(self, value: Union[int, float] = 0, unit=Unit.DEFAULT):
        self._qty: float = float(value)
        self._unit: Unit = unit
        self.mode: str = "us"
        self._base_display_str: str = ""
        self.use_base_display: bool = False

    def __str__(self):
        converted = convert_up(self)
        return f"{self.float_to_fraction(converted.qty)} {converted.unit.value}"

    def __mul__(self, other):
        if isinstance(other, Quantity):
            result = Quantity(self._qty * other.qty, self._unit)
        else:
            result = Quantity(self._qty * other, self._unit)
        result.mode = self.mode
        return result

    def __add__(self, other):
        if isinstance(other, Quantity):
            result = Quantity(self._qty + other.qty, self._unit)
        else:
            result = Quantity(self._qty + other, self._unit)
        result.mode = self.mode
        return result

    def __sub__(self, other):
        if isinstance(other, Quantity):
            result = Quantity(self._qty - other.qty, self._unit)
        else:
            result = Quantity(self._qty - other, self._unit)
        result.mode = self.mode
        return result

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            result = Quantity(self._qty / other.qty, self._unit)
        else:
            result = Quantity(self._qty / other, self._unit)
        result.mode = self.mode
        return result

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        self._qty = round(value, 2)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = UnitFactory.create(value)

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

        whole_str = str(int(whole)) if int(whole) else ""

        return f"{whole_str} {frac.numerator}/{frac.denominator}"

    def convert(self, factor):
        return self.qty * factor

    @staticmethod
    def is_float_str(s):
        return isinstance(s, str) and " " not in s and "." in s

    @staticmethod
    def is_int_str(s: str):
        return s.isnumeric() and "." not in s

    def _from_nl_string(self, s: str):
        parts = s.split(" ")
        whole = 0
        decimal = 0
        unit = ""

        for idx, part in enumerate(parts):
            if "." in part:
                if part.startswith("."):
                    whole = 0
                    decimal = float("0." + part[1:])
                else:
                    whole, decimal = part.split(".")
                    whole = int(whole)
                    decimal = float("0." + decimal)
            elif part.isnumeric():
                whole = int(part)
            elif "/" in part:
                decimal = int(part.split("/")[0]) / int(part.split("/")[1])
            elif (
                idx == len(parts) - 1
                and "/" not in part
                and "." not in part
                and not part.isnumeric()
            ):
                unit = part

        self.unit = UnitFactory.create(unit)
        self.qty = whole + decimal
        return self.qty, self.unit.value

    def _from_nl_string_old(self, s: str):
        """
        Parse from a string that follows a set format.

        [int|float]

        :param s:
        :return:
        """
        # Convert all whitespace to " "
        s = s.replace("\t", "").replace("\n", " ").replace("\r", " ")
        s = trim(s.lower())
        qty_set = False

        if self.is_float_str(s):
            if not qty_set:
                self.qty = float(s)
                qty_set = True
            self.unit = Unit.DEFAULT
        else:

            # Convert to lowercase and split at each space character
            parts = trim(s.lower().split(" "))
            qty_str = parts[0]

            if self.is_float_str(qty_str):
                self.qty = float(qty_str)
            else:

                if len(parts) > 1 and "/" in parts[1]:
                    qty_str += " " + parts[1]

            if len(parts) > 2:
                unit_str = " ".join(parts[2:])
            elif not parts[-1].isnumeric():
                unit_str = parts[-1]
            else:
                unit_str = ""

            if not qty_set:
                self.qty = Quantity.fraction_to_float(qty_str)
                qty_set = True

            self.unit = UnitFactory.create(unit_str)

            return Quantity.fraction_to_float(qty_str), unit_str

    def from_nl_string(self, s: str):
        self._base_display_str = s
        self.use_base_display = False
        try:
            out = self._from_nl_string(s)
            return out
        except:
            self._base_display_str = s
            self.use_base_display = True
            return self._base_display_str

    def as_fraction_string(self):
        if self.use_base_display:
            return self._base_display_str
        if self.qty > 1:
            unit_str = self.unit.plural()
        else:
            unit_str = self.unit.value

        return f"{self.float_to_fraction(self.qty)} {unit_str}"

    def as_float_string(self):
        return f"{self.qty} {self.unit.value}"

    def get_tooltip(self):
        return f"{self.float_to_fraction(self.qty)} {self.unit.fullname()}"


def convert_up(qty: Quantity):
    conversions = {
        Unit.TSP: (1, 0.33333, Unit.TBSP),
        Unit.TBSP: (4, 0.25, Unit.CUP),
        Unit.CUP: (2, 1, Unit.PINT),
        Unit.PINT: (2, 1, Unit.QUART),
        Unit.QUART: (4, 1, Unit.GALLON),
        Unit.OUNCE: (16, 1, Unit.POUND),
    }
    conversion = conversions.get(qty.unit, None)

    if conversion is None:
        return qty

    if qty.qty < conversion[0]:
        return qty
    else:
        conversion_factor = conversion[1]
        new_qty = qty.qty / conversion[0]
        if new_qty - int(new_qty) == 0:
            return convert_up(Quantity(new_qty * conversion_factor, conversion[2]))
        else:
            return qty


def convert_down(qty: Quantity):
    conversions = {
        Unit.TSP: (0.333, 1, Unit.TBSP),
        Unit.TBSP: (0.25, 4, Unit.CUP),
        Unit.CUP: (1, 2, Unit.PINT),
        Unit.PINT: (1, 2, Unit.QUART),
        Unit.QUART: (1, 4, Unit.GALLON),
        Unit.POUND: (1, 16, Unit.OUNCE),
    }
    conversion = conversions.get(qty.unit, None)

    if conversion is None:
        return qty

    if qty.qty < conversion[0]:
        return qty
    else:
        conversion_factor = conversion[1]
        new_qty = qty.qty / conversion[0]
        if new_qty - int(new_qty) == 0:
            return convert_up(Quantity(new_qty * conversion_factor, conversion[2]))
        else:
            return qty


# test = Quantity(65, Unit.TBSP)
#
# print(convert_up(test))
#


# test = Quantity()
# print(test.from_nl_string("1.25"))
# # print(test.from_nl_string("1 1/4 tbsp"))
# print(test.as_fraction_string())
