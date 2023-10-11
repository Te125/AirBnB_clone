#!/usr/bin/python3
""" This is the unittest for the base model"""
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def test_init_id(self):
        """ Check if id is generated and not empty """
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_init_created_updated(self):
        """ Check if created_at and updated_at are datetime objects """
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_save_method(self):
        """ save updates the updated_at attribute """
        obj = BaseModel()
        updated_at_before = obj.updated_at
        obj.save()
        """ save multiple times updates updated_at each time """
        updated_at_after = obj.updated_at
        self.assertNotEqual(updated_at_before, updated_at_after)

    def test_to_dict_method(self):
        """  dictionary returned by to_dict contains the expected keys """
        obj = BaseModel()
        obj_dict = obj.to_dict()
        self.assertIsInstance(obj_dict, dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertIn('created_at', obj_dict)
        self.assertIn('updated_at', obj_dict)
        """ datetime values in the dictionary are formatted correctly """
        self.assertEqual(obj_dict['created_at'], obj.created_at.isoformat())
        self.assertEqual(obj_dict['updated_at'], obj.updated_at.isoformat())

    def test_create_instance_from_dict(self):
        """ Create a dictionary representation of a BaseModel """
        data = {
                'id': 'some_id',
                'created_at': '2023-10-11T10:30:00.123456',
                'updated_at': '2023-10-11T10:45:30.987654',
                'other_attribute': 'some_value'
        }
        """ Create an instance from the dictionary """
        new_instance = BaseModel(**data)
        """ Check created instance attributes and values """
        self.assertEqual(new_instance.id, 'some_id')
        self.assertEqual(new_instance.created_at.isoformat(), '2023-10-11T10:30:00.123456')
        self.assertEqual(new_instance.updated_at.isoformat(), '2023-10-11T10:45:30.987654')
        self.assertEqual(new_instance.other_attribute, 'some_value')

    def test_str_representation(self):
        """  string representation of the object is in the expected format """
        obj = BaseModel()
        str_repr = str(obj)
        self.assertTrue('[BaseModel]' in str_repr)
        self.assertTrue(obj.id in str_repr)

    def test_instance_with_specific_id(self):
        """  instances of BaseModel to verify that their id """
        specific_id = 'test-specific-id'
        obj = BaseModel(id=specific_id)
        self.assertEqual(obj.id, specific_id)

    def test_serialization_and_deserialization(self):
        """ Serialize an instance to a dictionary """
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        """ Compare the attributes """
        self.assertEqual(obj.created_at.isoformat(), new_obj.created_at.isoformat())
        self.assertEqual(obj.created_at.isoformat(), new_obj.created_at.isoformat())


if __name__ == '__main__':
    unittest.main()
