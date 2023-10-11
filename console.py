#!/usr/bin/python3


"""
This module contains the the HBNBCommand class
which implements the cmd.Cmd class
"""


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


class_names = [
    "BaseModel", "User",
    "State", "City",
    "Amenity", "Place",
    "Review"
]


def update_instance(instance, attr, attr_value):
    """ add or update attribute of instance """

    value = getattr(instance, attr, None)
    if value is None:
        setattr(
            instance,
            attr, attr_value.replace('"', "")
        )
    else:
        value_type = type(getattr(instance, attr))
        setattr(instance, attr,
                value_type(attr_value.replace('"', "")))


def update_instance_with_dict(command):
    """ add or update multiple attributes with dict """

    command_list = command[
        command.index("{") + 1:command.index("}")
    ].replace(":", "").split(" ")
    arguments = command[
        :command.index("{")
    ].replace('"', '').replace(", ", "").replace(".update(", " ").split(" ")
    if len(arguments) == 0 or arguments[0] == "":
        print("** class name missing **")
    elif arguments[0] not in class_names:
        print("** class doesn't exist **")
    elif len(arguments) < 2:
        print("** instance id missing **")
    else:
        objects = models.storage.all()
        key = ".".join(arguments)
        if key in objects.keys():
            if len(command_list) == 0:
                print("** attribute name missing **")
            elif len(arguments) % 2 != 0:
                print("** value missing **")
            else:
                instance = objects[key]
                for i in range(0, len(command_list), 2):
                    update_instance(
                        instance,
                        command_list[i].replace("'", "").replace('"', ""),
                        command_list[i + 1]
                    )
                instance.save()
        else:
            print("** no instance found **")


def get_objects(arguments):
    """ get the objects in storage """

    objects = models.storage.all()
    objects_list = []
    for key, value in objects.items():
        if arguments[0] == "":
            objects_list.append(str(value))
            continue
        if arguments[0] == key[:len(arguments[0])]:
            objects_list.append(str(value))
    return objects_list


def get_command(command):
    """ reconstruct the command """

    if command.find("(") + 1 == command.find(")"):
        return "{}".format(command[:command.find(".")])

    return "{} {}".format(
        command[:command.find(".")],
        command[command.find(
            "(") + 1:-1].replace('"', '').replace(",", "")
        )


class HBNBCommand(cmd.Cmd):
    """ This is a commandline interpreter for the AirBnB clone """

    prompt = "(hbnb) "

    def do_update(self, command):
        """ update command's implementation """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in class_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                if len(arguments) < 3:
                    print("** attribute name missing **")
                elif len(arguments) < 4:
                    print("** value missing **")
                else:
                    instance = objects[key]
                    update_instance(instance, arguments[2], arguments[3])
                    instance.save()
            else:
                print("** no instance found **")

    def onecmd(self, command):
        """ handle commands such as User.all(), User.show(), etc """

        c = command.split(".")
        if len(c) > 1:
            func = command[command.index(".") + 1:command.index("(")]
            if func == "all":
                return self.do_all(command[:command.index(".")])
            elif func == "show":
                return self.do_show(get_command(command))
            elif func == "destroy":
                return self.do_destroy(get_command(command))
            elif func == "update":
                if command.find("{") >= 0:
                    update_instance_with_dict(command)
                    return
                else:
                    return self.do_update(get_command(command))
            elif func == "count":
                print(len(get_objects(get_command(command))))
                return
        return super(HBNBCommand, self).onecmd(command)

    def do_all(self, command):
        """ all command's implementation """

        arguments = command.split(" ")

        if arguments[0] != "" and arguments[0] not in class_names:
            print("** class doesn't exist **")
        else:
            print(get_objects(arguments))

    def do_destroy(self, command):
        """ destroy command's implementation """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in class_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                instance = objects[key]
                models.storage.remove(key)
                models.storage.save()
                del instance
            else:
                print("** no instance found **")

    def do_show(self, command):
        """ show command's implementation """

        arguments = command.split(" ")

        if arguments[0] == "":
            print("** class name missing **")
        elif arguments[0] not in class_names:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                print(objects[key])
            else:
                print("** no instance found **")

    def do_create(self, command):
        """ create command's implementation """

        if command == "":
            print("** class name missing **")
        elif command not in class_names:
            print("** class doesn't exist **")
        else:
            if command == class_names[0]:
                instance = BaseModel()
            elif command == class_names[1]:
                instance = User()
            elif command == class_names[2]:
                instance = State()
            elif command == class_names[3]:
                instance = City()
            elif command == class_names[4]:
                instance = Amenity()
            elif command == class_names[5]:
                instance = Place()
            elif command == class_names[6]:
                instance = Review()
            instance.save()
            print(instance.id)

    def do_quit(self, command):
        """ quit command's implementation """

        return True

    def help_quit(self):
        """ quit command's help """

        print('Quit command to exit the program\n')

    def do_EOF(self, command):
        """ EOF command's implementation """

        print()
        return True

    def emptyline(self):
        """ implements what happens when an emptyline is used as command """

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
