import sys
import pkgutil
import importlib
import inspect
import time
import random


def import_all_libraries():
    for e, name, e in pkgutil.iter_modules():
        if name not in sys.modules:
            try:
                importlib.import_module(name)
            except:
                pass

def get_defined_classes(module):
    classes = inspect.getmembers(module, inspect.isclass)
    return [cls_obj for cls_name, cls_obj in classes]


common_default = {int: 0, str: "", bool: False, list: [], dict: {},
                  set: set(), float: 0.0, complex: complex(0, 0),
                  tuple: (), iter: iter(())}


def typer_nightmare(defined_classes):
    some_class = random.choice(defined_classes)
    try:
        sign = inspect.signature(some_class)
        params = sign.parameters

        args = {}
        for name, param in params.items():
            if param.default != inspect.Parameter.empty:
                args[name] = param.default
            else:
                annotation = param.annotation
                if annotation in common_default:
                    args[name] = common_default[annotation]
                else:
                    args[name] = None

        return some_class(**args)

    except:
        try:
            maybe = some_class()
            return maybe
        except:
            return some_class


def main():
    import_all_libraries()
    defined_classes = []
    for module in sys.modules.copy():
        defined_classes.extend(get_defined_classes(sys.modules[module]))
    defined_classes_unique = list(set(defined_classes))
    result = typer_nightmare(defined_classes_unique)
    print(f"And... you get an object of type {type(result)}, here is your object {result}")

main()