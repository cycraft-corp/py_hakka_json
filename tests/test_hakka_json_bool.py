import unittest
import pickle
from py_hakka_json._hakka_json_bool import HakkaJsonBool, HakkaJsonTrue, HakkaJsonFalse
from py_hakka_json import (
    HakkaJsonInt,
    HakkaJsonString,
    HakkaJsonArray,
    HakkaJsonObject,
)


class TestHakkaJsonBool(unittest.TestCase):
    def test_initialization_true(self):
        bool_obj = HakkaJsonBool(True)
        self.assertIs(bool_obj, HakkaJsonTrue)
        self.assertTrue(bool(bool_obj))

    def test_initialization_false(self):
        bool_obj = HakkaJsonBool(False)
        self.assertIs(bool_obj, HakkaJsonFalse)
        self.assertFalse(bool(bool_obj))

    def test_singleton(self):
        true_obj1 = HakkaJsonBool(True)
        true_obj2 = HakkaJsonBool(True)
        false_obj1 = HakkaJsonBool(False)
        false_obj2 = HakkaJsonBool(False)
        self.assertIs(true_obj1, true_obj2)
        self.assertIs(false_obj1, false_obj2)
        self.assertIsNot(true_obj1, false_obj1)

    def test_to_python(self):
        self.assertTrue(HakkaJsonTrue.to_python())
        self.assertFalse(HakkaJsonFalse.to_python())

    def test_from_python(self):
        self.assertIs(HakkaJsonBool.from_python(True), HakkaJsonTrue)
        self.assertIs(HakkaJsonBool.from_python(False), HakkaJsonFalse)

    def test_equality(self):
        self.assertEqual(HakkaJsonTrue, HakkaJsonBool(True))
        self.assertEqual(HakkaJsonFalse, HakkaJsonBool(False))
        self.assertNotEqual(HakkaJsonTrue, HakkaJsonFalse)
        self.assertNotEqual(HakkaJsonTrue, HakkaJsonBool(False))

    def test_comparison_operations(self):
        self.assertTrue(HakkaJsonFalse < HakkaJsonTrue)
        self.assertTrue(HakkaJsonFalse <= HakkaJsonTrue)
        self.assertTrue(HakkaJsonTrue > HakkaJsonFalse)
        self.assertTrue(HakkaJsonTrue >= HakkaJsonFalse)
        self.assertTrue(HakkaJsonTrue != HakkaJsonFalse)
        self.assertTrue(HakkaJsonTrue == HakkaJsonBool(True))

    def test_hash(self):
        self.assertEqual(hash(HakkaJsonTrue.to_python()), hash(True))
        self.assertEqual(hash(HakkaJsonFalse.to_python()), hash(False))
        self.assertEqual(hash(HakkaJsonTrue), hash(HakkaJsonBool(True)))
        self.assertEqual(hash(HakkaJsonFalse), hash(HakkaJsonBool(False)))

    def test_pickle(self):
        serialized_true = pickle.dumps(HakkaJsonTrue)
        deserialized_true = pickle.loads(serialized_true)
        self.assertIs(deserialized_true, HakkaJsonTrue)

        serialized_false = pickle.dumps(HakkaJsonFalse)
        deserialized_false = pickle.loads(serialized_false)
        self.assertIs(deserialized_false, HakkaJsonFalse)

    def test_immutable(self):
        with self.assertRaises(AttributeError):
            HakkaJsonTrue.new_attribute = "test"

    def test_repr(self):
        self.assertEqual(repr(HakkaJsonTrue), "HakkaJsonTrue")
        self.assertEqual(repr(HakkaJsonFalse), "HakkaJsonFalse")

    def test_str(self):
        # breakpoint()
        self.assertEqual(str(HakkaJsonTrue), "True")
        self.assertEqual(str(HakkaJsonFalse), "False")

    def test_int_conversion(self):
        self.assertEqual(int(HakkaJsonTrue), 1)
        self.assertEqual(int(HakkaJsonFalse), 0)

    def test_float_conversion(self):
        self.assertEqual(float(HakkaJsonTrue), 1.0)
        self.assertEqual(float(HakkaJsonFalse), 0.0)

    def test_index_conversion(self):
        self.assertEqual(HakkaJsonTrue.__index__(), 1)
        self.assertEqual(HakkaJsonFalse.__index__(), 0)

    def test_arithmetic_operations(self):
        # breakpoint()
        self.assertEqual(HakkaJsonTrue + HakkaJsonFalse, 1)
        self.assertEqual(HakkaJsonTrue - HakkaJsonFalse, 1)
        self.assertEqual(HakkaJsonTrue * HakkaJsonFalse, 0)
        with self.assertRaises(ZeroDivisionError):
            HakkaJsonTrue / HakkaJsonFalse

    def test_bit_operations(self):
        self.assertEqual(HakkaJsonTrue & HakkaJsonTrue, True & True)
        self.assertEqual(HakkaJsonTrue | HakkaJsonFalse, True | False)
        self.assertEqual(HakkaJsonTrue ^ HakkaJsonFalse, True ^ False)
        self.assertEqual(~HakkaJsonTrue, ~1)

    def test_unary_operations(self):
        self.assertEqual(-HakkaJsonTrue, -1)
        self.assertEqual(+HakkaJsonFalse, +0)
        self.assertEqual(abs(HakkaJsonTrue), 1)
        with self.assertRaises(AttributeError):
            HakkaJsonTrue.conjugate()

    def test_as_integer_ratio(self):
        self.assertEqual(HakkaJsonTrue.as_integer_ratio(), (1, 1))
        self.assertEqual(HakkaJsonFalse.as_integer_ratio(), (0, 1))

    def test_is_integer(self):
        self.assertTrue(HakkaJsonTrue.is_integer())
        self.assertTrue(HakkaJsonFalse.is_integer())

    def test_bits_methods(self):
        self.assertEqual(HakkaJsonTrue.bit_count(), 1)
        self.assertEqual(HakkaJsonFalse.bit_count(), 0)
        self.assertEqual(HakkaJsonTrue.bit_length(), 1)
        self.assertEqual(HakkaJsonFalse.bit_length(), 0)

    def test_denominator_numerator(self):
        self.assertEqual(HakkaJsonTrue.denominator(), 1)
        self.assertEqual(HakkaJsonFalse.denominator(), 1)
        self.assertEqual(HakkaJsonTrue.numerator(), 1)
        self.assertEqual(HakkaJsonFalse.numerator(), 0)

    def test_real_imag(self):
        self.assertIs(HakkaJsonTrue.real(), HakkaJsonTrue)
        with self.assertRaises(AttributeError):
            HakkaJsonTrue.imag()

    def test_from_bytes(self):
        self.assertIs(HakkaJsonBool.from_bytes(b"\x01", "big"), HakkaJsonTrue)
        self.assertIs(HakkaJsonBool.from_bytes(b"\x00", "little"), HakkaJsonFalse)

    def test_to_bytes(self):
        self.assertEqual(HakkaJsonTrue.to_bytes(1, "big"), b"\x01")
        self.assertEqual(HakkaJsonFalse.to_bytes(1, "little"), b"\x00")
        with self.assertRaises(ValueError):
            HakkaJsonTrue.to_bytes(2, "big")
        with self.assertRaises(ValueError):
            HakkaJsonFalse.to_bytes(1, "invalid")

    def test_format(self):
        self.assertEqual(format(HakkaJsonTrue, "b"), format(True, "b"))
        self.assertEqual(format(HakkaJsonFalse, "b"), format(False, "b"))
        self.assertEqual(format(HakkaJsonTrue, ""), "True")
        self.assertEqual(format(HakkaJsonFalse, ""), "False")

    def test_getformat(self):
        self.assertEqual(HakkaJsonTrue.__getformat__("bool"), "native")
        self.assertEqual(HakkaJsonFalse.__getformat__("bool"), "native")
        with self.assertRaises(TypeError):
            HakkaJsonTrue.__getformat__("unsupported")

    def test_dir_all_are_in_dir(self):
        fun_list = dir(HakkaJsonBool)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonBool, name))


class TestHakkaJsonBoolAdvanced(unittest.TestCase):
    def test_boolean_logic_operations(self):
        true_obj = HakkaJsonBool(True)
        false_obj = HakkaJsonBool(False)
        # Logical AND
        and_result = true_obj and false_obj
        self.assertEqual(and_result, false_obj)
        # Logical OR
        or_result = true_obj or false_obj
        self.assertEqual(or_result, true_obj)
        # Logical NOT
        self.assertFalse(not true_obj)
        self.assertTrue(not false_obj)

    def test_boolean_arithmetic_operations(self):
        true_obj = HakkaJsonBool(True)
        false_obj = HakkaJsonBool(False)
        # Addition
        self.assertEqual(true_obj + true_obj, 2)
        self.assertEqual(true_obj + false_obj, 1)
        self.assertEqual(false_obj + false_obj, 0)
        # Multiplication
        self.assertEqual(true_obj * 10, 10)
        self.assertEqual(false_obj * 10, 0)
        # Subtraction
        self.assertEqual(true_obj - true_obj, 0)
        self.assertEqual(true_obj - false_obj, 1)
        self.assertEqual(false_obj - true_obj, -1)
        # Division
        with self.assertRaises(ZeroDivisionError):
            _ = true_obj / false_obj
        self.assertEqual(true_obj / true_obj, 1.0)

    def test_boolean_hash_equality(self):
        self.assertNotEqual(hash(HakkaJsonTrue), hash(True))
        self.assertNotEqual(hash(HakkaJsonFalse), hash(False))
        self.assertNotEqual(hash(HakkaJsonTrue), hash(HakkaJsonFalse))

    def test_pickling_bools(self):
        serialized_true = pickle.dumps(HakkaJsonTrue)
        deserialized_true = pickle.loads(serialized_true)
        self.assertIs(deserialized_true, HakkaJsonTrue)

        serialized_false = pickle.dumps(HakkaJsonFalse)
        deserialized_false = pickle.loads(serialized_false)
        self.assertIs(deserialized_false, HakkaJsonFalse)

    def test_functional_operations(self):
        # Using map and filter with HakkaJsonBool
        array = HakkaJsonArray(
            [HakkaJsonBool(True), HakkaJsonBool(False), HakkaJsonBool(True)]
        )
        # Map: invert each boolean
        inverted = HakkaJsonArray([HakkaJsonBool(not x.to_python()) for x in array])
        self.assertEqual(inverted.to_python(), [False, True, False])
        # Filter: keep only True
        filtered = HakkaJsonArray([x for x in array if x.to_python()])
        self.assertEqual(filtered.to_python(), [True, True])

    def test_cross_type_interactions(self):
        # Interact with other HakkaJson types
        true_obj = HakkaJsonBool(True)
        false_obj = HakkaJsonBool(False)
        hakka_int = HakkaJsonInt(1)
        hakka_str = HakkaJsonString("True")
        array = HakkaJsonArray([true_obj, false_obj, hakka_int, hakka_str])
        self.assertIn(true_obj, array)
        self.assertIn(false_obj, array)
        self.assertIn(hakka_int, array)
        self.assertIn(hakka_str, array)

    def test_invalid_operations(self):
        true_obj = HakkaJsonBool(True)
        with self.assertRaises(TypeError):
            true_obj + "string"

    def test_memory_leak_detection(self):
        import sys

        initial_memory = sys.getrefcount(HakkaJsonBool)
        for _ in range(1000):
            obj = HakkaJsonBool(True)
        import gc

        gc.collect()
        final_memory = sys.getrefcount(HakkaJsonBool)
        self.assertEqual(initial_memory, final_memory)

    def test_dir_all_are_in_dir(self):
        # Ensure all methods are accessible
        fun_list = dir(HakkaJsonBool)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonBool, name))

    def test_boolean_methods(self):
        # Test boolean-specific methods if any
        true_obj = HakkaJsonBool(True)
        false_obj = HakkaJsonBool(False)
        # Assuming methods like to_python, etc.
        self.assertTrue(true_obj.to_python())
        self.assertFalse(false_obj.to_python())

    def test_complex_serialization(self):
        # Serialize and deserialize objects containing booleans
        obj = HakkaJsonObject(
            {
                "is_active": HakkaJsonBool(True),
                "is_admin": HakkaJsonBool(False),
                "flags": HakkaJsonArray([HakkaJsonBool(True), HakkaJsonBool(True)]),
            }
        )
        serialized = obj.dumps()
        deserialized = HakkaJsonObject.loads(serialized)
        self.assertEqual(
            deserialized.to_python(),
            {"is_active": True, "is_admin": False, "flags": [True, True]},
        )


if __name__ == "__main__":
    unittest.main()
