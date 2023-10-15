#!/usr/bin/python3
""" This program contains the entry point of the command interpreter """
import cmd
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """ this is the initial class for the program """
    prompt = '(hbnb) '
    classes = {'BaseModel': BaseModel,
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
        """ Exits the program """
        return True

    def emptyline(self):
        pass

    def do_create(self, arg):
        """Create a new instance, save it, and print its id"""
        if not arg:
            print("** class name missing **")
            return
        class_name = arg.split()[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = class_name + "." + instance_id
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        if not arg:
            all_instances = storage.all()
        else:
            if arg not in self.classes:
                print("** class doesn't exist **")
                return
            all_instances = {k: v for k, v in storage.all().items() if arg in k}
        print([str(v) for v in all_instances.values()])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in storage.all():
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            attr_name = args[2]
            attr_value = args[3]
            instance = storage.all()[key]
            setattr(instance, attr_name, attr_value)
            instance.save()
        else:
            print("** no instance found **")



if __name__ == '__main__':
    HBNBCommand().cmdloop()
