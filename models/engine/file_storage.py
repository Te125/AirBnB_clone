#!/usr/bin/python3
""" This class serializes instances to a json file and deserializes json
to instances """
import json
from models.base_model import BaseModel


class FileStorage:
    """ defines path to json file and dict to store objects """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Set obj in objects with the key id """
        FileStorage.__objects = {}
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key not in FileStorage.__objects:
            FileStorage.__objects[key] = obj

    def save(self):
        """ Serialize objects to the JSON file """
        serialized = {}
        for key, obj in FileStorage.__objects.items():
            serialized[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized, file)

    def reload(self):
        """ Deserialize the JSON file into objects if it exists """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                serialized = json.load(file)
                FileStorage.__objects = {}
                for key, data in serialized.items():
                    class_name, obj_id = key.split('.')
                    obj = BaseModel(**data)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            FileStorage.__objects = {}
        except json.decoder.JSONDecodeError:
            FileStorage.__objects = {}
