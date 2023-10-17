#!/usr/bin/python3
""" The filestorage module """
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ defines path to json file and dict to store objects """
    __file_path = "file.json"
    __objects = {}
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity':  Amenity,
        'Place': Place,
        'Review': Review
    }

    def all(self):
        """ Returns the dictionary objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Sets in obj the object with key id """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ Serializes objects to the json file """
        data = FileStorage.__file_path
        new_obj = {
            k: FileStorage.__objects[k].to_dict()
            for k in FileStorage.__objects.keys()
        }
        with open(data, "w") as file:
            json.dump(new_obj, file)
        """objects_dict = {}
        for key, value in FileStorage.__objects.items():
            objects_dict[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, "w") as file:
            json.dump(objects_dict, file)"""

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        try:
            with open(self.__file_path) as file:
                object_json = json.load(file)
                for obj in object_json.values():
                    class_name = obj['__class__']
                    del obj['__class__']
                    self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            return
        """if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r") as file:
            content = file.read()
            if content is None:
                return
            objects_dict = json.loads(content)
            FileStorage.__objects = {}
            for key, value in objects_dict.items():
                class_name = value['__class__']
                del value['__class__']
                cls = FileStorage.classes[class_name]
                FileStorage.__objects[key] = cls(**value)"""
