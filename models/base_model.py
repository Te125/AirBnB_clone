#!/usr/bin/python3
"""This is the base model for the project"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Base class for other classes, providing common functionality.

    Attributes:
        id (str): A unique identifier for the instance.
        created_at (datetime): The date and time the instance was created.
        updated_at (datetime): The date and time the instance was last updated.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the BaseModel.

        Args:
            *args: Variable-length positional arguments
            (not used in this implementation).
            **kwargs: Variable-length keyword arguments that
            can be used to initialize instance attributes.
        """
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return a string representation of the instance.

        Returns:
            str: A string containing the class name, id,
            and instance attributes.
        """
        class_name = type(self).__name__
        attributes = ', '.join([f'{key}={value}' for
                                key, value in self.__dict__.items()])
        return f"[{class_name}] ({self.id}) {attributes}"

    def save(self):
        """Update the 'updated_at' attribute to the current datetime."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance.

        Returns:
            dict: A dictionary containing instance attributes and metadata.
        """
        class_name = type(self).__name__
        obj_dict = self.__dict__.copy()
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['__class__'] = class_name
        return obj_dict
