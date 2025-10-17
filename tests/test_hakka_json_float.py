import unittest
import pickle
from py_hakka_json._hakka_json_float import HakkaJsonFloat


class TestHakkaJsonFloat(unittest.TestCase):
    def test_initialization(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(float(hakka_float), value)

    def test_arithmetic_operations(self):
        a = HakkaJsonFloat(10.0)
        b = HakkaJsonFloat(20.0)
        self.assertEqual(a + b, HakkaJsonFloat(30.0))
        self.assertEqual(b - a, HakkaJsonFloat(10.0))
        self.assertEqual(a * b, HakkaJsonFloat(200.0))
        self.assertEqual(b // a, HakkaJsonFloat(2.0))
        self.assertEqual(b % a, HakkaJsonFloat(0.0))

    def test_comparison_operations(self):
        a = HakkaJsonFloat(10.0)
        b = HakkaJsonFloat(20.0)
        self.assertTrue(a < b)
        self.assertTrue(a <= b)
        self.assertTrue(b > a)
        self.assertTrue(b >= a)
        self.assertTrue(a != b)
        self.assertEqual(a, HakkaJsonFloat(10.0))

    def test_hash(self):
        value = 42.0
        hakka_float1 = HakkaJsonFloat(value)
        hakka_float2 = HakkaJsonFloat(value)
        self.assertEqual(hakka_float1, hakka_float2)

        hakka_float_hash1 = hash(hakka_float1)
        hakka_float_hash2 = hash(hakka_float2)
        self.assertEqual(hakka_float_hash1, hakka_float_hash2)

    def test_int(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(int(hakka_float), int(value))

    def test_setstate_valid(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        state = 84.0
        hakka_float.__setstate__(state)
        self.assertEqual(float(hakka_float), state)

    def test_setstate_invalid_type(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        with self.assertRaises(TypeError):
            hakka_float.__setstate__("invalid")

    def test_setstate_runtime_error(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        hakka_float.__setstate__(float("nan"))  # Ok, this is a valid float

    def test_initialization_with_float(self):
        value = 42.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(float(hakka_float), value)

    def test_initialization_with_HakkaJsonFloat(self):
        value = 100.0
        original = HakkaJsonFloat(value)
        copy = HakkaJsonFloat(original)
        self.assertEqual(float(copy), value)

    def test_initialization_with_invalid_type(self):
        with self.assertRaises(TypeError):
            HakkaJsonFloat("invalid")

    def test_immutable(self):
        hakka_float = HakkaJsonFloat(10.0)
        with self.assertRaises(AttributeError):
            hakka_float.some_attribute = 5

    def test_to_python(self):
        value = 123.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(hakka_float.to_python(), value)

    def test_negative_values(self):
        value = -50.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(float(hakka_float), value)

    def test_zero_value(self):
        value = 0.0
        hakka_float = HakkaJsonFloat(value)
        self.assertFalse(bool(hakka_float))
        self.assertEqual(float(hakka_float), value)

    def test_repr(self):
        value = 256.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(repr(hakka_float), f"HakkaJsonFloat({value})")

    def test_str(self):
        value = 512.0
        hakka_float = HakkaJsonFloat(value)
        self.assertEqual(str(hakka_float), str(value))

    def test_pickle(self):
        value = 64.0
        hakka_float = HakkaJsonFloat(value)
        serialized = pickle.dumps(hakka_float)
        deserialized = pickle.loads(serialized)
        self.assertEqual(deserialized, hakka_float)

    def test_true_division(self):
        a = HakkaJsonFloat(10.0)
        b = HakkaJsonFloat(2.0)
        self.assertEqual(a / b, 5.0)
        self.assertEqual(a / 2.0, 5.0)
        with self.assertRaises(ZeroDivisionError):
            a / HakkaJsonFloat(0.0)

    def test_reverse_arithmetic_operations(self):
        a = HakkaJsonFloat(10.0)
        b = 20.0
        self.assertEqual(b + a, HakkaJsonFloat(30.0))
        self.assertEqual(b - a, HakkaJsonFloat(10.0))
        self.assertEqual(b * a, HakkaJsonFloat(200.0))
        self.assertEqual(b // a, HakkaJsonFloat(2.0))
        self.assertEqual(b % a, HakkaJsonFloat(0.0))

    def test_reverse_true_division(self):
        a = HakkaJsonFloat(2.0)
        b = 10.0
        self.assertEqual(b / a, 5.0)
        with self.assertRaises(ZeroDivisionError):
            10.0 / HakkaJsonFloat(0.0)

    def test_power_operations(self):
        a = HakkaJsonFloat(2.0)
        b = HakkaJsonFloat(3.0)
        self.assertEqual(a**b, HakkaJsonFloat(8.0))
        self.assertEqual(a**3.0, HakkaJsonFloat(8.0))
        self.assertEqual(2.0**b, HakkaJsonFloat(8.0))

    def test_unary_operations(self):
        a = HakkaJsonFloat(10.0)
        self.assertEqual(-a, HakkaJsonFloat(-10.0))
        self.assertEqual(+a, HakkaJsonFloat(10.0))
        self.assertEqual(abs(a), HakkaJsonFloat(10.0))

    def test_integer_ratio(self):
        a = HakkaJsonFloat(10.0)
        self.assertEqual(a.as_integer_ratio(), (10, 1))

    def test_real_and_imag(self):
        a = HakkaJsonFloat(10.0)
        self.assertEqual(a.real(), a)
        with self.assertRaises(AttributeError):
            _ = a.imag()

    def test_is_integer(self):
        a = HakkaJsonFloat(10.0)
        b = HakkaJsonFloat(10.5)
        self.assertTrue(a.is_integer())
        self.assertFalse(b.is_integer())

    def test_as_integer_ratio(self):
        a = HakkaJsonFloat(10.0)
        self.assertEqual(a.as_integer_ratio(), (10, 1))

    def test_fromhex(self):
        hex_str = "0x1.8p1"
        hakka_float = HakkaJsonFloat.from_python(float.fromhex(hex_str))
        self.assertEqual(hakka_float, HakkaJsonFloat(3.0))

    def test_hex(self):
        a = HakkaJsonFloat(3.0)
        self.assertEqual(float.fromhex(a.hex()), 3.0)

    def test_ceil(self):
        a = HakkaJsonFloat(10.1)
        self.assertEqual(a.__ceil__(), HakkaJsonFloat(11.0))

    def test_floor(self):
        a = HakkaJsonFloat(10.9)
        self.assertEqual(a.__floor__(), HakkaJsonFloat(10.0))

    def test_trunc(self):
        a = HakkaJsonFloat(10.9)
        self.assertEqual(a.__trunc__(), HakkaJsonFloat(10.0))

    def test_round(self):
        a = HakkaJsonFloat(10.12345)
        self.assertEqual(a.__round__(2), HakkaJsonFloat(10.12))

    def test_format(self):
        a = HakkaJsonFloat(10.12345)
        self.assertEqual(format(a, ".2f"), "10.12")

    def test_getformat(self):
        a = HakkaJsonFloat(10.0)
        self.assertEqual(a.__getformat__("float"), "native")
        with self.assertRaises(TypeError):
            a.__getformat__("unsupported")

    def test_dir_all_are_in_dir(self):
        fun_list = dir(HakkaJsonFloat)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonFloat, name))


if __name__ == "__main__":
    unittest.main()
