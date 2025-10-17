#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base class for all HakkaJson classes.
This class is designed to be memory efficient by setting the __slots__ attribute,
which reduces memory consumption.
"""

import py_hakka_json

json_obj = py_hakka_json.HakkaJsonObject()

# Add some key-value pairs
json_obj["name"] = "John Doe"
json_obj["age"] = 30
json_obj["is_student"] = False

# Access values
name = json_obj["name"]
age = json_obj["age"]
is_student = json_obj["is_student"]

print(f"Name: {name}, Age: {age}, Is Student: {is_student}")

# Iterate over JSON object
for key, value in json_obj.items():
    print(f"{key}: {value}")

print(json_obj, type(json_obj))
print(json_obj["name"], type(json_obj["name"]))
