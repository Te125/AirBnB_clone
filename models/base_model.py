#!/usr/bin/python3
""" This class module defines all common attributes/methods for all classes """
import uuid
from datetime import datetime
import models


class BaseModel:
    """  initial class base """
    def __init__(self, *args, **kwargs):
        if kwargs:
            """ handle conversion of created-at and updated_at from strings """
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    self.__dict__[key] = datetime.fromisoformat(value)
                elif key != '__class__':
                    self.__dict__[key] = value
        else:
            """ initial class instance """
            self.id = str(uuid.uuid4())
            """ assign string when instance is created """
            self.created_at = datetime.now()
            """ assign with curent datetime """
            self.updated_at = datetime.now()

    def __str__(self):
        """ String instance that should be printed """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ update public instance with current datetime """
        self.updated_at = datetime.now()
        """ save current istance to the storage """
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ returns a dictionary containing all keys/values of dict """
        obj_dict = self.__dict__.copy()
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict
