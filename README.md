# py_hakka_json

## Use Cases:
- Memory constrained environments where memory usage is a concern.
- Ideal for scenarios where small objects or string dominate the JSON data.
    - Objects are small. String values are short. Arrays are small.
    - The same values are repeated throughout.
- Suitable for unique integer or double values not exceeding 2^30 (1,073,741,824), including negative values.
    - For example: [1, 1, 2, 3, 3, 3, 6] holds **4** unique values, please do not exceed 2^30 unique values.
- Compliant with the [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259) JSON standard.
- Fully tested on x86_64 and arm64 architectures. Other architectures are conceptually supported but not tested.

## How to build

### Dependencies:
- CMake 3.10 or later is required (a network connection is needed to download dependencies).
    - Automatically downloaded dependencies:
        - Google Test
        - nlohmann/json
        - TartanLlama/expected
        - ICU (International Components for Unicode)
- A C++20 compliant compiler is required.
- [Ninja](https://ninja-build.org/) build system (optional, but recommended).
- [mold](https://github.com/rui314/mold) (optional, but recommended).

### Building the C++ Library:
The C++ library with a C API is located in the `py_hakka_json/_core/src/hakka_json/` submodule. To build the dynamic library, execute the following commands:

```bash
cd py_hakka_json/_core/src/hakka_json/
cmake .. -DCMAKE_BUILD_TYPE=Release -G Ninja -DCMAKE_LINKER=$(which mold) -Wno-dev
ninja
```

#### Running Tests (C++ Library):
To test the C++ library, use the following commands:

```bash
cd py_hakka_json/_core/src/hakka_json/
cmake .. -DCMAKE_BUILD_TYPE=Debug -G Ninja -DCMAKE_LINKER=$(which mold) -DENABLE_TESTS=true -Wno-dev
ninja
ctest
```

### Building the Python Library:
It should build the C++ library first before building the Python library. 
After building the C++ library, the python module can be used directly.

```python
import py_hakka_json

# ...
```

#### Testing the Python Library:
To test the Python library, use the following commands:

```bash
poetry run pytest
```

## How to use

Here is an example of how to use the `py_hakka_json` library in your Python code:

```python
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
```

- Sample output:
```
(hakka-json-py3.13) ➜  py_hakka_json git:(main) ✗ python ./__main__.py
Name: John Doe, Age: 30, Is Student: False
name: John Doe
age: 30
is_student: False
{'name': 'John Doe', 'age': 30, 'is_student': False} <class 'py_hakka_json._hakka_json_object.HakkaJsonObject'>
John Doe <class 'py_hakka_json._hakka_json_string.HakkaJsonString'>
```

## Documentation
```bash
python -m pydoc py_hakka_json
```

## License
Dual-licensed under:
- [Boost Software License 1.0](https://www.boost.org/LICENSE_1_0.txt) OR
- [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

You may choose either license at your option.

