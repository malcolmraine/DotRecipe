import datetime
import json
import os
import pathlib
from uuid import uuid4


class JsonModel(object):
    def __init__(self):
        self.file = self.default_filename() + ".json"
        self.created_at = None
        self.updated_at = None
        self._dirty = False
        self.dir = pathlib.Path("../resources")
        self.never_saved = True

    def default_filename(self):
        return str(uuid4())

    def __setattr__(self, key, value):
        try:
            if not self.__getattribute__("_dirty"):
                super(JsonModel, self).__setattr__("_dirty", True)
        except:
            pass
        super(JsonModel, self).__setattr__(key, value)

    def get_metadata_dict(self):
        return {
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }
        }

    def set_dirty(self):
        super(JsonModel, self).__setattr__("_dirty", True)

    def unset_dirty(self):
        super(JsonModel, self).__setattr__("_dirty", False)

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        raise json.dumps(self.to_dict(), indent=4)

    def from_json(self, s):
        raise NotImplementedError()

    def from_file(self, file):
        with open(file, "r") as f:
            self.file = file
            self.from_json(f.read())

    def save(self):
        if self.created_at is None:
            self.created_at = str(datetime.datetime.now())

        if not self._dirty:
            print("Not dirty - no need to save")
            return

        self.updated_at = str(datetime.datetime.now())
        original_contents = ""

        if self.never_saved and len(self.file) == 0:
            self.file = str(self.dir) + "/" + self.default_filename() + ".json"

        if os.path.exists(self.file):
            with open(self.file, "r") as file:
                original_contents = file.read()

        with open(self.file, "w") as file:
            try:
                file.write(self.to_json())
                self.unset_dirty()
            except Exception as e:
                print(e)
                file.truncate()
                file.write(original_contents)

    def delete(self):
        os.remove(self.file)
