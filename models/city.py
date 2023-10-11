#!/usr/bin/python3

"""
this is a module containg the City class
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class which inherits the BaseModel
    """

    state_id = ""
    name = ""
