import datetime
import os
import shutil
import json
from uuid import uuid4
import pathlib


class JsonModel(object):
    def __init__(self):
        self.file = str(uuid4()) + ".json"
        self.created_at = None
        self.updated_at = None
        self._dirty = False
        self.dir = pathlib.Path("../resources")
        
    def __setattr__(self, key, value):
        try:
            if not self.__getattribute__("_dirty"):
                super(JsonModel, self).__setattr__("_dirty", True)
        except:
            pass
        super(JsonModel, self).__setattr__(key, value)
        
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

    def save(self):
        if self.created_at is None:
            self.created_at = str(datetime.datetime.now())

        if not self._dirty:
            print("Not dirty - no need to save")
            return

        self.updated_at = str(datetime.datetime.now())

        if os.path.exists(self.file):
            with open(self.file, "r") as file:
                original_contents = file.read()

        with open(self.file, "w") as file:
            try:
                print(self.to_json())
                file.write(self.to_json())
                self.unset_dirty()
            except Exception as e:
                print(e)
                file.truncate()
                file.write(original_contents)

    def delete(self):
        os.remove(self.file)


