from typing import Any, Type

import re
import enum

class rEnum:
    def __init__(self, enum_type: Type[enum.Enum]):
        self.enum_type = enum_type

    def __call__(self, value: Any) -> enum.Enum:
        if isinstance(value, self.enum_type):
            return value
        if isinstance(value, str):
            try:
                return self.enum_type[value]
            except KeyError:
                raise ValueError(f"Invalid value '{value}' for enum {self.enum_type.__name__}")
        raise TypeError(f"Cannot convert {value} to {self.enum_type.__name__}")

    @classmethod
    def __class_getitem__(cls, item: Type[enum.Enum]):
        return cls(item)

class rConstant:
    def __init__(self, value_type: type, value=None):
        if value_type is None:
            raise TypeError("rConstant requires a valid type")
        self.value_type = value_type
        self.value = value

    def __call__(self, value):
        # Handle enums by returning the enum's value directly
        if issubclass(self.value_type, enum.Enum):
            return self.value_type[value].value
        
        # Handle constant-like classes (e.g., LoggingLevels)
        if isinstance(self.value_type, type) and hasattr(self.value_type, value):
            return getattr(self.value_type, value)
        
        # Handle basic types
        return self.value_type(value)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        if isinstance(self.value, int):
            return self.value
        raise TypeError(f"{self.value} cannot be converted to int.")

    def __float__(self):
        if isinstance(self.value, (int, float)):
            return float(self.value)
        raise TypeError(f"{self.value} cannot be converted to float.")
    
    def __repr__(self):
        return f"rConstant[{self.value_type.__name__}] = {self.value}"

    @classmethod
    def __class_getitem__(cls, item: type):
        return cls(item)

class Address:
    def __init__(self, value: str):
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
            raise ValueError(f"Invalid IP address: {value}")
        self.value = value

    def __str__(self):
        return self.value

class Port:
    def __init__(self, value: int):
        if type(value) == str:
            value = int(value)
        if not (0 <= value <= 65535):
            raise ValueError(f"Invalid port number: {value}")
        self.value = value

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)