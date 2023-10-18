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


class_names = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review
}


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
        objects = storage.all()
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
    objects = storage.all()
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
    """ this is the initial class for the program """
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Create a new instance, save it, and print its id"""
        if not arg:
            print("** class name missing **")
        elif arg not in storage.classes:
            print("** class doesn't exist **")
        else:
            new_instance = class_names[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in class_names:
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
        elif args[0] not in HBNBCommand.class_names:
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
        """Prints all string representation of all instances """
        args = arg.split()
        if not arg:
            all_objects = storage.all()
            print([str(obj) for obj in all_objects.values()])
        elif arg in storage.class_names:
            all_objects = storage.all()
            filtered_objects = [
                str(obj) for key,
                obj in all_objects.items()
                if key.startswith(arg + ".")
            ]
            print(filtered_objects)
        else:
            print("** class doesn't exist **")

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
            objects = storage.all()
            key = arguments[0] + "." + arguments[1]
            if key in objects.keys():
                instance = objects[key]
                del objects[key]
                storage.save()
                del instance
            else:
                print("** no instance found **")

    """def do_update(self, arg):
        Updates an instance based on the class name and id
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
                obj.save()"""

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
            objects = storage.all()
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

    """def do_all(self, command):
         all command's implementation
        arguments = command.split(" ")
        if arguments[0] != "" and arguments[0] not in class_names:
            print("** class doesn't exist **")
        else:
            print(get_objects(arguments)) """

    def do_count(self, arg):
        """ retrieve the number of instances of a class """
        arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """ Exit the program """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
