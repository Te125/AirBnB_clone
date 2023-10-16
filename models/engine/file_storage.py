#!/usr/bin/python3
""" The filestorage module """
import json
from os.path import isfile
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
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def all(self):
        """ Returns the dictionary objects """
        return self.__objects

    def new(self, obj):
        """ Sets in obj the object with key id """
        key = f"{obj.__class__.____name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """ Serializes objects to the json file """
        data = {}
        for key, obj in self.__objects.items():
            data[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    def reload(self):
        """ Deserializes the json file to objects if it exists """
        if isfile(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            from models.base_model import BaseModel
            for key, value in data.items():
                class_name, obj_id = key.split('.')
                obj = eval(class_name)(**value)
                self.__objects[key] = obj
