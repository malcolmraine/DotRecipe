

class FilterCollection(object):
    def __init__(self, data=None):
        self.data = data if data else []

    def __repr__(self):
        return f"FilterCollection({self.data})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def to_list(self):
        return self.data

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        if isinstance(items, list):
            self.data.extend(items)
        elif isinstance(items, FilterCollection):
            self.data.extend(items.to_list())

    def clear(self):
        self.data.clear()

    def find_first_having(self, attr, value, func=lambda x: x):
        for item in self.data:
            if getattr(item, attr) == value:
                return item

    def find_all_having(self, attr, value, func=lambda x: x):
        results = FilterCollection()
        for item in self.data:
            if getattr(func(item), attr) == value:
                results.append(item)
        return results

    def find_first_equal(self, value, func=lambda x: x):
        for item in self.data:
            if func(item) == value:
                return item
        return None

    def find_all_equal(self, value, func=lambda x: x):
        results = FilterCollection()
        for item in self.data:
            if func(item) == value:
                results.append(item)
        return results

    def find_first_notequal(self, value, func=lambda x: x):
        for item in self.data:
            if func(item) != value:
                return item
        return None

    def find_all_notequal(self, value, func=lambda x: x):
        results = FilterCollection()
        for item in self.data:
            if func(item) != value:
                results.append(item)
        return results

    def not_having(self, attr, value):
        results = FilterCollection()
        for item in self.data:
            if getattr(item, attr) != value:
                results.append(item)

        return results


test = FilterCollection(["one", "two", "three", "four"])
print(test.find_all_equal(3, len))