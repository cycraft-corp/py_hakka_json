import unittest
from py_hakka_json import HakkaJsonNull, HakkaJsonArray, HakkaJsonObject
import pickle


class TestHakkaJsonNull(unittest.TestCase):
    def setUp(self):
        self.null_instance = HakkaJsonNull()

    def test_singleton_pattern(self):
        # Ensure that only one instance exists
        another_instance = HakkaJsonNull()
        self.assertIs(self.null_instance, another_instance)

    def test_to_python(self):
        # Ensure to_python returns None
        self.assertIsNone(self.null_instance.to_python())

    def test_from_python(self):
        # Ensure from_python returns the singleton instance
        self.assertIs(HakkaJsonNull.from_python(), self.null_instance)

    def test_bool(self):
        # Ensure bool conversion returns False
        self.assertFalse(bool(self.null_instance))

    def test_equality(self):
        # Ensure equality comparisons work correctly
        self.assertEqual(self.null_instance, HakkaJsonNull())
        self.assertEqual(self.null_instance, None)
        self.assertNotEqual(self.null_instance, "not null")

    def test_comparison(self):
        # Ensure comparison operations work correctly
        self.assertTrue(self.null_instance <= HakkaJsonNull())
        self.assertTrue(self.null_instance >= HakkaJsonNull())
        self.assertFalse(self.null_instance < HakkaJsonNull())
        self.assertFalse(self.null_instance > HakkaJsonNull())
        self.assertTrue(self.null_instance == HakkaJsonNull())
        self.assertFalse(self.null_instance != HakkaJsonNull())

    def test_hash(self):
        # Ensure hash computation works correctly
        self.assertEqual(hash(self.null_instance), hash(HakkaJsonNull()))

    def test_repr(self):
        # Ensure repr returns the correct string
        self.assertEqual(repr(self.null_instance), "HakkaJsonNull()")

    def test_str(self):
        # Ensure str returns the correct string
        self.assertEqual(str(self.null_instance), "null")

    def test_pickle_support(self):
        # Ensure pickling and unpickling works correctly

        pickled = pickle.dumps(self.null_instance)
        unpickled = pickle.loads(pickled)
        self.assertIs(unpickled, self.null_instance)


class TestHakkaJsonNullAdvanced(unittest.TestCase):
    def test_singleton_behavior(self):
        null1 = HakkaJsonNull()
        null2 = HakkaJsonNull()
        self.assertIs(null1, null2)
        self.assertEqual(null1, null2)

    def test_to_python(self):
        null = HakkaJsonNull()
        self.assertIsNone(null.to_python())

    def test_pickling_null(self):
        null = HakkaJsonNull()
        serialized = pickle.dumps(null)
        deserialized = pickle.loads(serialized)
        self.assertIs(deserialized, null)

    def test_invalid_operations(self):
        null = HakkaJsonNull()
        with self.assertRaises(TypeError):
            null + 1
        with self.assertRaises(TypeError):
            null * 2

    def test_length_behavior(self):
        null = HakkaJsonNull()
        self.assertEqual(len(null), 0)  # Assuming null has length 0

    def test_iterating_over_null(self):
        null = HakkaJsonNull()
        with self.assertRaises(TypeError):
            list(iter(null))  # Null is not iterable

    def test_dir_all_are_in_dir(self):
        # Ensure all methods are accessible
        fun_list = dir(HakkaJsonNull)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonNull, name))

    def test_memory_leak_detection(self):
        import sys

        initial_memory = sys.getrefcount(HakkaJsonNull)
        for _ in range(1000):
            null = HakkaJsonNull()
            self.assertIs(null, HakkaJsonNull())
        import gc

        gc.collect()
        final_memory = sys.getrefcount(HakkaJsonNull)
        self.assertEqual(initial_memory, final_memory)

    def test_contains_method(self):
        obj = HakkaJsonObject({"key": HakkaJsonNull()})
        self.assertIn("key", obj)
        self.assertEqual(obj["key"], HakkaJsonNull())

    def test_repr_and_str(self):
        null = HakkaJsonNull()
        self.assertEqual(repr(null), "HakkaJsonNull()")
        self.assertEqual(str(null), "null")

    def test_hash(self):
        null = HakkaJsonNull()
        # It is not possible to make HakkaJsonNull to be equal to None
        # self.assertEqual(hash(null), hash(None))
        self.assertEqual(hash(null), hash(HakkaJsonNull()))


if __name__ == "__main__":
    unittest.main()
