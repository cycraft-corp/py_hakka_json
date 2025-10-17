import unittest

import pickle
from py_hakka_json._hakka_json_bool import HakkaJsonBool
from py_hakka_json._hakka_json_int import HakkaJsonInt
from py_hakka_json._hakka_json_string import HakkaJsonString
from py_hakka_json._hakka_json_array import HakkaJsonArray, HakkaJsonArrayIterator
from py_hakka_json._hakka_json_object import HakkaJsonObject
from py_hakka_json._hakka_json_float import HakkaJsonFloat


class TestHakkaJsonArray(unittest.TestCase):
    def test_initialization(self):
        array = HakkaJsonArray()
        self.assertEqual(len(array), 0)

        array_with_elements = HakkaJsonArray([1, 2, 3])
        self.assertEqual(len(array_with_elements), 3)
        self.assertEqual(array_with_elements.to_python(), [1, 2, 3])

    def test_loads(self):
        array = HakkaJsonArray.loads("[1, 2, 3]")
        self.assertEqual(len(array), 3)
        self.assertEqual(array.to_python(), [1, 2, 3])

    def test_loads_invalid(self):
        # string is not a valid JSON
        with self.assertRaises(ValueError):
            HakkaJsonArray.loads("invalid json")
        # bad json (missing closing bracket)
        with self.assertRaises(ValueError):
            HakkaJsonArray.loads("[1, 2, 3")
        # bad json (invalid qoute)
        with self.assertRaises(ValueError):
            HakkaJsonArray.loads('["a", "b, "c"]')

    def test_loads_depth_exceed(self):
        """
        Test loading a JSON array with exceeded depth.
        """
        with self.assertRaises(RecursionError):
            HakkaJsonArray.loads(
                """[[[[[[[[[[[[[[1, 2, 3]]]]]]]]]]]]]]""",
                3,
            )

    def test_append(self):
        array = HakkaJsonArray()
        array.append(1)
        self.assertEqual(len(array), 1)
        self.assertEqual(array[0].to_python(), 1)

    def test_extend(self):
        array = HakkaJsonArray([1, 2])
        array.extend([3, 4])
        self.assertEqual(len(array), 4)
        self.assertEqual(array.to_python(), [1, 2, 3, 4])

    def test_pop(self):
        array = HakkaJsonArray([1, 2, 3])
        value = array.pop()
        self.assertEqual(value.to_python(), 3)
        self.assertEqual(len(array), 2)

        popped = array.pop(0)
        self.assertEqual(popped.to_python(), 1)
        self.assertEqual(len(array), 1)

    def test_getitem(self):
        array = HakkaJsonArray([1, 2, 3])
        self.assertEqual(array[1].to_python(), 2)
        self.assertEqual(array[-1].to_python(), 3)

        with self.assertRaises(IndexError):
            _ = array[3]

    def test_setitem(self):
        array = HakkaJsonArray([1, 2, 3])
        array[1] = 20
        self.assertEqual(array[1].to_python(), 20)
        self.assertEqual(array.to_python(), [1, 20, 3])

        with self.assertRaises(IndexError):
            array[3] = 4

    def test_delete_item(self):
        array = HakkaJsonArray([1, 2, 3])
        del array[1]
        self.assertEqual(len(array), 2)
        self.assertEqual(array.to_python(), [1, 3])

        with self.assertRaises(IndexError):
            del array[2]

    def test_contains(self):
        array = HakkaJsonArray([1, 2, 3])
        self.assertTrue(2 in array)
        self.assertFalse(4 in array)

    def test_clear(self):
        array = HakkaJsonArray([1, 2, 3])
        array.clear()
        self.assertEqual(len(array), 0)
        self.assertFalse(array)

    def test_copy(self):
        array = HakkaJsonArray([1, 2, 3])
        copied = array.copy()
        self.assertEqual(copied.to_python(), [1, 2, 3])
        self.assertIsNot(array, copied)

    def test_equality(self):
        array1 = HakkaJsonArray([1, 2, 3])
        array2 = HakkaJsonArray([1, 2, 3])
        array3 = HakkaJsonArray([4, 5, 6])
        self.assertEqual(array1, array2)
        self.assertNotEqual(array1, array3)

    def test_iteration(self):
        array = HakkaJsonArray([1, 2, 3])
        items = [item.to_python() for item in array]
        self.assertEqual(items, [1, 2, 3])

    def test_reverse(self):
        array = HakkaJsonArray([1, 2, 3])
        array.reverse()
        self.assertEqual(array.to_python(), [3, 2, 1])

    def test_sort(self):
        array = HakkaJsonArray([3, 1, 2])
        array.sort()
        self.assertEqual(array.to_python(), [1, 2, 3])

        array_desc = HakkaJsonArray([3, 1, 2])
        array_desc.sort(reverse=True)
        self.assertEqual(array_desc.to_python(), [3, 2, 1])

    def test_insert(self):
        array = HakkaJsonArray([1, 3])
        array.insert(1, 2)
        self.assertEqual(array.to_python(), [1, 2, 3])

        with self.assertRaises(IndexError):
            array.insert(5, 4)

    def test_remove(self):
        array = HakkaJsonArray([1, 2, 3, 2])
        array.remove(2)
        self.assertEqual(array.to_python(), [1, 3, 2])

        with self.assertRaises(ValueError):
            array.remove(4)

    def test_count(self):
        array = HakkaJsonArray([1, 2, 2, 3])
        self.assertEqual(array.count(2), 2)
        self.assertEqual(array.count(4), 0)

    def test_index(self):
        array = HakkaJsonArray([1, 2, 3, 2])
        self.assertEqual(array.index(2), 1)
        self.assertEqual(array.index(2, 2), 3)

        with self.assertRaises(ValueError):
            array.index(4)

    def test_add(self):
        array1 = HakkaJsonArray([1, 2])
        array2 = HakkaJsonArray([3, 4])
        result = array1 + array2
        self.assertEqual(result.to_python(), [1, 2, 3, 4])

        with self.assertRaises(TypeError):
            array1 + 5

    def test_iadd(self):
        array1 = HakkaJsonArray([1, 2])
        array2 = HakkaJsonArray([3, 4])
        array1 += array2
        self.assertEqual(array1.to_python(), [1, 2, 3, 4])

        with self.assertRaises(TypeError):
            array1 += 5

    def test_mul(self):
        array = HakkaJsonArray([1, 2])
        result = array * 3
        self.assertEqual(result.to_python(), [1, 2, 1, 2, 1, 2])

        with self.assertRaises(TypeError):
            array * "a"

    def test_rmul(self):
        array = HakkaJsonArray([1, 2])
        result = 3 * array
        self.assertEqual(result.to_python(), [1, 2, 1, 2, 1, 2])

    def test_imul(self):
        array = HakkaJsonArray([1, 2])
        array *= 3
        self.assertEqual(array.to_python(), [1, 2, 1, 2, 1, 2])

        with self.assertRaises(TypeError):
            array *= "a"

    def test_repr(self):
        array = HakkaJsonArray([1, 2, 3])
        self.assertEqual(
            repr(array),
            "HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2), HakkaJsonInt(3)])",
        )

    def test_str(self):
        array = HakkaJsonArray([1, 2, 3])
        self.assertEqual(
            str(array), "[HakkaJsonInt(1), HakkaJsonInt(2), HakkaJsonInt(3)]"
        )

    def test_reduce(self):
        array = HakkaJsonArray([1, 2, 3])
        data = pickle.dumps(array)
        loaded_array = pickle.loads(data)
        self.assertEqual(loaded_array.to_python(), [1, 2, 3])
        self.assertNotEqual(id(array), id(loaded_array))

    def test_reversed(self):
        array = HakkaJsonArray([1, 2, 3])
        reversed_items = list(reversed(array))
        self.assertEqual(reversed_items, [3, 2, 1])

    def test_from_python(self):
        py_list = [4, 5, 6]
        array = HakkaJsonArray.from_python(py_list)
        self.assertIsInstance(array, HakkaJsonArray)
        self.assertEqual(array.to_python(), py_list)

        with self.assertRaises(TypeError):
            HakkaJsonArray.from_python("not a list")

    def test_dump(self):
        array = HakkaJsonArray([1, HakkaJsonString("two"), HakkaJsonBool(True)])
        dumped = array.dumps()
        self.assertEqual(dumped, '[1, "two", true]')

        empty_array = HakkaJsonArray()
        self.assertEqual(empty_array.dumps(), "[]")

    def test_from_python_invalid(self):
        with self.assertRaises(TypeError):
            HakkaJsonArray.from_python(123)  # Not an iterable

    def test_append_string(self):
        array = HakkaJsonArray()
        array.append("A dummy string instead of HakkaJsonBase")
        self.assertEqual(len(array), 1)
        self.assertEqual(
            array[0].to_python(), "A dummy string instead of HakkaJsonBase"
        )

    def test_extend_list(self):
        array = HakkaJsonArray()
        array.extend([1, "dummy", 3])
        self.assertEqual(len(array), 3)
        self.assertEqual(array.to_python(), [1, "dummy", 3])

    def test_insert_python_string(self):
        array = HakkaJsonArray([1, 2, 3])
        array.insert(1, "dummy")

    def test_remove_invalid(self):
        array = HakkaJsonArray([1, 2, 3])
        with self.assertRaises(ValueError):
            array.remove("invalid")

    def test_pop_empty(self):
        array = HakkaJsonArray()
        with self.assertRaises(IndexError):
            array.pop()

    def test_copy_independence(self):
        array = HakkaJsonArray([1, 2, 3])
        copied = array.copy()
        copied.append(4)
        self.assertEqual(array.to_python(), [1, 2, 3])
        self.assertEqual(copied.to_python(), [1, 2, 3, 4])

    def test_sort_with_key(self):
        array = HakkaJsonArray(
            [
                HakkaJsonString("banana"),
                HakkaJsonString("apple"),
                HakkaJsonString("cherry"),
            ]
        )
        array.sort(key=lambda x: x.to_python())
        self.assertEqual(array.to_python(), ["apple", "banana", "cherry"])

    def test_sort_reverse(self):
        array = HakkaJsonArray([3, 1, 2])
        array.sort(reverse=True)
        self.assertEqual(array.to_python(), [3, 2, 1])

    def test_reduce_unpickle(self):
        array = HakkaJsonArray([1, 2, 3])
        data = pickle.dumps(array)
        loaded_array = pickle.loads(data)
        self.assertEqual(loaded_array.to_python(), [1, 2, 3])
        self.assertIsInstance(loaded_array, HakkaJsonArray)

    def test_iterator_reverse(self):
        array = HakkaJsonArray([1, 2, 3])
        iter_rev = HakkaJsonArrayIterator(array, reverse=True)
        items = [item.to_python() for item in iter_rev]
        self.assertEqual(items, [3, 2, 1])

    def test_contains_with_custom_objects(self):
        array = HakkaJsonArray(
            [HakkaJsonInt(1), HakkaJsonString("two"), HakkaJsonBool(True)]
        )
        self.assertTrue(HakkaJsonInt(1) in array)
        self.assertFalse(HakkaJsonInt(2) in array)
        self.assertTrue(HakkaJsonString("two") in array)
        self.assertFalse(HakkaJsonString("three") in array)

    def test_non_iterable_initialization(self):
        with self.assertRaises(TypeError):
            HakkaJsonArray(123)

    def test_len_after_operations(self):
        array = HakkaJsonArray()
        self.assertEqual(len(array), 0)
        array.append(HakkaJsonInt(1))
        self.assertEqual(len(array), 1)
        array.extend([HakkaJsonInt(2), HakkaJsonInt(3)])
        self.assertEqual(len(array), 3)
        array.pop()
        self.assertEqual(len(array), 2)
        array.clear()
        self.assertEqual(len(array), 0)

    # test complex structure, nested array and many types
    def test_complex_structure(self):
        array = HakkaJsonArray()
        array.append(HakkaJsonInt(1))
        array.append(HakkaJsonString("two"))
        array.append(HakkaJsonBool(True))
        nested = HakkaJsonArray()
        nested.append(HakkaJsonInt(4))
        nested.append(HakkaJsonString("five"))
        nested.append(HakkaJsonBool(False))
        array.append(nested)
        self.assertEqual(array.to_python(), [1, "two", True, [4, "five", False]])

    # test returning a inner array from another function constructed from HakkaJsonArray
    # for example: some function have local HakkaJsonArray [1, 2, 3, ["another", "array", [null, 4]]]
    # but the function returns only the inner array ["another", "array", [null, 4]]
    # check the returned array is HakkaJsonArray and its content is correct
    def test_inner_array(self):
        def get_inner_array():
            arr = HakkaJsonArray.loads('[1, 2, 3, ["another", "array", [null, 4]]]')
            # check the array is correct
            self.assertEqual(
                arr.to_python(), [1, 2, 3, ["another", "array", [None, 4]]]
            )
            # return the inner array
            return arr[3]

        inner = get_inner_array()
        self.assertIsInstance(inner, HakkaJsonArray)
        self.assertEqual(
            inner.to_python(), ["another", "array", [None, 4]]
        )  # ensure functional style works

    def test_dir_all_are_in_dir(self):
        fun_list = dir(HakkaJsonArray)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonArray, name))

    def test_slice(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        sliced = array[1:4]
        self.assertEqual(sliced.to_python(), [2, 3, 4])
        self.assertIsInstance(sliced, HakkaJsonArray)

    def test_slice_with_step(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        sliced = array[1:4:2]
        self.assertEqual(sliced.to_python(), [2, 4])
        self.assertIsInstance(sliced, HakkaJsonArray)

    def test_slice_with_negative_index(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        sliced = array[-4:-1]
        self.assertEqual(sliced.to_python(), [2, 3, 4])
        self.assertIsInstance(sliced, HakkaJsonArray)

    def test_slice_with_negative_index_and_step(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        sliced = array[-4:-1:2]
        self.assertEqual(sliced.to_python(), [2, 4])
        self.assertIsInstance(sliced, HakkaJsonArray)

    def test_slice_with_negative_index_and_step_and_end(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        sliced = array[-4:-1:2]
        self.assertEqual(sliced.to_python(), [2, 4])
        self.assertIsInstance(sliced, HakkaJsonArray)

    # test set slice
    def test_set_slice(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        array[1:4] = [10, 20, 30]
        self.assertEqual(array.to_python(), [1, 10, 20, 30, 5]) 
    
    def test_or_operator_with_hakka_json_array(self):
        array1 = HakkaJsonArray([1, 2, 3])
        array2 = HakkaJsonArray([4, 5, 6])
        result = array1 | array2
        self.assertEqual(result.to_python(), [1, 2, 3, 4, 5, 6])

    def test_or_operator_with_list(self):
        array1 = HakkaJsonArray([1, 2, 3])
        list2 = [4, 5, 6]
        result = array1 | list2
        self.assertEqual(result.to_python(), [1, 2, 3, 4, 5, 6])

    def test_or_operator_with_tuple(self):
        array1 = HakkaJsonArray([1, 2, 3])
        tuple2 = (4, 5, 6)
        result = array1 | tuple2
        self.assertEqual(result.to_python(), [1, 2, 3, 4, 5, 6])

    def test_or_operator_with_invalid_type(self):
        array1 = HakkaJsonArray([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = array1 | "invalid"

    def test_inplace_or_operator_with_hakka_json_array(self):
        array1 = HakkaJsonArray([1, 2, 3])
        array2 = HakkaJsonArray([4, 5, 6])
        array1 |= array2
        self.assertEqual(array1.to_python(), [1, 2, 3, 4, 5, 6])

    def test_inplace_or_operator_with_list(self):
        array1 = HakkaJsonArray([1, 2, 3])
        list2 = [4, 5, 6]
        array1 |= list2
        self.assertEqual(array1.to_python(), [1, 2, 3, 4, 5, 6])

    def test_inplace_or_operator_with_tuple(self):
        array1 = HakkaJsonArray([1, 2, 3])
        tuple2 = (4, 5, 6)
        array1 |= tuple2
        self.assertEqual(array1.to_python(), [1, 2, 3, 4, 5, 6])

    def test_inplace_or_operator_with_invalid_type(self):
        array1 = HakkaJsonArray([1, 2, 3])
        with self.assertRaises(TypeError):
            array1 |= "invalid"

class TestHakkaJsonArrayAdvanced(unittest.TestCase):
    def test_deeply_nested_arrays(self):
        # Create a deeply nested array
        depth = 1000
        nested = HakkaJsonArray()
        current = nested
        for _ in range(depth):
            new_array = HakkaJsonArray()
            current.append(new_array)
            current = new_array
        self.assertEqual(len(nested.to_python()), 1)
        self.assertIsInstance(nested[0], HakkaJsonArray)
        # Test access at depth
        current = nested
        for _ in range(depth):
            current = current[0]
        self.assertEqual(len(current), 0)

    def test_large_array_operations(self):
        large_size = 10000
        large_array = HakkaJsonArray()
        # Append large number of elements
        for i in range(large_size):
            large_array.append(HakkaJsonInt(i))
        self.assertEqual(len(large_array), large_size)
        # Test random access
        self.assertEqual(large_array[9999].to_python(), 9999)
        # Test serialization/deserialization
        serialized = large_array.dumps()
        deserialized = HakkaJsonArray.loads(serialized)
        self.assertEqual(deserialized.to_python(), list(range(large_size)))

    def test_compound_types(self):
        # Array containing objects and other arrays
        obj = HakkaJsonObject.from_python({"nested_key": "nested_value"})
        inner_array = HakkaJsonArray.from_python([1, 2, 3])
        compound_array = HakkaJsonArray([obj, inner_array, HakkaJsonBool(True)])
        self.assertEqual(
            compound_array.to_python(),
            [{"nested_key": "nested_value"}, [1, 2, 3], True],
        )
        # Test nested mutations
        # breakpoint()
        compound_array[0]["nested_key"] = "changed_value"
        self.assertEqual(compound_array.to_python()[0]["nested_key"], "changed_value")
        compound_array[1].append(4)
        self.assertEqual(compound_array.to_python()[1], [1, 2, 3, 4])

    def test_edge_cases_empty_and_single_element(self):
        empty_array = HakkaJsonArray()
        self.assertEqual(len(empty_array), 0)
        single_element = HakkaJsonArray([HakkaJsonInt(1)])
        self.assertEqual(len(single_element), 1)
        self.assertEqual(single_element[0].to_python(), 1)

    def test_off_by_one_errors(self):
        array = HakkaJsonArray([1, 2, 3])
        with self.assertRaises(IndexError):
            _ = array[3]  # Out of bounds
        with self.assertRaises(IndexError):
            _ = array[-4]  # Negative out of bounds
        # Ensure no off-by-one in len and indexing
        self.assertEqual(len(array), 3)
        self.assertEqual(array[2].to_python(), 3)

    def test_mutation_side_effects(self):
        array = HakkaJsonArray([1, 2, 3])
        copied = array.copy()
        copied.append(4)
        self.assertEqual(array.to_python(), [1, 2, 3])
        self.assertEqual(copied.to_python(), [1, 2, 3, 4])
        # Ensure deep copy if nested
        nested_array = HakkaJsonArray([array])
        nested_copied = nested_array.copy()
        nested_copied[0].append(5)
        self.assertEqual(nested_array.to_python(), [[1, 2, 3, 5]])
        self.assertEqual(nested_copied.to_python(), [[1, 2, 3, 5]])

    def test_iterators_with_modifications(self):
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        iterator = iter(array)
        self.assertEqual(next(iterator).to_python(), 1)
        array.pop()  # Modify during iteration
        self.assertEqual(next(iterator).to_python(), 2)
        with self.assertRaises(StopIteration):
            for _ in range(4):
                next(iterator)

    # def test_pickle_complex_structure(self):
    #     # Complex nested structures
    #     obj = HakkaJsonObject(
    #         {
    #             "numbers": HakkaJsonArray([HakkaJsonInt(i) for i in range(10)]),
    #             "details": HakkaJsonObject({"active": HakkaJsonBool(True)}),
    #         }
    #     )
    #     serialized = pickle.dumps(obj)
    #     deserialized = pickle.loads(serialized)
    #     self.assertEqual(deserialized.to_python(), obj.to_python())
    #     self.assertIsInstance(deserialized, HakkaJsonObject)
    #     self.assertIsInstance(deserialized["numbers"], HakkaJsonArray)
    #     self.assertIsInstance(deserialized["details"], HakkaJsonObject)

    def test_functional_operations(self):
        # Using map and filter with HakkaJsonArray
        array = HakkaJsonArray([1, 2, 3, 4, 5])
        # Map: multiply each element by 2
        mapped = HakkaJsonArray([HakkaJsonInt(x.to_python() * 2) for x in array])
        self.assertEqual(mapped.to_python(), [2, 4, 6, 8, 10])
        # Filter: keep even numbers
        filtered = HakkaJsonArray([x for x in array if x.to_python() % 2 == 0])
        self.assertEqual(filtered.to_python(), [2, 4])

    def test_boundary_conditions_large_numbers(self):
        # Test with very large integers
        large_int = 10**100
        with self.assertRaises(OverflowError):
            HakkaJsonArray([HakkaJsonInt(large_int), HakkaJsonInt(-large_int)])
        large_float = 10**100
        HakkaJsonArray([HakkaJsonFloat(large_float), HakkaJsonFloat(-large_float)])

    def test_dynamic_method_addition(self):
        # Ensure that methods are dynamically accessible and work as expected
        array = HakkaJsonArray([1, 2, 3])

        # Dynamically add a method (not recommended, but testing behavior)
        def custom_method(self):
            return "custom"

        HakkaJsonArray.custom_method = custom_method
        self.assertEqual(array.custom_method(), "custom")
        del HakkaJsonArray.custom_method

    def test_memory_leak_detection(self):
        # We do this because we have the handle_to_object() to hold the class object
        def one_batch():
            import sys

            # Create and delete a large array, ensure memory is reclaimed
            initial_memory = sys.getrefcount(HakkaJsonArray)
            for _ in range(1000):
                array = HakkaJsonArray([HakkaJsonInt(i) for i in range(1000)])
            import gc

            gc.collect()
            final_memory = sys.getrefcount(HakkaJsonArray)
            return initial_memory, final_memory

        initial_memory, final_memory = one_batch()
        initial_memory2, final_memory2 = one_batch()

        self.assertEqual(initial_memory, initial_memory2)
        self.assertEqual(final_memory, final_memory2)

    def test_hierarchical_structure_integrity(self):
        # Complex hierarchical structures
        obj = HakkaJsonObject(
            {
                "array1": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2)]),
                "object1": HakkaJsonObject(
                    {"key1": HakkaJsonString("value1"), "key2": HakkaJsonBool(False)}
                ),
            }
        )
        serialized = obj.dumps()
        deserialized = HakkaJsonObject.loads(serialized)
        self.assertEqual(deserialized.to_python(), obj.to_python())

    def test_compound_mutations(self):
        # Mutate nested structures and ensure integrity
        obj = HakkaJsonObject(
            {"nested_array": HakkaJsonArray([HakkaJsonInt(1), HakkaJsonInt(2)])}
        )
        obj["nested_array"].append(HakkaJsonInt(3))
        self.assertEqual(obj.to_python(), {"nested_array": [1, 2, 3]})
        obj["nested_array"][0] = HakkaJsonInt(10)
        self.assertEqual(obj.to_python(), {"nested_array": [10, 2, 3]})

    def test_cross_type_interactions(self):
        # Interact between different HakkaJson types
        array = HakkaJsonArray(
            [HakkaJsonString("hello"), HakkaJsonInt(42), HakkaJsonBool(True)]
        )
        self.assertIn(HakkaJsonString("hello"), array)
        self.assertIn(HakkaJsonInt(42), array)
        self.assertIn(HakkaJsonBool(True), array)
        self.assertNotIn(HakkaJsonString("world"), array)
        self.assertNotIn(HakkaJsonInt(0), array)
        self.assertNotIn(HakkaJsonBool(False), array)


if __name__ == "__main__":
    unittest.main()
