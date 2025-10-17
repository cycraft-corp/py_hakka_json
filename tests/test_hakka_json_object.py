import unittest
import pickle

from py_hakka_json import (
    HakkaJsonObject,
    HakkaJsonArray,
    HakkaJsonInt,
    HakkaJsonString,
    HakkaJsonBool,
    HakkaJsonNull,
)


class TestHakkaJsonObject(unittest.TestCase):
    def test_initialization(self):
        obj = HakkaJsonObject()
        self.assertEqual(len(obj), 0)

        obj_from_dict = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj_from_dict["key"], "value")

        obj_from_obj = HakkaJsonObject(obj_from_dict)
        self.assertEqual(obj_from_obj["key"], "value")

    def test_initialization_invalid_type(self):
        with self.assertRaises(TypeError):
            HakkaJsonObject("invalid")

    def test_to_python(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj.to_python(), {"key": "value"})

    def test_from_python(self):
        obj = HakkaJsonObject.from_python({"key": "value"})
        self.assertEqual(obj["key"], "value")

    def test_dumps(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj.dumps(), '{"key": "value"}')

    def test_len(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(len(obj), 1)

    def test_getitem(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj["key"], "value")
        with self.assertRaises(KeyError):
            _ = obj["nonexistent"]

    def test_setitem(self):
        obj = HakkaJsonObject()
        obj["key"] = "value"
        self.assertEqual(obj["key"], "value")

    def test_delitem(self):
        obj = HakkaJsonObject({"key": "value"})
        del obj["key"]
        self.assertNotIn("key", obj)
        with self.assertRaises(KeyError):
            del obj["nonexistent"]

    def test_contains(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertIn("key", obj)
        self.assertNotIn("nonexistent", obj)

    def test_iter(self):
        obj = HakkaJsonObject({"key": "value"})
        keys = list(iter(obj))
        self.assertEqual(keys, ["key"])

    def test_get(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj.get("key"), "value")
        self.assertEqual(obj.get("nonexistent", "default"), "default")

    def test_setdefault(self):
        obj = HakkaJsonObject()
        obj.setdefault("key", "value")
        self.assertEqual(obj["key"], "value")
        obj.setdefault("key", "new_value")
        self.assertEqual(obj["key"], "value")

    def test_pop(self):
        obj = HakkaJsonObject({"key": "value"})
        value = obj.pop("key")
        self.assertEqual(value, "value")
        self.assertNotIn("key", obj)
        with self.assertRaises(KeyError):
            obj.pop("nonexistent")
        self.assertEqual(obj.pop("nonexistent", "default"), "default")

    def test_popitem(self):
        obj = HakkaJsonObject({"key": "value"})
        key, value = obj.popitem()
        self.assertEqual(key, "key")
        self.assertEqual(value, "value")
        with self.assertRaises(KeyError):
            obj.popitem()

    def test_keys(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(list(obj.keys()), ["key"])

    def test_values(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(list(obj.values()), ["value"])

    def test_items(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(list(obj.items()), [("key", "value")])

    def test_update(self):
        obj = HakkaJsonObject({"key": "value"})
        obj.update({"new_key": "new_value"})
        self.assertEqual(obj["new_key"], "new_value")

    def test_clear(self):
        obj = HakkaJsonObject({"key": "value"})
        obj.clear()
        self.assertEqual(len(obj), 0)

    def test_copy(self):
        obj = HakkaJsonObject({"key": "value"})
        obj_copy = obj.copy()
        self.assertEqual(obj_copy["key"], "value")

    def test_fromkeys(self):
        obj = HakkaJsonObject.fromkeys(["key1", "key2"], "value")
        self.assertEqual(obj["key1"], "value")
        self.assertEqual(obj["key2"], "value")

    def test_repr(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(repr(obj), "HakkaJsonObject({'key': 'value'})")

    def test_str(self):
        obj = HakkaJsonObject({"key": "value"})
        self.assertEqual(str(obj), "{'key': 'value'}")

    def test_eq(self):
        obj1 = HakkaJsonObject({"key": "value"})
        obj2 = HakkaJsonObject({"key": "value"})
        self.assertEqual(obj1, obj2)

    def test_ne(self):
        obj1 = HakkaJsonObject({"key": "value"})
        obj2 = HakkaJsonObject({"key": "different_value"})
        self.assertNotEqual(obj1, obj2)

    def test_lt(self):
        obj1 = HakkaJsonObject({"key": "value"})
        obj2 = HakkaJsonObject({"key": "value", "key2": "value2"})
        self.assertLess(obj1, obj2)

    def test_le(self):
        obj1 = HakkaJsonObject({"key": "value"})
        obj2 = HakkaJsonObject({"key": "value"})
        self.assertLessEqual(obj1, obj2)

    def test_gt(self):
        obj1 = HakkaJsonObject({"key": "value", "key2": "value2"})
        obj2 = HakkaJsonObject({"key": "value"})
        self.assertGreater(obj1, obj2)

    def test_ge(self):
        obj1 = HakkaJsonObject({"key": "value"})
        obj2 = HakkaJsonObject({"key": "value"})
        self.assertGreaterEqual(obj1, obj2)

    def test_or(self):
        obj1 = HakkaJsonObject({"key1": "value1"})
        obj2 = HakkaJsonObject({"key2": "value2"})
        result = obj1 | obj2
        self.assertEqual(result["key1"], "value1")
        self.assertEqual(result["key2"], "value2")

    def test_ior(self):
        obj1 = HakkaJsonObject({"key1": "value1"})
        obj2 = HakkaJsonObject({"key2": "value2"})
        obj1 |= obj2
        self.assertEqual(obj1["key1"], "value1")
        self.assertEqual(obj1["key2"], "value2")

    def test_hash(self):
        obj = HakkaJsonObject({"key": "value"})
        with self.assertRaises(TypeError):
            hash(obj)

    def test_pickle(self):
        obj = HakkaJsonObject({"key": "value"})
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        self.assertEqual(deserialized, obj)

    def test_dir_all_are_in_dir(self):
        fun_list = dir(HakkaJsonObject)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonObject, name))


class TestHakkaJsonObjectAdvanced(unittest.TestCase):
    def test_nested_objects_and_arrays(self):
        # Create a complex nested object
        obj = HakkaJsonObject(
            {
                "user": HakkaJsonObject(
                    {
                        "id": HakkaJsonInt(1),
                        "name": HakkaJsonString("Alice"),
                        "roles": HakkaJsonArray(
                            [HakkaJsonString("admin"), HakkaJsonString("user")]
                        ),
                    }
                ),
                "active": HakkaJsonBool(True),
                "meta": HakkaJsonNull(),
            }
        )
        self.assertEqual(
            obj.to_python(),
            {
                "user": {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
                "active": True,
                "meta": None,
            },
        )
        # Test deep access and mutation
        obj["user"]["roles"].append(HakkaJsonString("editor"))
        self.assertEqual(obj.to_python()["user"]["roles"], ["admin", "user", "editor"])

    def test_dynamic_key_addition_and_deletion(self):
        obj = HakkaJsonObject()
        obj["new_key"] = "new_value"
        self.assertIn("new_key", obj)
        self.assertEqual(obj["new_key"], "new_value")
        del obj["new_key"]
        self.assertNotIn("new_key", obj)
        with self.assertRaises(KeyError):
            del obj["new_key"]

    def test_edge_cases_empty_object(self):
        empty_obj = HakkaJsonObject()
        self.assertEqual(len(empty_obj), 0)
        self.assertEqual(empty_obj.to_python(), {})
        with self.assertRaises(KeyError):
            _ = empty_obj["nonexistent"]

    def test_iteration_order(self):
        # Ensure that iteration order is preserved (Python 3.7+ dictionaries preserve insertion order)
        obj = HakkaJsonObject({"first": "1st", "second": "2nd", "third": "3rd"})
        keys = [key for key in obj]
        self.assertEqual(keys, ["first", "second", "third"])

    def test_off_by_one_errors(self):
        obj = HakkaJsonObject({"a": 1, "b": 2, "c": 3})
        self.assertEqual(len(obj), 3)
        with self.assertRaises(KeyError):
            _ = obj["d"]  # Nonexistent key

    def test_compound_types(self):
        # Object containing arrays and other objects
        obj = HakkaJsonObject(
            {
                "array": HakkaJsonArray([HakkaJsonInt(10), HakkaJsonInt(20)]),
                "nested_obj": HakkaJsonObject({"key": "value"}),
            }
        )
        self.assertEqual(
            obj.to_python(), {"array": [10, 20], "nested_obj": {"key": "value"}}
        )
        # Modify nested array
        obj["array"].append(HakkaJsonInt(30))
        self.assertEqual(obj.to_python()["array"], [10, 20, 30])

    # TODO: Implement HakkaJsonBase.__reduce__ to enable pickling
    # def test_pickle_complex_object(self):
    #     # Complex object with nested structures
    #     obj = HakkaJsonObject(
    #         {
    #             "user": HakkaJsonObject(
    #                 {
    #                     "id": HakkaJsonInt(2),
    #                     "name": HakkaJsonString("Bob"),
    #                     "active": HakkaJsonBool(False),
    #                 }
    #             ),
    #             "tags": HakkaJsonArray(
    #                 [HakkaJsonString("beta"), HakkaJsonString("tester")]
    #             ),
    #             "metadata": HakkaJsonNull(),
    #         }
    #     )
    #     serialized = pickle.dumps(obj)
    #     deserialized = pickle.loads(serialized)
    #     self.assertEqual(deserialized.to_python(), obj.to_python())
    #     self.assertIsInstance(deserialized, HakkaJsonObject)
    #     self.assertIsInstance(deserialized["user"], HakkaJsonObject)
    #     self.assertIsInstance(deserialized["tags"], HakkaJsonArray)

    def test_functional_operations(self):
        # Using functional programming with HakkaJsonObject
        obj = HakkaJsonObject(
            {"a": HakkaJsonInt(1), "b": HakkaJsonInt(2), "c": HakkaJsonInt(3)}
        )
        # Map: Increment each value by 1
        incremented = HakkaJsonObject(
            {key: HakkaJsonInt(value.to_python() + 1) for key, value in obj.items()}
        )
        self.assertEqual(incremented.to_python(), {"a": 2, "b": 3, "c": 4})
        # Filter: Keep only even values
        filtered = HakkaJsonObject(
            {key: value for key, value in obj.items() if value.to_python() % 2 == 0}
        )
        self.assertEqual(filtered.to_python(), {"b": 2})

    def test_boundary_conditions_large_keys_and_values(self):
        # Test with very long keys and large values
        large_key = "k" * 1000
        large_value = 10**100
        with self.assertRaises(OverflowError):
            HakkaJsonObject({large_key: HakkaJsonInt(large_value)})
        with self.assertRaises(OverflowError):
            HakkaJsonObject({HakkaJsonString(large_key): HakkaJsonInt(large_value)})
        with self.assertRaises(OverflowError):
            HakkaJsonObject({large_key: large_value})

    def test_invalid_key_types(self):
        # Assuming keys must be strings, test with invalid key types
        with self.assertRaises(TypeError):
            HakkaJsonObject({123: "number key"})
        with self.assertRaises(TypeError):
            HakkaJsonObject({HakkaJsonInt(1): "hakka key"})

    def test_dynamic_method_addition(self):
        # Dynamically add a method to HakkaJsonObject
        obj = HakkaJsonObject({"key": "value"})

        def custom_method(self):
            return "custom_method_result"

        HakkaJsonObject.custom_method = custom_method
        self.assertEqual(obj.custom_method(), "custom_method_result")
        del HakkaJsonObject.custom_method

    def test_memory_leak_detection(self):
        # We do this because we have the handle_to_object() to hold the class object
        def one_batch():
            import sys

            # Create and delete a large number of objects, ensure memory is reclaimed
            initial_memory = sys.getrefcount(HakkaJsonObject)
            for _ in range(1000):
                obj = HakkaJsonObject({f"key{i}": HakkaJsonInt(i) for i in range(100)})
            import gc

            gc.collect()
            final_memory = sys.getrefcount(HakkaJsonObject)
            return initial_memory, final_memory

        initial_memory, final_memory = one_batch()
        initial_memory2, final_memory2 = one_batch()

        self.assertEqual(initial_memory, initial_memory2)
        self.assertEqual(final_memory, final_memory2)

    def test_hierarchical_integrity_after_mutations(self):
        # Ensure that mutations in nested structures maintain overall integrity
        obj = HakkaJsonObject(
            {
                "level1": HakkaJsonObject(
                    {"level2": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2)])}
                )
            }
        )
        # Mutate level2 array
        obj["level1"]["level2"].append(HakkaJsonInt(3))
        self.assertEqual(obj.to_python(), {"level1": {"level2": [1, 2, 3]}})
        # Mutate level1 object
        obj["level1"]["new_key"] = HakkaJsonString("new_value")
        self.assertEqual(
            obj.to_python(), {"level1": {"level2": [1, 2, 3], "new_key": "new_value"}}
        )

    def test_cross_type_interactions(self):
        # Interactions between different HakkaJson types within an object
        obj = HakkaJsonObject(
            {
                "string": HakkaJsonString("test"),
                "int": HakkaJsonInt(10),
                "bool": HakkaJsonBool(True),
                "null": HakkaJsonNull(),
                "array": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonString("two")]),
            }
        )
        self.assertIn("string", obj)
        self.assertIn("int", obj)
        self.assertIn("bool", obj)
        self.assertIn("null", obj)
        self.assertIn("array", obj)
        self.assertEqual(obj["string"].to_python(), "test")
        self.assertEqual(obj["int"].to_python(), 10)
        self.assertEqual(obj["bool"].to_python(), True)
        self.assertIsNone(obj["null"].to_python())
        self.assertEqual(obj["array"].to_python(), [1, "two"])

    def test_type_enforcement(self):
        obj = HakkaJsonObject()
        obj["key"] = 123  # Assuming only HakkaJsonBase instances are allowed
        obj.update({"new_key": "value"})  # Assuming type enforcement

    def test_dir_all_are_in_dir(self):
        # Ensure all methods are accessible
        fun_list = dir(HakkaJsonObject)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonObject, name))


if __name__ == "__main__":
    unittest.main()
