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

    def do_create(self, arg):
        """Create a new instance, save it, and print its id"""
        if not arg:
            print("** class name missing **")
        elif arg not in storage.classes:
            print("** class doesn't exist **")
        else:
            new_instance = storage.classes[arg]()
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
            key = args[0] + "." + args[1]
            """ key = "{}.{}".format(args[0], args[1]) """
            all_objects = storage.all()
            if key in all_objects:
                print(all_objects[key])
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
        """Prints all string representation of all instances
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
            print("** class doesn't exist **") """
        if not arg:
            all_objects = storage.all()
            print([str(obj) for obj in all_objects.values()])
        elif arg in storage.classes:
            all_objects = storage.all()
            filtered_objects = [
                str(obj) for key,
                obj in all_objects.items()
                if key.startswith(arg + ".")
            ]
            print(filtered_objects)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in storage.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            all_objects = storage.all()
            if key not in all_objects:
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                obj = all_objects[key]
                attr_name = args[2]
                value = args[3]
                try:
                    value = eval(value)
                except (NameError, SyntaxError):
                    pass
                setattr(obj, attr_name, value)
                obj.save()

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
