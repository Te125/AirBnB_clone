#!/usr/bin/python3
""" This module contains the the HBNBCommand class
which implements the cmd.Cmd class """
import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
import models


class HBNBCommand(cmd.Cmd):
    """This is a command-line interpreter for the AirBnB clone."""
    
    prompt = "(hbnb) "
    class_names = [
        "BaseModel", "User",
        "State", "City",
        "Amenity", "Place",
        "Review"
    ]
    
    def emptyline(self):
        """Called when an empty line is entered. Does nothing."""
        pass
    
    def do_quit(self, _):
        """Exit the program."""
        return True
    
    def help_quit(self):
        """Display help message for the quit command."""
        print("Quit command to exit the program")
    
    def do_EOF(self, _):
        """Exit the program at EOF (Ctrl+D)."""
        print()
        return True
    
    def do_create(self, command):
        """Create a new instance of a class and save it to the JSON file."""
        if not command:
            print("** class name missing **")
            return
        if command not in HBNBCommand.class_names:
            print("** class doesn't exist **")
            return
        new_instance = eval(command)()
        new_instance.save()
        print(new_instance.id)
    
    def do_show(self, command):
        """Print the string representation of an instance."""
        if not command:
            print("** class name missing **")
            return
        args = command.split()
        if args[0] not in HBNBCommand.class_names:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objects = models.storage.all()
        key = args[0] + "." + args[1]
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")
    
    def do_destroy(self, command):
        """Delete an instance based on the class name and id."""
        if not command:
            print("** class name missing **")
            return
        args = command.split()
        if args[0] not in HBNBCommand.class_names:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objects = models.storage.all()
        key = args[0] + "." + args[1]
        if key in objects:
            del objects[key]
            models.storage.save()
        else:
            print("** no instance found **")
    
    def do_all(self, command):
        """Print all string representations of instances."""
        args = command.split()
        objects = models.storage.all()
        obj_list = []
        for key, value in objects.items():
            if not args or args[0] == value.__class__.__name__:
                obj_list.append(str(value))
        print(obj_list)
    
    def do_update(self, command):
        """Update an instance by adding or updating an attribute."""
        if not command:
            print("** class name missing **")
            return
        args = command.split()
        if args[0] not in HBNBCommand.class_names:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objects = models.storage.all()
        key = args[0] + "." + args[1]
        if key not in objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        instance = objects[key]
        attribute, value = args[2], args[3]
        setattr(instance, attribute, value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
