#!/usr/bin/python3
""" This is the base model for the project """
import uuid
from datetime import datetime


class BaseModel:
    """ initial class base """
    def __init__(self, *args, **kwargs):
        """ Initialize a new instance """
        if kwargs:
            """ handle conversion of created_at and updated_at from strings """
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            """ initial class nstance """
            self.id = str(uuid.uuid4())
            """ assign string when instance is created """
            self.created_at = datetime.now()
            """ assigne with cuurent datetime """
            self.updated_at = datetime.now()

    def __str__(self):
        """ String instance that should be printed """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """Update the 'updated_at' attribute to the current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """ return a dict containing all key/values of dict """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
