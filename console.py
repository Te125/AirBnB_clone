#!/usr/bin/python3
""" Entry point of the command interpreter """
import cmd
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


class HBNBCommand(cmd.Cmd):
    """ this is the initial class for the program """
    prompt = '(hbnb) '
    classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
    }

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, arg):
        """ Exit the program """
        return True

    def emptyline(self):
        """ Do nothing """
        pass

    def do_create(self, arg):
        """Create a new instance, save it, and print its id"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.classes[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            objects = storage.all()
            if key in objects:
                print(objects()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            objects = storage.all()
            if key in objects:
                objects.pop(key)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        objects = storage.all()
        if not args:
            print([str(obj) for obj in objects.values()])
        elif args[0] in HBNBCommand.classes:
            print(
                [str(obj) for key,
                    obj in objects.items()
                    if key.split('.')[0] == args[0]]
            )
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            objects = storage.all()
            if key in objects:
                obj = objects[key]
                attr_name = args[2]
                attr_value = args[3]
                try:
                    attr_value = eval(attr_value)
                    setattr(obj, attr_name, attr_value)
                    obj.save()
                except (SyntaxError, NameError):
                    pass
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
