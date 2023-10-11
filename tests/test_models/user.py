#!/usr/bin/python3

"""
this is a module containg the User class
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class which inherits the BaseModel and
    a user
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
