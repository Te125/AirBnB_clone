#!/usr/bin/python3
""" This test module is the unittest for file_storage """
import unittest
import os
import json
from datetime import datetime
from uuid import uuid4
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.file_path = FileStorage._FileStorage__file_path
        self.storage = FileStorage()
        self.storage.reload()
        self.test_data = {
            'BaseModel.1': {'id': '1', 'name': 'Object 1'},
            'BaseModel.2': {'id': '2', 'name': 'Object 2'},
        }
        self.file_path = 'test_file.json'

    def tearDown(self):
        del self.storage
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_new_and_all(self):
        """ test the new and all methods """
        obj1 = BaseModel(id='1', name='Object 1')
        obj2 = BaseModel(id='2', name='Object 2')
        self.storage.new(obj1)
        self.storage.new(obj2)
        all_objects = self.storage.all()
        self.assertEqual(len(all_objects), 2)
        self.assertIn('BaseModel.1', all_objects)
        self.assertIn('BaseModel.2', all_objects)

    def test_save_and_reload(self):
        """ Test the save and reload methods """
        obj1 = BaseModel(id='1', name='Object 1')
        obj2 = BaseModel(id='2', name='Object 2')
        self.storage.new(obj1)
        self.storage.new(obj2)
        """ check if the json file was created """
        self.assertFalse(os.path.exists(self.file_path))
        """ create a new storage object for testing reload """
        new_storage = FileStorage()
        new_storage.__file_path = self.file_path
        new_storage.reload()
        all_objects = new_storage.all()
        self.assertEqual(len(all_objects), 2)
        self.assertIn('BaseModel.1', all_objects)
        self.assertIn('BaseModel.2', all_objects)


if __name__ == '__main__':
    unittest.main()
