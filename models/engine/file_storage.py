#!/usr/bin/python3
""" This is a module containg the FileStorage class """

import os
import json
from datetime import datetime
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

    def remove(self, key):
        """ removes obj from __objects using the key <obj class name>.id """
        self.__objects.pop(key)

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        with open(self.__file_path, "w") as file:
            objects_dict = {}
            for key, value in self.__objects.items():
                objects_dict[key] = self.__objects[key].to_dict()
            json.dump(objects_dict, file)

    def reload(self):
        """ deserializes the JSON file to __objects """
        if not os.path.exists(self.__file_path):
            return
        with open(self.__file_path, "r") as file:
            content = file.read()
            if content is None:
                return
            objects_dict = json.loads(content)
            self.__objects = {}
            for key, value in objects_dict.items():
                if "User" in key:
                    self.__objects[key] = User(**objects_dict[key])
                    continue
                elif "State" in key:
                    self.__objects[key] = State(**objects_dict[key])
                    continue
                elif "City" in key:
                    self.__objects[key] = City(**objects_dict[key])
                    continue
                elif "Place" in key:
                    self.__objects[key] = Place(**objects_dict[key])
                    continue
                elif "Amenity" in key:
                    self.__objects[key] = Amenity(**objects_dict[key])
                    continue
                elif "Review" in key:
                    self.__objects[key] = Review(**objects_dict[key])
                    continue
                self.__objects[key] = BaseModel(**objects_dict[key])
