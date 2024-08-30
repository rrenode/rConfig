from dotenv import load_dotenv
from os import getenv
from pathlib import Path

import yaml
import inspect
import datetime

from .CustomTypes import Address, Port

load_dotenv()

# Move FIELD_TYPE_CONVERTERS to a separate function to allow extension
def get_field_type_converters(custom_converters=None):
    converters = {
        int: int,
        float: float,
        str: str,
        bool: lambda x: x.lower() in ('true', '1', 'yes'),
        datetime.datetime: lambda value: datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S"),
        Path: lambda value: Path(value),
        Address: lambda value: Address(value),
        Port: lambda value: Port(value)
    }
    
    if custom_converters:
        converters.update(custom_converters)
    
    return converters

def dev_config(cls, custom_converters=None):
    converters = get_field_type_converters(custom_converters)
    for key, field_type in cls.__annotations__.items():
        if str(key).startswith("__"):
            continue
        env_value = getenv(key)
        if env_value is not None and field_type in converters:
            value = converters[field_type](env_value)
            setattr(cls, key, value)
    return cls

@dev_config
class Paths:
    CONFIG_PATH: Path = Path("config.yaml")
    SECRETS_PATH: Path = Path(".secrets")

@dev_config
class DevConfig:
    VERBOSE_DEV: bool = False
    CONFIG_CONTROLLER_LOG: bool = False

def config(cls, custom_converters=None):
    converters = get_field_type_converters(custom_converters)
    config_path = Paths.CONFIG_PATH
    
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        if config_data is None:
            config_data = {}

        class_name = cls.__name__
        class_config = config_data.get(class_name, {})

        for key in vars(cls):
            if key in class_config:
                if str(key).startswith("__"):
                    continue
                value = class_config[key]
                field_type = getattr(cls, key)
                if field_type in converters:
                    value = converters[field_type](value)
                setattr(cls, key, value)
                if DevConfig.VERBOSE_DEV or DevConfig.CONFIG_CONTROLLER_LOG:
                    print(f"Set {cls.__name__}.{key} to {value}")
            elif not str(key).startswith("__"):
                if inspect.isfunction(getattr(cls, key)):
                    continue
                if DevConfig.VERBOSE_DEV or DevConfig.CONFIG_CONTROLLER_LOG:
                    print(f"Using default value for {cls.__name__}.{key}: {getattr(cls, key)}")

    except FileNotFoundError:
        if DevConfig.VERBOSE_DEV or DevConfig.CONFIG_CONTROLLER_LOG:
            print(f"Configuration file '{config_path}' not found. Using default values for {cls.__name__}.")
    
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

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