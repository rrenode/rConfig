from typing import Any, Callable, List
from enum import Enum
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

import yaml
import inspect
import datetime

from .CustomTypes import Address, Port, rEnum, rConstant
from .logging import Logger

load_dotenv()

class ConverterNotFoundError(Exception):
    def __init__(self, field_type):
        self.field_type = field_type
        super().__init__(f"[rConfig] No converter found for field type: {field_type}")

#TODO: Move converters to their own file
# Helper function for converting lists of items to the correct type
def list_converter(item_type) -> Callable[[Any], list]:
    """
    Converts a comma-separated string into a list of the appropriate item type.
    """
    # Get the appropriate item converter based on the item type
    item_converter = get_field_type_converters().get(item_type)
    if not item_converter:
        raise ConverterNotFoundError(item_type)

    def convert(value):
        if isinstance(value, str):
            # If value is a string, split by commas and convert each item
            return [item_converter(v.strip()) for v in value.split(',')]
        elif isinstance(value, list):
            # If value is already a list, apply the converter to each item in the list
            return [item_converter(v) for v in value]
        else:
            # If value is neither a string nor a list, raise an error or handle as needed
            raise ValueError(f"Expected string or list, but got {type(value)}")

    return convert

# Move FIELD_TYPE_CONVERTERS to a separate function to allow extension
def get_field_type_converters(custom_converters=None):
    converters = {
        int: int,
        float: float,
        str: str,
        bool: lambda x: x.lower() in ('true', '1', 'yes'),
        dict: lambda value: value,
        datetime.datetime: lambda value: datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S"),
        Path: lambda value: Path(value),
        Address: lambda value: Address(value),
        Port: lambda value: Port(value)
    }

    def enum_converter(enum_instance: rEnum) -> Callable[[Any], Enum]:
        return lambda value: enum_instance(value)
    
    def rConstant_converter(constant_type: rConstant) -> Callable[[Any], Any]:
        return lambda value: constant_type(value)
    
    converters[rEnum] = enum_converter
    converters[rConstant] = rConstant_converter

    if custom_converters:
        converters.update(custom_converters)
    
    return converters

def dev_config(cls, custom_converters=None):
    ignore_list = ['rSILENT', 'rDEBUG', 'rVERBOSE', 'rCONFIG_PATH', 'rSECRETS_PATH']
    converters = get_field_type_converters(custom_converters)

    for key, field_type in cls.__annotations__.items():
        if str(key).startswith("__"):
            continue
        env_value = getenv(key)
        
        # Handle List types
        if hasattr(field_type, '__origin__') and field_type.__origin__ == List:
            item_type = field_type.__args__[0]  # Get the item type
            list_converter_func = converters.get(List)
            if not list_converter_func:
                raise ConverterNotFoundError(field_type)
        if env_value is None:
            if key in ignore_list:
                continue
            Logger.debug(f"Using default value for dev_config {cls.__name__}.{key}: {getattr(cls, key)}")
        else:
            value = converters[field_type](env_value)
            setattr(cls, key, value)

    return cls

@dev_config
class Paths:
    rCONFIG_PATH: Path = Path("config.yaml")
    rSECRETS_PATH: Path = Path(".secrets")

@dev_config
class rConfig:
    rSILENT: bool = False
    rDEBUG: bool = False
    rVERBOSE: bool = False

def config(cls, custom_converters=None):
    converters = get_field_type_converters(custom_converters)
    config_path = Paths.rCONFIG_PATH
    
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        if config_data is None:
            config_data = {}

        class_name = cls.__name__
        class_config = config_data.get(class_name, {})

        for key, field_type in cls.__annotations__.items():
            if key in class_config:
                if str(key).startswith("__"):
                    continue
                value = class_config.get(key, getattr(cls, key))

                # Handle List types (List[str], List[int], etc.)
                if hasattr(field_type, '__origin__') and (field_type.__origin__ == list or field_type.__origin__ == List):
                    item_type = field_type.__args__[0]  # Get the type of the list's item (e.g., str for List[str])
                    
                    # Directly use the list_converter, passing the item_type
                    value = list_converter(item_type)(value)
                elif isinstance(field_type, rEnum):
                    value = converters[rEnum](field_type)(value)
                elif isinstance(field_type, rConstant):
                    value = converters[rConstant](field_type)(value)
                elif field_type not in converters:
                    raise ConverterNotFoundError(field_type)
                else:
                    value = converters[field_type](value)

                setattr(cls, key, value)
            elif not str(key).startswith("__"):
                if inspect.isfunction(getattr(cls, key)):
                    continue
                if not rConfig.rSILENT:
                    msg = f"Using default value for {cls.__name__}.{key}: {getattr(cls, key)}"
                    Logger.debug(msg)

    except FileNotFoundError:
        Logger.warning(f"Configuration file '{config_path}' not found. Using default values for {cls.__name__}.")
    
    except yaml.YAMLError as e:
        raise ValueError(f"[rConfig] Error parsing YAML file: {e}")

    # Collect methods to be processed as @config_property
    config_properties = []
    for key, method in cls.__dict__.items():
        if callable(method) and getattr(method, '_is_config_property', False):
            config_properties.append((key, method))
    
    # Process the collected methods
    for key, method in config_properties:
        new_key = f"_{key}_internal"
        setattr(cls, new_key, method)
        setattr(cls, key, method(cls))
        
    return cls

def config_property(func):
    func._is_config_property = True
    return func