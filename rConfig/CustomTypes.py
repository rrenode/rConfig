import re

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