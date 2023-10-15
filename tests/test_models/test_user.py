#!/usr/bin/python3
"""Unittests module for the class User."""

import unittest
from models.user import User
from datetime import datetime
from models.base_model import BaseModel


class TestUser(unittest.TestCase):

    def test_user_instance(self):
        """
        Test if a User instance is correctly created.
        """
        user = User()
        self.assertIsInstance(user, User)

    def test_user_attributes(self):
        """
        Test if the User instance has the expected attributes.
        """
        user = User()
        self.assertTrue(hasattr(user, 'id'))
        self.assertTrue(hasattr(user, 'created_at'))
        self.assertTrue(hasattr(user, 'updated_at'))
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

    def test_user_attributes_default_values(self):
        """
        Test if the default values of User attributes are correct.
        """
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_user_attributes_assignment(self):
        """
        Test if the User attributes can be assigned values correctly.
        """
        user = User(email="test@example.com", password="password123",
                    first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    """
        def test_user_str_representation(self):
        Test if the string representation of a User
        instance is correctly formatted.
        user = User(email="test@example.com", password="password123",
                    first_name="John", last_name="Doe")
        user_str = str(user)
        self.assertIsInstance(user_str, str)
        self.assertIn('[User]', user_str)
        self.assertIn(user.id, user_str)
        """

    def test_user_created_at_and_updated_at(self):
        """
        Test if created_at and updated_at are correctly
        initialized as datetime objects
        and if they have the same value upon initialization.
        """
        user = User()
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        self.assertEqual(user.created_at, user.updated_at)

    def test_user_save_updates_updated_at(self):
        """
        Test if the save method updates the updated_at attribute.
        """
        user = User()
        original_updated_at = user.updated_at
        user.save()
        self.assertNotEqual(original_updated_at, user.updated_at)


if __name__ == '__main__':
    unittest.main()
