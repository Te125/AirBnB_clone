#!/usr/bin/python3
"""Unittest for the file storage"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()

    def tearDown(self):
        try:
            os.remove(self.storage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_file_storage_initialization(self):
        """Test whether FileStorage initializes correctly"""
        self.assertEqual(self.storage._FileStorage__file_path, "file.json")
        self.assertEqual(self.storage._FileStorage__objects, {})

    def test_file_storage_all(self):
        """Test the 'all' method of FileStorage"""
        data = self.storage.all()
        self.assertIsInstance(data, dict)
        self.assertEqual(data, {})

    def test_file_storage_new(self):
        """Test the 'new' method of FileStorage"""
        class MockModel:
            def __init__(self, id):
                self.id = id
        obj = MockModel(1)
        self.storage.new(obj)
        data = self.storage.all()
        self.assertIn("MockModel.1", data)

    def test_file_storage_save_reload(self):
        """Test the 'save' and 'reload' methods of FileStorage"""
        class MockModel:
            def __init__(self, id):
                self.id = id

            def to_dict(self):
                return {"id": self.id}

        obj = MockModel(1)
        self.storage.new(obj)
        self.storage.save()

        """Create a new storage instance"""
        new_storage = FileStorage()
        new_storage.reload()
        data = new_storage.all()
        self.assertIn("MockModel.1", data)
        self.assertEqual(data["MockModel.1"]["id"], 1)


if __name__ == '__main__':
    unittest.main()
