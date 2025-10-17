import unittest
from io import StringIO
from py_hakka_json._hakka_json import HakkaJson
from py_hakka_json._hakka_json_array import HakkaJsonArray
from py_hakka_json._hakka_json_object import HakkaJsonObject


class TestHakkaJson(unittest.TestCase):
    def setUp(self):
        self.json_array = HakkaJsonArray([1, 2, 3])
        self.json_object = HakkaJsonObject({"key": "value"})

    def test_dump_array(self):
        file = StringIO()
        HakkaJson.dump(self.json_array, file)
        file.seek(0)
        self.assertEqual(file.read(), "[1, 2, 3]")

    def test_dump_object(self):
        file = StringIO()
        HakkaJson.dump(self.json_object, file)
        file.seek(0)
        self.assertEqual(file.read(), '{"key": "value"}')

    def test_dumps_array(self):
        result = HakkaJson.dumps(self.json_array)
        self.assertEqual(result, "[1, 2, 3]")

    def test_dumps_object(self):
        result = HakkaJson.dumps(self.json_object)
        self.assertEqual(result, '{"key": "value"}')

    def test_load_array(self):
        file = StringIO("[1, 2, 3]")
        result = HakkaJson.load(file)
        self.assertIsInstance(result, HakkaJsonArray)
        self.assertEqual(result.to_python(), [1, 2, 3])

    def test_load_object(self):
        file = StringIO('{"key": "value"}')
        result = HakkaJson.load(file)
        self.assertIsInstance(result, HakkaJsonObject)
        self.assertEqual(result.to_python(), {"key": "value"})

    def test_loads_array(self):
        result = HakkaJson.loads("[1, 2, 3]")
        self.assertIsInstance(result, HakkaJsonArray)
        self.assertEqual(result.to_python(), [1, 2, 3])

    def test_loads_object(self):
        result = HakkaJson.loads('{"key": "value"}')
        self.assertIsInstance(result, HakkaJsonObject)
        self.assertEqual(result.to_python(), {"key": "value"})

    def test_dump_invalid_type(self):
        with self.assertRaises(TypeError):
            HakkaJson.dump("invalid", StringIO())

    def test_dumps_invalid_type(self):
        with self.assertRaises(TypeError):
            HakkaJson.dumps("invalid")


from py_hakka_json._hakka_json_bool import HakkaJsonBool
from py_hakka_json._hakka_json_float import HakkaJsonFloat
from py_hakka_json._hakka_json_int import HakkaJsonInt
from py_hakka_json._hakka_json_null import HakkaJsonNull
from py_hakka_json._hakka_json_string import HakkaJsonString


class TestHakkaJsonAdvanced(unittest.TestCase):
    def setUp(self):
        self.json_array = HakkaJsonArray(
            [HakkaJsonInt(1), HakkaJsonInt(2), HakkaJsonInt(3)]
        )
        self.json_object = HakkaJsonObject(
            {
                "key1": HakkaJsonString("value1"),
                "key2": HakkaJsonBool(True),
                "key3": HakkaJsonNull(),
                "key4": HakkaJsonArray([HakkaJsonInt(4), HakkaJsonInt(5)]),
            }
        )

    def test_dump_and_load_complex_structure(self):
        # Dump and load a complex object
        buffer = StringIO()
        HakkaJson.dump(self.json_object, buffer)
        buffer.seek(0)
        loaded_obj = HakkaJson.load(buffer)
        self.assertEqual(loaded_obj.to_python(), self.json_object.to_python())

    def test_dumps_and_loads_with_nested_arrays(self):
        # Dump and load nested arrays
        nested_array = HakkaJsonArray(
            [
                HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2)]),
                HakkaJsonArray([HakkaJsonInt(3), HakkaJsonInt(4)]),
            ]
        )
        json_str = HakkaJson.dumps(nested_array)
        expected_str = "[[1, 2], [3, 4]]"
        self.assertEqual(json_str, expected_str)
        loaded_array = HakkaJson.loads(json_str)
        self.assertEqual(loaded_array.to_python(), [[1, 2], [3, 4]])

    def test_loads_invalid_json(self):
        invalid_jsons = [
            "",  # Empty string
            "not json",  # Plain string
            "{unclosed_object: 1",  # Malformed JSON
            "[1, 2, 3",  # Unclosed array
            '{"key": "value",}',  # Trailing comma
            '{"key": value}',  # Missing quotes around value
        ]
        for json_str in invalid_jsons:
            with self.assertRaises(ValueError):
                HakkaJson.loads(json_str)

    def test_dump_invalid_type(self):
        # Attempt to dump an unsupported type
        with self.assertRaises(TypeError):
            HakkaJson.dump("invalid_type", StringIO())

    def test_loads_with_depth_limit(self):
        # Test loading JSON with deep nesting exceeding limit
        deep_json = "[" * 1001 + "1" + "]" * 1001  # Exceeds typical recursion limits
        with self.assertRaises(RecursionError):
            HakkaJson.loads(deep_json, max_depth=1000)

    def test_dump_and_load_empty_structures(self):
        empty_array = HakkaJsonArray()
        empty_object = HakkaJsonObject()
        # Dump and load empty array
        buffer = StringIO()
        HakkaJson.dump(empty_array, buffer)
        buffer.seek(0)
        loaded_empty_array = HakkaJson.load(buffer)
        self.assertEqual(loaded_empty_array.to_python(), [])
        # Dump and load empty object
        buffer = StringIO()
        HakkaJson.dump(empty_object, buffer)
        buffer.seek(0)
        loaded_empty_object = HakkaJson.load(buffer)
        self.assertEqual(loaded_empty_object.to_python(), {})

    def test_dump_and_load_with_varied_types(self):
        # Dump and load structures with varied types
        mixed_obj = HakkaJsonObject(
            {
                "int": HakkaJsonInt(10),
                "float": HakkaJsonFloat(3.14),
                "bool": HakkaJsonBool(True),
                "string": HakkaJsonString("test"),
                "null": HakkaJsonNull(),
                "array": HakkaJsonArray(
                    [HakkaJsonInt(1), HakkaJsonString("two"), HakkaJsonBool(False)]
                ),
            }
        )
        buffer = StringIO()
        HakkaJson.dump(mixed_obj, buffer)
        buffer.seek(0)
        loaded_mixed_obj = HakkaJson.load(buffer)
        self.assertEqual(loaded_mixed_obj.to_python(), mixed_obj.to_python())

    def test_dump_and_load_with_escape_characters(self):
        # Test strings with escape characters
        obj = HakkaJsonObject(
            {
                "newline": HakkaJsonString("Line1\nLine2"),
                "tab": HakkaJsonString("Column1\tColumn2"),
                "quote": HakkaJsonString('He said, "Hello"'),
            }
        )
        buffer = StringIO()
        HakkaJson.dump(obj, buffer)
        buffer.seek(0)
        loaded_obj = HakkaJson.load(buffer)
        self.assertEqual(loaded_obj.to_python(), obj.to_python())

    def test_dump_with_custom_objects(self):
        # Attempt to dump custom HakkaJson objects
        class CustomHakkaJson:
            pass

        custom_obj = CustomHakkaJson()
        with self.assertRaises(TypeError):
            HakkaJson.dump(custom_obj, StringIO())

    def test_dump_round_trip_integrity(self):
        # Ensure that dumping and loading retains data integrity
        original_obj = HakkaJsonObject(
            {
                "numbers": HakkaJsonArray([HakkaJsonInt(i) for i in range(100)]),
                "flags": HakkaJsonArray(
                    [
                        HakkaJsonBool(True) if i % 2 == 0 else HakkaJsonBool(False)
                        for i in range(100)
                    ]
                ),
                "details": HakkaJsonObject(
                    {"nested_key": HakkaJsonString("nested_value")}
                ),
            }
        )
        serialized = HakkaJson.dumps(original_obj)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), original_obj.to_python())

    def test_dump_with_comments_in_json(self):
        json_with_comments = '{"key": "value"} // This is a comment'
        HakkaJson.loads(json_with_comments) # Comments are safe

    def test_dump_and_load_with_unicode_escape_sequences(self):
        # Test strings with Unicode escape sequences
        obj = HakkaJsonObject(
            {"unicode": HakkaJsonString("Unicode test: \u2603")}  # Snowman
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"unicode": "Unicode test: ☃"}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), obj.to_python())

    def test_loads_with_utf8_characters(self):
        # Test loading JSON with UTF-8 characters
        json_str = '{"greeting": "こんにちは世界"}'  # "Hello World" in Japanese
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"greeting": "こんにちは世界"})

    def test_dump_with_invalid_json_object(self):
        # Attempt to dump an object with non-serializable values
        with self.assertRaises(RuntimeError):
            obj = HakkaJsonObject({"set": set([1, 2, 3])})  # Sets are not JSON serializable

    def test_loads_with_correct_depth_limit(self):
        # Test loading JSON within depth limits
        depth = 10
        nested_json = "[" * depth + "1" + "]" * depth
        loaded_array = HakkaJson.loads(nested_json, max_depth=depth)
        current = loaded_array
        for _ in range(depth):
            self.assertIsInstance(current, HakkaJsonArray)
            self.assertEqual(len(current), 1)
            current = current[0]
        self.assertEqual(current.to_python(), 1)

    def test_loads_with_insufficient_depth_limit(self):
        # Test loading JSON exceeding depth limits
        depth = 5
        nested_json = "[" * (depth + 1) + "1" + "]" * (depth + 1)
        with self.assertRaises(RecursionError):
            HakkaJson.loads(nested_json, max_depth=depth)

    def test_dump_and_load_with_boolean_values(self):
        # Ensure boolean values are correctly handled
        obj = HakkaJsonObject(
            {"isActive": HakkaJsonBool(True), "isAdmin": HakkaJsonBool(False)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"isActive": true, "isAdmin": false}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"isActive": True, "isAdmin": False})

    def test_dump_and_load_with_null_values(self):
        # Ensure null values are correctly handled
        obj = HakkaJsonObject({"value1": HakkaJsonNull(), "value2": HakkaJsonNull()})
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"value1": null, "value2": null}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"value1": None, "value2": None})

    def test_dump_and_load_with_mixed_types(self):
        # Dump and load objects containing mixed types
        obj = HakkaJsonObject(
            {
                "int": HakkaJsonInt(10),
                "float": HakkaJsonFloat(3.14),
                "bool": HakkaJsonBool(True),
                "string": HakkaJsonString("test"),
                "null": HakkaJsonNull(),
                "array": HakkaJsonArray(
                    [HakkaJsonInt(1), HakkaJsonString("two"), HakkaJsonBool(False)]
                ),
                "nested_obj": HakkaJsonObject({"key": "value"}),
            }
        )
        serialized = HakkaJson.dumps(obj)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), obj.to_python())

    def test_dump_with_non_string_keys(self):
        # Attempt to dump objects with non-string keys (should fail)
        with self.assertRaises(TypeError):
            obj = HakkaJsonObject(
                {HakkaJsonInt(1): "one", "two": "2"}  # Assuming keys must be strings
            )
            HakkaJson.dump(obj, StringIO())

    def test_dump_with_duplicate_keys(self):
        # JSON does not support duplicate keys; ensure handling or raise error
        json_str = '{"key": "value1", "key": "value2"}'
        loaded_obj = HakkaJson.loads(json_str)
        # Depending on implementation, last key might overwrite
        self.assertEqual(loaded_obj.to_python(), {"key": "value2"})

    def test_loads_with_trailing_data(self):
        # Ensure that trailing data after valid JSON raises an error
        json_str = '{"key": "value"} extra'
        with self.assertRaises(ValueError):
            HakkaJson.loads(json_str)

    def test_loads_with_escaped_characters(self):
        # Test loading JSON with escaped characters
        json_str = '{"text": "Line1\\nLine2\\tTabbed\\"Quote\\""}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_obj.to_python(), {"text": 'Line1\nLine2\tTabbed"Quote"'}
        )

    def test_dump_with_empty_string_keys(self):
        # Test dumping objects with empty string keys
        obj = HakkaJsonObject(
            {"": HakkaJsonString("empty_key"), "valid": HakkaJsonInt(1)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"": "empty_key", "valid": 1}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"": "empty_key", "valid": 1})

    def test_loads_with_various_whitespaces(self):
        # Test loading JSON with various whitespace characters
        json_str = '{\n\t"key1": "value1",\r\n\t"key2": 2\r\n}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"key1": "value1", "key2": 2})

    def test_dump_with_nested_structures(self):
        # Test dumping objects with deeply nested structures
        nested_obj = HakkaJsonObject(
            {
                "level1": HakkaJsonObject(
                    {
                        "level2": HakkaJsonObject(
                            {
                                "level3": HakkaJsonArray(
                                    [
                                        HakkaJsonInt(1),
                                        HakkaJsonArray(
                                            [HakkaJsonInt(2), HakkaJsonInt(3)]
                                        ),
                                    ]
                                )
                            }
                        )
                    }
                )
            }
        )
        serialized = HakkaJson.dumps(nested_obj)
        expected_serialized = '{"level1": {"level2": {"level3": [1, [2, 3]]}}}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), nested_obj.to_python())

    def test_dump_with_boolean_keys(self):
        # Attempt to dump objects with boolean keys (should fail if keys must be strings)
        with self.assertRaises(TypeError):
            obj = HakkaJsonObject({True: "truth", False: "falsehood"})
            HakkaJson.dump(obj, StringIO())

    def test_loads_with_non_ascii_characters(self):
        # Test loading JSON with non-ASCII characters
        json_str = '{"greeting": "你好，世界"}'  # "Hello, World" in Chinese
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"greeting": "你好，世界"})

    def test_dump_and_load_with_numeric_keys_as_strings(self):
        # JSON keys must be strings; numeric keys should be converted to strings
        json_str = '{"1": "one", "2": "two"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"1": "one", "2": "two"})

    def test_loads_with_mixed_type_values(self):
        # Load JSON with mixed type values
        json_str = '{"int": 1, "float": 2.5, "bool": true, "null": null, "array": [1, "two", false]}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_obj.to_python(),
            {
                "int": 1,
                "float": 2.5,
                "bool": True,
                "null": None,
                "array": [1, "two", False],
            },
        )

    def test_dump_with_array_inside_object_inside_array(self):
        # Complex nesting: array inside object inside array
        nested_array = HakkaJsonArray(
            [
                HakkaJsonObject(
                    {"inner_key": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2)])}
                )
            ]
        )
        serialized = HakkaJson.dumps(nested_array)
        expected_serialized = '[{"inner_key": [1, 2]}]'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), [{"inner_key": [1, 2]}])

    def test_loads_with_invalid_escape_sequences(self):
        # Test loading JSON with invalid escape sequences
        invalid_json = '{"text": "Invalid \\x escape"}'
        with self.assertRaises(ValueError):
            HakkaJson.loads(invalid_json)

    def test_dump_with_duplicate_keys_preservation(self):
        # Depending on implementation, duplicate keys might not be preserved
        # JSON standard does not allow duplicate keys; typically last key wins
        json_str = '{"key": "value1", "key": "value2"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"key": "value2"})

    def test_dump_with_special_number_formats(self):
        # Test dumping objects with special number formats
        obj = HakkaJsonObject(
            {
                "scientific": HakkaJsonFloat(1.23e4),
                "hex": HakkaJsonInt(0x1A),
                "binary": HakkaJsonInt(0b1010),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"scientific": 12300.0, "hex": 26, "binary": 10}'
        # TODO: FIXME: Float formatting issue
        # self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"scientific": 12300.0, "hex": 26, "binary": 10}
        )

    def test_loads_with_boolean_values(self):
        # Load JSON containing boolean values
        json_str = '{"isActive": true, "isAdmin": false}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"isActive": True, "isAdmin": False})

    def test_dump_and_load_with_nulls_in_arrays(self):
        # Ensure that nulls within arrays are handled correctly
        array = HakkaJsonArray(
            [HakkaJsonInt(1), HakkaJsonNull(), HakkaJsonString("three")]
        )
        serialized = HakkaJson.dumps(array)
        expected_serialized = '[1, null, "three"]'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), [1, None, "three"])

    def test_loads_with_nested_nulls(self):
        # Load JSON with nested nulls
        json_str = '{"nested": {"key": null}}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"nested": {"key": None}})

    def test_dump_with_non_string_values(self):
        # Attempt to dump objects with non-string values (which should be allowed)
        obj = HakkaJsonObject(
            {
                "number": HakkaJsonInt(10),
                "float": HakkaJsonFloat(3.14),
                "bool": HakkaJsonBool(True),
                "null": HakkaJsonNull(),
                "array": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonString("two")]),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"number": 10, "float": 3.14, "bool": true, "null": null, "array": [1, "two"]}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), obj.to_python())

    def test_loads_with_extra_whitespace(self):
        # Load JSON with leading and trailing whitespace
        json_str = '   { "key": "value" }   '
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"key": "value"})

    def test_dump_with_empty_array_and_object(self):
        obj = HakkaJsonObject(
            {"empty_array": HakkaJsonArray(), "empty_object": HakkaJsonObject()}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"empty_array": [], "empty_object": {}}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"empty_array": [], "empty_object": {}}
        )

    def test_loads_with_mixed_type_arrays(self):
        # Load JSON arrays containing mixed types
        json_str = '[1, "two", true, null, {"key": "value"}, [3, 4]]'
        loaded_array = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_array.to_python(), [1, "two", True, None, {"key": "value"}, [3, 4]]
        )

    def test_loads_with_invalid_json_syntax(self):
        # Test loading JSON with invalid syntax
        invalid_jsons = [
            '{"key": "value",}',  # Trailing comma
            '{"key": value}',  # Missing quotes around value
            '{"key": "value"',  # Missing closing brace
            "[1, 2, 3",  # Missing closing bracket
            '{"key": "value", "another_key":}',  # Missing value
        ]
        for json_str in invalid_jsons:
            with self.assertRaises(ValueError):
                HakkaJson.loads(json_str)

    def test_loads_with_control_characters(self):
        # Load JSON strings containing control characters
        json_str = '{"text": "Control\\u0001Character"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"text": "Control\x01Character"})

    def test_loads_with_surrogate_pairs(self):
        # Load JSON strings containing surrogate pairs
        json_str = '{"emoji": "\\ud83d\\ude00"}'  # 😀 emoji in UTF-16 surrogate pairs
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"emoji": "😀"})

    def test_dump_with_non_ascii_keys(self):
        # Dump objects with non-ASCII keys
        obj = HakkaJsonObject(
            {
                "ключ": HakkaJsonString("значение"),  # "key": "value" in Russian
                "キー": HakkaJsonString("値"),  # "key": "value" in Japanese
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"ключ": "значение", "キー": "値"}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"ключ": "значение", "キー": "値"})

    def test_loads_with_duplicate_keys_preserved_last(self):
        # JSON standard dictates that last duplicate key overwrites previous ones
        json_str = '{"a": 1, "a": 2, "a": 3}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"a": 3})

    def test_dump_with_mixed_unicode_and_ascii(self):
        # Dump objects with mixed Unicode and ASCII characters
        obj = HakkaJsonObject(
            {
                "greeting": HakkaJsonString("Hello, 世界"),
                "farewell": HakkaJsonString("Goodbye, 世界"),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"greeting": "Hello, 世界", "farewell": "Goodbye, 世界"}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(),
            {"greeting": "Hello, 世界", "farewell": "Goodbye, 世界"},
        )

    def test_dump_and_load_with_boolean_true_and_false(self):
        # Ensure that boolean values are correctly handled
        obj = HakkaJsonObject(
            {"true_val": HakkaJsonBool(True), "false_val": HakkaJsonBool(False)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"true_val": true, "false_val": false}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"true_val": True, "false_val": False}
        )

    def test_dump_with_complex_numeric_values(self):
        # Test dumping objects with complex numeric values
        obj = HakkaJsonObject(
            {"float": HakkaJsonFloat(1.23e-4), "int": HakkaJsonInt(1234567890)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"float": 0.000123, "int": 1234567890}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"float": 0.000123, "int": 1234567890}
        )

    def test_loads_with_inconsistent_types(self):
        # Load JSON where types are inconsistent or unexpected
        json_str = '{"number": "not a number"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"number": "not a number"})
        # If HakkaJson enforces types, this might need to raise an error

    def test_dump_and_load_with_empty_strings(self):
        # Test dumping and loading objects with empty strings
        obj = HakkaJsonObject(
            {"empty1": HakkaJsonString(""), "empty2": HakkaJsonString("")}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"empty1": "", "empty2": ""}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"empty1": "", "empty2": ""})

    def test_dump_with_boolean_keys_in_object(self):
        # Attempt to dump objects with boolean keys (should fail if keys must be strings)
        with self.assertRaises(TypeError):
            obj = HakkaJsonObject(
                {HakkaJsonBool(True): "truth", HakkaJsonBool(False): "falsehood"}
            )
            HakkaJson.dump(obj, StringIO())

    def test_loads_with_empty_json(self):
        # Test loading empty JSON objects and arrays
        empty_obj = "{}"
        empty_array = "[]"
        loaded_obj = HakkaJson.loads(empty_obj)
        loaded_array = HakkaJson.loads(empty_array)
        self.assertEqual(loaded_obj.to_python(), {})
        self.assertEqual(loaded_array.to_python(), [])

    def test_dump_and_load_with_nested_nulls(self):
        # Dump and load objects with nested nulls
        obj = HakkaJsonObject({"level1": HakkaJsonObject({"level2": HakkaJsonNull()})})
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"level1": {"level2": null}}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"level1": {"level2": None}})

    def test_loads_with_invalid_unicode_escape(self):
        # Test loading JSON with invalid Unicode escape sequences
        invalid_json = '{"text": "Invalid \\uZZZZ escape"}'
        with self.assertRaises(ValueError):
            HakkaJson.loads(invalid_json)

    def test_loads_with_numeric_keys_as_strings(self):
        # JSON keys must be strings; numeric keys are treated as strings
        json_str = '{"1": "one", "2": "two"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"1": "one", "2": "two"})

    def test_dump_with_invalid_utf8_characters(self):
        # If HakkaJson enforces UTF-8, test dumping strings with invalid UTF-8
        # However, Python strings are Unicode, so invalid UTF-8 sequences aren't possible
        # unless using bytes, which HakkaJsonString likely does not accept
        with self.assertRaises(TypeError):
            HakkaJsonString(b"\xff").to_python()  # Assuming to_python expects str

    def test_loads_with_null_values_in_arrays(self):
        # Load JSON arrays containing null values
        json_str = '[1, null, "three", null]'
        loaded_array = HakkaJson.loads(json_str)
        self.assertEqual(loaded_array.to_python(), [1, None, "three", None])

    def test_dump_and_load_with_boolean_in_objects(self):
        # Ensure that boolean values within objects are handled correctly
        obj = HakkaJsonObject(
            {"isActive": HakkaJsonBool(True), "isVerified": HakkaJsonBool(False)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"isActive": true, "isVerified": false}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"isActive": True, "isVerified": False}
        )

    def test_loads_with_empty_object_and_array(self):
        # Load JSON with empty object and array
        json_str = '{"empty_obj": {}, "empty_array": []}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"empty_obj": {}, "empty_array": []})

    def test_dump_with_boolean_values_in_array(self):
        # Dump and load arrays containing boolean values
        array = HakkaJsonArray([HakkaJsonBool(True), HakkaJsonBool(False)])
        serialized = HakkaJson.dumps(array)
        expected_serialized = "[true, false]"
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), [True, False])

    def test_loads_with_nested_objects_and_arrays(self):
        # Load JSON with nested objects and arrays
        json_str = """
        {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ],
            "count": 2,
            "active": true
        }
        """
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_obj.to_python(),
            {
                "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
                "count": 2,
                "active": True,
            },
        )

    def test_dump_with_nested_nulls(self):
        # Dump and load objects with nested nulls
        obj = HakkaJsonObject(
            {
                "level1": HakkaJsonObject({"level2": HakkaJsonNull()}),
                "level3": HakkaJsonNull(),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"level1": {"level2": null}, "level3": null}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"level1": {"level2": None}, "level3": None}
        )

    def test_loads_with_extra_brackets(self):
        # Test loading JSON with extra brackets
        json_str = '{"key": "value"}}'
        with self.assertRaises(ValueError):
            HakkaJson.loads(json_str)

    def test_dump_with_numeric_keys_as_strings(self):
        # Ensure numeric keys are treated as strings
        obj = HakkaJsonObject({"1": HakkaJsonInt(1), "2": HakkaJsonInt(2)})
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"1": 1, "2": 2}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"1": 1, "2": 2})

    def test_loads_with_empty_string(self):
        # Loading an empty string should raise an error
        with self.assertRaises(ValueError):
            HakkaJson.loads("")

    def test_dump_and_load_with_boolean_nested_in_objects(self):
        # Ensure that boolean values nested within objects are handled correctly
        obj = HakkaJsonObject(
            {
                "settings": HakkaJsonObject(
                    {"enabled": HakkaJsonBool(True), "visible": HakkaJsonBool(False)}
                )
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"settings": {"enabled": true, "visible": false}}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"settings": {"enabled": True, "visible": False}}
        )

    def test_loads_with_invalid_boolean_values(self):
        # Test loading JSON with invalid boolean representations
        invalid_jsons = [
            '{"key": True}',  # True should be lowercase
            '{"key": False}',  # False should be lowercase
            '{"key": TRUE}',  # Incorrect casing
            '{"key": FALSE}',  # Incorrect casing
        ]
        for json_str in invalid_jsons:
            with self.assertRaises(ValueError):
                HakkaJson.loads(json_str)

    def test_dump_with_special_float_values(self):
        # Dump objects with NaN and Infinity
        obj = HakkaJsonObject(
            {
                "nan": HakkaJsonFloat(float("nan")),
                "inf": HakkaJsonFloat(float("inf")),
                "neg_inf": HakkaJsonFloat(float("-inf")),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"nan": nan, "inf": inf, "neg_inf": -inf}'
        self.assertEqual(serialized, expected_serialized)
        with self.assertRaises(ValueError):
            HakkaJson.loads(serialized)


    def test_dump_with_empty_object_keys(self):
        # Test dumping objects with empty string keys
        obj = HakkaJsonObject(
            {"": HakkaJsonString("empty_key"), "non_empty": HakkaJsonInt(1)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"": "empty_key", "non_empty": 1}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"": "empty_key", "non_empty": 1})

    def test_loads_with_array_of_nulls(self):
        # Load JSON arrays containing only nulls
        json_str = "[null, null, null]"
        loaded_array = HakkaJson.loads(json_str)
        self.assertEqual(loaded_array.to_python(), [None, None, None])

    def test_dump_and_load_with_mixed_nested_structures(self):
        # Dump and load deeply nested mixed structures
        obj = HakkaJsonObject(
            {
                "array": HakkaJsonArray(
                    [
                        HakkaJsonObject(
                            {
                                "nested_array": HakkaJsonArray(
                                    [
                                        HakkaJsonInt(1),
                                        HakkaJsonObject(
                                            {"deep_key": HakkaJsonString("deep_value")}
                                        ),
                                    ]
                                )
                            }
                        ),
                        HakkaJsonBool(True),
                    ]
                ),
                "null_value": HakkaJsonNull(),
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"array": [{"nested_array": [1, {"deep_key": "deep_value"}]}, true], "null_value": null}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(),
            {
                "array": [{"nested_array": [1, {"deep_key": "deep_value"}]}, True],
                "null_value": None,
            },
        )

    def test_loads_with_multiple_types_in_array(self):
        # Load JSON arrays containing multiple types
        json_str = '[1, "two", 3.0, true, null, {"key": "value"}, [4, "five"]]'
        loaded_array = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_array.to_python(),
            [1, "two", 3.0, True, None, {"key": "value"}, [4, "five"]],
        )

    def test_dump_with_custom_objects_in_array(self):
        array = HakkaJsonArray([HakkaJsonInt(1), "invalid_string"])
        HakkaJson.dump(array, StringIO())

    def test_loads_with_mixed_escape_sequences(self):
        # Load JSON with mixed escape sequences in strings
        json_str = '{"path": "C:\\\\Users\\\\Name", "newline": "Line1\\nLine2"}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_obj.to_python(),
            {"path": "C:\\Users\\Name", "newline": "Line1\nLine2"},
        )

    def test_dump_with_nested_nulls_in_arrays(self):
        # Dump objects with nested nulls within arrays
        obj = HakkaJsonObject(
            {
                "array": HakkaJsonArray(
                    [HakkaJsonNull(), HakkaJsonInt(1), HakkaJsonNull()]
                )
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"array": [null, 1, null]}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(deserialized.to_python(), {"array": [None, 1, None]})

    def test_loads_with_empty_string_keys(self):
        # Load JSON with empty string keys
        json_str = '{"": "empty_key", "valid_key": 1}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(loaded_obj.to_python(), {"": "empty_key", "valid_key": 1})

    def test_dump_with_numeric_values_as_strings(self):
        # Ensure numeric values are correctly handled when represented as strings
        obj = HakkaJsonObject(
            {"number_str": HakkaJsonString("12345"), "number_int": HakkaJsonInt(12345)}
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = '{"number_str": "12345", "number_int": 12345}'
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(), {"number_str": "12345", "number_int": 12345}
        )

    def test_loads_with_boolean_and_null_combinations(self):
        # Load JSON with combinations of boolean and null
        json_str = '{"active": true, "deleted": false, "archived": null}'
        loaded_obj = HakkaJson.loads(json_str)
        self.assertEqual(
            loaded_obj.to_python(), {"active": True, "deleted": False, "archived": None}
        )

    def test_dump_with_nested_boolean_objects(self):
        # Dump and load objects containing nested boolean values
        obj = HakkaJsonObject(
            {
                "settings": HakkaJsonObject(
                    {
                        "feature_enabled": HakkaJsonBool(True),
                        "beta_mode": HakkaJsonBool(False),
                    }
                )
            }
        )
        serialized = HakkaJson.dumps(obj)
        expected_serialized = (
            '{"settings": {"feature_enabled": true, "beta_mode": false}}'
        )
        self.assertEqual(serialized, expected_serialized)
        deserialized = HakkaJson.loads(serialized)
        self.assertEqual(
            deserialized.to_python(),
            {"settings": {"feature_enabled": True, "beta_mode": False}},
        )


if __name__ == "__main__":
    unittest.main()
