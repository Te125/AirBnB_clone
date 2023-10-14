#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage

class TestConsoleMethods(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        pass  # Clean up if needed

    def test_quit(self):
        with self.subTest():
            self.assertTrue(self.console.onecmd("quit"))
        with self.subTest():
            self.assertTrue(self.console.onecmd("EOF"))

    def test_create(self):
        with self.subTest():
            out = StringIO()
            sys.stdout = out
            self.assertFalse(self.console.onecmd("create"))
            self.assertIn("** class name missing **", out.getvalue())

        with self.subTest():
            out = StringIO()
            sys.stdout = out
            self.assertFalse(self.console.onecmd("create SomeModel"))
            self.assertIn("** class doesn't exist **", out.getvalue())

        with self.subTest():
            self.assertTrue(self.console.onecmd("create BaseModel"))
            objects = storage.all()
            self.assertTrue("BaseModel." + list(objects.keys())[0])
            
            def setUpClass(cls):
        cls.console = console.HBNBCommand()

    def test_create_invalid_class(self):
        result = self.console.onecmd("create InvalidClass")
        self.assertEqual(result, "** class doesn't exist **")

    def test_create_no_class(self):
        result = self.console.onecmd("create")
        self.assertEqual(result, "** class name missing **")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_valid_class(self, mock_stdout):
        result = self.console.onecmd("create BaseModel")
        self.assertTrue(result.strip().isalnum())

    def test_show_invalid_class(self):
        result = self.console.onecmd("show InvalidClass")
        self.assertEqual(result, "** class doesn't exist **")

    def test_show_no_class(self):
        result = self.console.onecmd("show")
        self.assertEqual(result, "** class name missing **")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show_valid_instance(self, mock_stdout):
        self.console.onecmd("create BaseModel")
        result = self.console.onecmd("show BaseModel")
        self.assertNotEqual(result, "** no instance found **")

    def test_show_invalid_instance(self):
        self.console.onecmd("create BaseModel")
        result = self.console.onecmd("show BaseModel 12345")
        self.assertEqual(result, "** no instance found **")

if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
