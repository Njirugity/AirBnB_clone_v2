#!/usr/bin/python3
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB"""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
    }

    def emptyline(self):
        """Override to prevent re-executing the last command"""
        pass

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """Exit the program on EOF"""
        print()
        return True

    def do_create(self, args):
        """Create a new instance of a class, save it, and print the id
        Usage: create <ClassName> key1=value1 key2=value2"""
        args = shlex.split(args)
        if not args:
            print("** class name missing **")
            return

        cls_name = args[0]
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for arg in args[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"').replace("_", " ")
                elif value.isdigit():
                    value = int(value)
                elif value.replace(".", "").isdigit():
                    value = float(value)
                kwargs[key] = value

        instance = HBNBCommand.classes[cls_name](**kwargs)
        instance.save()
        print(instance.id)

    def do_show(self, args):
        """Show an instance based on class name and id
        Usage: show <ClassName> <id>"""
        args = shlex.split(args)
        if len(args) < 1:
            print("** class name missing **")
            return

        cls_name = args[0]
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{cls_name}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, args):
        """Delete an instance based on class name and id
        Usage: destroy <ClassName> <id>"""
        args = shlex.split(args)
        if len(args) < 1:
            print("** class name missing **")
            return

        cls_name = args[0]
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{cls_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, args):
        """Show all instances, or all instances of a class
        Usage: all [ClassName]"""
        args = shlex.split(args)
        if args and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        cls_name = args[0] if args else None
        objs = storage.all()
        result = [str(obj) for key, obj in objs.items()
                  if not cls_name or key.startswith(cls_name)]
        print(result)

    def do_update(self, args):
        """Update an instance by adding or updating an attribute
        Usage: update <ClassName> <id> <attribute_name> <attribute_value>
        Or: update <ClassName> <id> {"key": value, ...}"""
        args = shlex.split(args)
        if len(args) < 1:
            print("** class name missing **")
            return

        cls_name = args[0]
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{cls_name}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return

        if len(args) == 2:
            print("** attribute name missing **")
            return

        if len(args) == 3:
            print("** value missing **")
            return

        attr_name, attr_value = args[2], args[3]
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value.strip('"').replace("_", " ")
        elif attr_value.isdigit():
            attr_value = int(attr_value)
        elif attr_value.replace(".", "").isdigit():
            attr_value = float(attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()

    def precmd(self, line):
        """Parse advanced command syntax"""
        if '.' in line and '(' in line and ')' in line:
            try:
                cls_name, rest = line.split('.', 1)
                command, args = rest.split('(', 1)
                args = args.strip(')')
                line = f"{command} {cls_name} {args}"
            except ValueError:
                pass
        return line

if __name__ == "__main__":
    HBNBCommand().cmdloop()

