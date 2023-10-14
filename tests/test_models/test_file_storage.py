#!/usr/bin/python3
""" This is the unittest for the filestorage """

import unittest
import os
from models import storage
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

class TestFileStorage(unittest.TestCase):
    
    def test_file_storage_methods(self):
        """ create a flestorage and basemodel instance """
        storage = FileStorage()
        obj = BaseModel()
        """ test the new method to check if its added right """
        storage.new(obj)
        self.assertTrue("BaseModel.{}".format(obj.id) in storage.all())
        """ test the save method to see if it serilaizes data to json """
        storage.save()
        file_exists = os.path.isfile(storage._FileStorage__file_path)
        self.assertTrue(file_exists)
        """ test the reload method to see that it can load from json """
        storage.reload()
        loaded_obj = storage.all().get("BaseModel.{}".format(obj.id))
        self.assertEqual(loaded_obj.id, obj.id)

    def setUpClass(cls):
        """ create a test JSON file path and initialize FileStorage """
        cls.test_file_path = 'test_file.json'
        cls.storage = FileStorage(cls.test_file_path)

    def tearDownClass(cls):
        """ remove the test JSON file """
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)
        
    def test_initialization(self):
        """ compare the instance attributes """
        self.assertEqual(self.storage._FileStorage__file_path, self.test_file_path)
        self.assertEqual(type(self.storage._FileStorage__objects), dict)

    def test_all_method(self):
        """ test that 'all' method returns an empty dictionary initially """
        all_data = self.storage.all()
        self.assertEqual(all_data, {})
        """ create and save objects """
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj1_key = "{}.{}".format(obj1.__class__.__name__, obj1.id)
        obj2_key = "{}.{}".format(obj2.__class__.__name__, obj2.id)
        self.storage.new(obj1)
        self.storage.new(obj2)
        """ test that 'all' method returns all objects """
        all_data = self.storage.all()
        self.assertEqual(all_data[obj1_key], obj1)
        self.assertEqual(all_data[obj2_key], obj2)

    def test_saving_and_reloading(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        """ save objects to JSON """
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.save()
        """ create a new FileStorage instance """
        new_storage = FileStorage(self.test_file_path)
        """ reload the data """
        new_storage.reload()
        all_data = new_storage.all()
        obj1_key = "{}.{}".format(obj1.__class__.__name__, obj1.id)
        obj2_key = "{}.{}".format(obj2.__class__.__name__, obj2.id)
        self.assertEqual(all_data[obj1_key].id, obj1.id)
        self.assertEqual(all_data[obj2_key].id, obj2.id)

    def test_save_reload_different_file_paths(self):
        """ test saving and reloading from different file paths """
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.save()
        """ create a new FileStorage instance with a different file path """
        new_file_path = 'test_file2.json'
        new_storage = FileStorage(new_file_path)
        new_storage.reload()
        all_data = new_storage.all()

        obj1_key = "{}.{}".format(obj1.__class__.__name__, obj1.id)
        obj2_key = "{}.{}".format(obj2.__class__.__name__, obj2.id)

        self.assertEqual(all_data[obj1_key].id, obj1.id)
        self.assertEqual(all_data[obj2_key].id, obj2.id)
        os.remove(new_file_path)

if __name__ == '__main__':
    unittest.main()
