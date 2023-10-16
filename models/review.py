#!/usr/bin/python3
from models.base_model import BaseModel


class Review(BaseModel):
    """ class inherts from basemodel """
    place_id = ""
    user_id = ""
    text = ""
