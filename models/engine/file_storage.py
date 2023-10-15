#!/usr/bin/python3
"""The filestorage module"""

import json
import os
import datetime


class FileStorage:
    """
    This class serializes instances to a JSON file and
    deserializes JSON file to instances.
    """

    def __init__(self):
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if
        the JSON file (__file_path) exists;
        otherwise, do nothing).
        If the file doesn't exist, no exception should be raised.
        """
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name, obj_id = key.split('.')
                    obj_cls = self.classes().get(class_name)
                    if obj_cls:
                        class_name = value.pop("__class__")
                        self.__objects[key] = obj_cls(**value)

    @classmethod
    def classes(cls):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    @classmethod
    def attributes(cls, class_name):
        """Returns the valid attributes and their types
        for the given classname"""
        attributes = {
            "BaseModel": {"id": str, "created_at": datetime.datetime,
                          "updated_at": datetime.datetime},
            "User": {"email": str, "password": str, "first_name":
                     str, "last_name": str},
            "State": {"name": str},
            "City": {"state_id": str, "name": str},
            "Amenity": {"name": str},
            "Place": {"city_id": str, "user_id": str, "name": str,
                      "description": str, "number_rooms": int,
                      "number_bathrooms": int, "max_guest": int,
                      "price_by_night": int, "latitude": float,
                      "longitude": float, "amenity_ids": list},
            "Review": {"place_id": str, "user_id": str, "text": str}
        }
        return attributes.get(class_name, {})

    def close(self):
        """Call reload method for deserializing the JSON file"""
        self.reload()
