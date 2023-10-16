#!/usr/bin/python3
from models.base_model import BaseModel


class User(BaseModel):
    """ class inherits from bsemodel """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
