from __future__ import annotations

from copy import deepcopy


class Query(object):
    op_funcs = {
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
    }

    def __init__(self, data: list or FilterCollection):
        self.data = FilterCollection(data)
        self._wheres = []
        self._selects = []

    def _handle_str_op(self, rval, op, lval):
        return self.op_funcs.get(op, lambda x, y: False)(rval, lval)

    def select(self, *args):
        self._selects.extend(args)
        return self

    def where(self, *args):
        self._wheres.append([*args, False])
        return self

    def where_not(self, *args):
        self._wheres.append([*args, True])
        return self

    def _apply_where(self, collection, where: tuple):
        results = FilterCollection()
        invert = where[-1]

        for item in collection:
            include_item = False
            if callable(where[0]):
                rval = where[0](item)
            else:
                rval = getattr(item, where[0])

            if len(where) == 2:
                include_item = bool(rval)
            elif len(where) == 3:
                include_item = rval == where[1]
            elif len(where) == 4:
                include_item = self._handle_str_op(rval, where[1], where[2])

            if invert and not include_item:
                results.append(item)
            elif include_item and not invert:
                results.append(item)

        return results

    def _apply_selects(self, collection: FilterCollection) -> dict or FilterCollection:
        if len(self._selects) == 0:
            return collection

        results = []

        for item in collection:
            result = dict()
            for attr in self._selects:
                result[attr] = getattr(item, attr)

            results.append(result)

        return results

    def get(self) -> FilterCollection:
        results = self.data

        for where in self._wheres:
            results = self._apply_where(results, where)

        return self._apply_selects(results)

    def exists(self) -> bool:
        return not self.get().empty()

    def first(self):
        results = self.get()
        if len(results) > 0:
            return results[0]
        else:
            return None


class FilterCollection(object):
    def __init__(self, data=None):
        if isinstance(data, FilterCollection):
            self.data = data.data
        else:
            self.data = data if data else []

    def __repr__(self):
        return f"FilterCollection({self.data})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        for item in self.data:
            yield item

    def __copy__(self):
        return self.__class__(deepcopy(self.data))

    def __add__(self, other):
        result = self.__copy__()
        result.extend(other)
        return result

    def __truediv__(self, other):
        result = FilterCollection()

        for item in other:
            if item in self:
                result.append(item)

        return result

    def unique(self):
        result = FilterCollection()

        for item in self:
            if item not in result:
                result.append(item)

        return result

    def sort(self, key=None):
        if key is None:
            self.data.sort()
        elif callable(key):
            self.data.sort(key=key)
        else:
            self.data.sort(key=lambda item: getattr(item, key))

    def to_list(self):
        return self.data

    def insert(self, index, item):
        self.data.insert(index, item)

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        if isinstance(items, list):
            self.data.extend(items)
        elif isinstance(items, FilterCollection):
            self.data.extend(items.to_list())

    def clear(self):
        self.data.clear()

    def empty(self):
        return len(self.data) == 0

    def query(self):
        return Query(self)

    def where(self, *args):
        return Query(self).where(*args)

    def where_not(self, *args):
        return Query(self).where_not(*args)

    def max(self, attr, get_item=False):
        if len(self.data) == 0:
            return None

        current_max_item = self.data[0]
        current_max_value = getattr(current_max_item, attr)
        for n in range(1, len(self.data)):
            value = getattr(self.data[n], attr)

            if value > current_max_value:
                current_max_value = value
                current_max_item = self.data[n]

        if get_item:
            return current_max_item
        else:
            return current_max_value


class Test(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age



a = FilterCollection([1, 2, 3, 3])
print(a.unique())