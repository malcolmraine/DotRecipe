from support.string_helpers import trim, condense_ws
from enum import Enum
from fractions import Fraction
import math
from data_models.unit import Unit, UnitFactory


class Quantity(object):
    def __init__(self, value=0):
        self._qty = value
        self._unit: Unit = Unit.DEFAULT
        self.mode = "us"
        self._base_display_str = ""
        self.use_base_display = False

    def __str__(self):
        return f"{self.float_to_fraction(self._qty)} {self._unit.value}"

    def __mul__(self, other):
        result = Quantity()
        result._qty = self._qty * other
        result._unit = self._unit
        result.mode = self.mode

        return result

    def __truediv__(self, other):
        result = Quantity()
        result._qty = self._qty / other
        result._unit = self._unit
        result.mode = self.mode

        return result

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
        return self._qty * factor

    def is_float_str(self, value):
        return isinstance(value, str) and " " not in value and "." in value

    def is_int_str(self, value: str):
        return value.isnumeric()

    def _from_nl_string(self, s: str):
        parts = s.split(" ")
        whole = 0
        decimal = 0
        unit = ""

        for idx, part in enumerate(parts):
            print(part)

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
            elif idx == len(parts) - 1 and "/" not in part and "." not in part and not part.isnumeric():
                unit = part

        self._unit = UnitFactory.create(unit)
        self._qty = whole + decimal
        return self._qty, self._unit.value

    def _from_nl_string_old(self, s: str):
        """
               Parse from a string that follows a set format.

               [int|float]

               :param s:
               :return:
               """
        # Convert all whitespace to " "
        s = s.replace("\t", "") \
            .replace("\n", " ") \
            .replace("\r", " ")
        s = trim(s.lower())
        qty_set = False

        if self.is_float_str(s):
            if not qty_set:
                self._qty = float(s)
                qty_set = True
            self._unit = Unit.DEFAULT
        else:

            # Convert to lowercase and split at each space character
            parts = trim(s.lower().split(" "))
            print(parts)

            qty_str = parts[0]

            if self.is_float_str(qty_str):
                self._qty = float(qty_str)
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
                self._qty = Quantity.fraction_to_float(qty_str)
                qty_set = True

            self._unit = UnitFactory.create(unit_str)

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
        if self._qty > 1:
            unit_str = self._unit.plural()
        else:
            unit_str = self._unit.value

        return f"{self.float_to_fraction(self._qty)} {unit_str}"

    def as_float_string(self):
        return f"{self._qty} {self._unit.value}"

    def get_tooltip(self):
        return f"{self.float_to_fraction(self._qty)} {self._unit.fullname()}"


# test = Quantity()
# print(test.from_nl_string("1.25"))
# # print(test.from_nl_string("1 1/4 tbsp"))
# print(test.as_fraction_string())