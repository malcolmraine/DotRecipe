import os


class JsonModel(object):
    def __init__(self):
        self.file = ""
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        raise NotImplementedError()

    def from_json(self, s):
        raise NotImplementedError()

    def save(self):
        with open(self.file, "w") as file:
            file.write(self.to_json())

    def delete(self):
        os.remove(self.file)


