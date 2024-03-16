import importlib.util
import inspect


def get_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_class_from_module(class_name, module):
    for member in inspect.getmembers(module):
        if not inspect.isclass(member[1]):
            continue
        if member[0] == class_name:
            return member[1]


server_api_domain_py = get_module_from_file(
    'api',
    '..\\..\\api_server\\src\\domain\\api.py')
Error = get_class_from_module('Error', server_api_domain_py)
ImageToTextRequest = get_class_from_module('ImageToTextRequest', server_api_domain_py)
