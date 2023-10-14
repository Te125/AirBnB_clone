#!/usr/bin/python3
""" This is a module containg the Review class """
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review class which inherits the BaseModel """
    place_id = ""
    user_id = ""
    text = ""
