#!/usr/bin/python3
""" This is a module containg the FileStorage class """

import os
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage():
    """ This class serializes instances to a json file and deserializes
    json file to instances """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """  returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = str(type(obj).__name__) + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the json file """
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def deserialize(self, obj_dict):
        """ deserializes the json file """
        class_lookup = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
        }
        for key, obj_dict in obj_dict.items():
            class_name, obj_id = key.split(".")
            class_name = class_lookup.get(class_name, BaseModel)
            self.__objects[key] = class_name(**obj_dict)

    def reload(self):
        """ deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.deserialize(data)
        except FileNotFoundError:
            pass
