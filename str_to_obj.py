import json
from dataclasses import dataclass
from typing import List, Type, TypeVar, Any

T = TypeVar('T')

def from_dict(data: Any, cls: Type[T]) -> T:
    if isinstance(data, list):
        return [from_dict(item, cls.__args__[0]) for item in data]  # type: ignore
    elif isinstance(data, dict):
        if hasattr(cls, '__annotations__'):
            kwargs = {key: from_dict(value, cls.__annotations__[key]) for key, value in data.items()}
            return cls(**kwargs)
        else:
            return data
    else:
        return data

@dataclass
class Address:
    street: str
    city: str

@dataclass
class Person:
    name: str
    age: int
    address: Address
    friends: List[str]

json_str = '''
{
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    },
    "friends": ["Jane", "Doe"]
}
'''

data = json.loads(json_str)
person = from_dict(data, Person)
print("Using dataclass:")
print(person)
print('\n')

# Using Marshmallow library
from marshmallow import Schema, fields, post_load

class Address:
    def __init__(self, street: str, city: str):
        self.street = street
        self.city = city

class Person:
    def __init__(self, name: str, age: int, address: Address, friends: list):
        self.name = name
        self.age = age
        self.address = address
        self.friends = friends

class AddressSchema(Schema):
    street = fields.Str()
    city = fields.Str()

    @post_load
    def make_address(self, data, **kwargs):
        return Address(**data)

class PersonSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    address = fields.Nested(AddressSchema)
    friends = fields.List(fields.Str())

    @post_load
    def make_person(self, data, **kwargs):
        return Person(**data)

json_str = '''
{
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    },
    "friends": ["Jane", "Doe"]
}
'''

data = json.loads(json_str)
person_schema = PersonSchema()
person = person_schema.load(data)
print("Using Marshmallow:")
print(person)
print('\n')

# Using Dataclass-wizard
from dataclasses import dataclass
from dataclass_wizard import fromdict

@dataclass
class Address:
    street: str
    city: str

@dataclass
class Person:
    name: str
    age: int
    address: Address
    friends: list

json_str = '''
{
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    },
    "friends": ["Jane", "Doe"]
}
'''

data = json.loads(json_str)
person = fromdict(Person, data)
print("Using dataclass-wizard:")
print(person)
print('\n')
