import unittest
from py_hakka_json._hakka_json_invalid import HakkaJsonInvalid
from py_hakka_json._hakka_json_base import HakkaJsonBase
from py_hakka_json._hakka_json_enum import HakkaJsonResultEnum
import pickle


class TestHakkaJsonInvalid(unittest.TestCase):
    def test_singleton(self):
        instance1 = HakkaJsonInvalid()
        instance2 = HakkaJsonInvalid()
        self.assertIs(instance1, instance2)

    def test_bool(self):
        instance = HakkaJsonInvalid()
        self.assertFalse(instance)

    def test_to_python(self):
        instance = HakkaJsonInvalid()
        self.assertIsNone(instance.to_python())

    def test_from_python(self):
        instance = HakkaJsonInvalid.from_python()
        self.assertIsInstance(instance, HakkaJsonInvalid)

    def test_equality(self):
        instance1 = HakkaJsonInvalid()
        instance2 = HakkaJsonInvalid()
        self.assertEqual(instance1, instance2)
        self.assertNotEqual(instance1, None)
        self.assertNotEqual(instance1, "invalid")

    def test_hash(self):
        instance = HakkaJsonInvalid()
        self.assertEqual(hash(instance), hash("HakkaJsonInvalid"))

    def test_repr(self):
        instance = HakkaJsonInvalid()
        self.assertEqual(repr(instance), "HakkaJsonInvalid")

    def test_str(self):
        instance = HakkaJsonInvalid()
        self.assertEqual(str(instance), "invalid")

    def test_pickle(self):
        instance = HakkaJsonInvalid()
        data = pickle.dumps(instance)
        loaded_instance = pickle.loads(data)
        self.assertIs(instance, loaded_instance)

    def test_dir(self):
        instance = HakkaJsonInvalid()
        expected_methods = [
            "__new__",
            "__init__",
            "__bool__",
            "to_python",
            "from_python",
            "__eq__",
            "__hash__",
            "__reduce__",
            "__repr__",
            "__str__",
            "__getnewargs__",
            "__getstate__",
            "__dir__",
        ]
        for method in expected_methods:
            self.assertIn(method, dir(instance))

    def test_isinstance(self):
        instance = HakkaJsonInvalid()
        self.assertIsInstance(instance, HakkaJsonInvalid)

    def test_subclass(self):
        self.assertTrue(issubclass(HakkaJsonInvalid, HakkaJsonBase))

    def test_singleton_thread_safety(self):
        import threading

        instances = []

        def create_instance():
            instances.append(HakkaJsonInvalid())

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for instance in instances:
            self.assertIs(instance, instances[0])

    def test_singleton_after_pickle(self):
        instance = HakkaJsonInvalid()
        data = pickle.dumps(instance)
        loaded_instance = pickle.loads(data)
        self.assertIs(instance, loaded_instance)
        self.assertIs(HakkaJsonInvalid(), loaded_instance)


if __name__ == "__main__":
    unittest.main()
