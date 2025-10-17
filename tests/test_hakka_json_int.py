import unittest
import pickle
from py_hakka_json._hakka_json_int import HakkaJsonInt


class TestHakkaJsonInt(unittest.TestCase):
    def test_initialization(self):
        value = 42
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(int(hakka_int), value)

    def test_arithmetic_operations(self):
        a = HakkaJsonInt(10)
        b = HakkaJsonInt(20)
        self.assertEqual(a + b, HakkaJsonInt(30))
        self.assertEqual(b - a, HakkaJsonInt(10))
        self.assertEqual(a * b, HakkaJsonInt(200))
        self.assertEqual(b // a, HakkaJsonInt(2))
        self.assertEqual(b % a, HakkaJsonInt(0))

    def test_comparison_operations(self):
        a = HakkaJsonInt(10)
        b = HakkaJsonInt(20)
        self.assertTrue(a < b)
        self.assertTrue(a <= b)
        self.assertTrue(b > a)
        self.assertTrue(b >= a)
        self.assertTrue(a != b)
        self.assertEqual(a, HakkaJsonInt(10))

    def test_hash(self):
        value = 42
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(hash(hakka_int), hash(value))

    def test_initialization_with_int(self):
        value = 42
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(int(hakka_int), value)

    def test_initialization_with_HakkaJsonInt(self):
        value = 100
        original = HakkaJsonInt(value)
        copy = HakkaJsonInt(original)
        self.assertEqual(int(copy), value)

    def test_initialization_with_invalid_type(self):
        with self.assertRaises(TypeError):
            HakkaJsonInt("invalid")

    def test_immutable(self):
        hakka_int = HakkaJsonInt(10)
        with self.assertRaises(AttributeError):
            hakka_int.some_attribute = 5

    def test_to_python(self):
        value = 123
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(hakka_int.to_python(), value)

    def test_negative_values(self):
        value = -50
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(int(hakka_int), value)

    def test_zero_value(self):
        value = 0
        hakka_int = HakkaJsonInt(value)
        self.assertFalse(bool(hakka_int))
        self.assertEqual(int(hakka_int), value)

    def test_bit_length(self):
        value = 16
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(hakka_int.bit_length(), value.bit_length())

    def test_repr(self):
        value = 256
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(repr(hakka_int), f"HakkaJsonInt({value})")

    def test_str(self):
        value = 512
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(str(hakka_int), str(value))

    def test_pickle(self):
        value = 64
        hakka_int = HakkaJsonInt(value)
        serialized = pickle.dumps(hakka_int)
        deserialized = pickle.loads(serialized)
        self.assertEqual(deserialized, hakka_int)

    def test_from_bytes(self):
        value = 1024
        hakka_int = HakkaJsonInt.from_bytes(
            source_bytes=value.to_bytes(2, byteorder="big"), byteorder="big"
        )
        self.assertEqual(int(hakka_int), value)

    def test_to_bytes(self):
        value = 2048
        hakka_int = HakkaJsonInt(value)
        self.assertEqual(
            hakka_int.to_bytes(2, byteorder="big"), value.to_bytes(2, byteorder="big")
        )

    def test_true_division(self):
        a = HakkaJsonInt(10)
        b = HakkaJsonInt(2)
        self.assertEqual(a / b, 5.0)
        self.assertEqual(a / 2, 5.0)
        with self.assertRaises(ZeroDivisionError):
            a / HakkaJsonInt(0)

    def test_reverse_arithmetic_operations(self):
        a = HakkaJsonInt(10)
        b = 20
        self.assertEqual(b + a, HakkaJsonInt(30))
        self.assertEqual(b - a, HakkaJsonInt(10))
        self.assertEqual(b * a, HakkaJsonInt(200))
        self.assertEqual(b // a, HakkaJsonInt(2))
        self.assertEqual(b % a, HakkaJsonInt(0))

    def test_reverse_true_division(self):
        a = HakkaJsonInt(2)
        b = 10
        self.assertEqual(b / a, 5.0)
        with self.assertRaises(ZeroDivisionError):
            10 / HakkaJsonInt(0)

    def test_power_operations(self):
        a = HakkaJsonInt(2)
        b = HakkaJsonInt(3)
        self.assertEqual(a**b, HakkaJsonInt(8))
        self.assertEqual(a**3, HakkaJsonInt(8))
        self.assertEqual(2**b, HakkaJsonInt(8))

    def test_unary_operations(self):
        a = HakkaJsonInt(10)
        self.assertEqual(-a, HakkaJsonInt(-10))
        self.assertEqual(+a, HakkaJsonInt(10))
        self.assertEqual(abs(a), HakkaJsonInt(10))
        self.assertEqual(~a, HakkaJsonInt(~10))

    def test_bitwise_operations(self):
        a = HakkaJsonInt(10)
        b = HakkaJsonInt(4)
        self.assertEqual(a & b, HakkaJsonInt(10 & 4))
        self.assertEqual(a | b, HakkaJsonInt(10 | 4))
        self.assertEqual(a ^ b, HakkaJsonInt(10 ^ 4))
        self.assertEqual(a << 2, HakkaJsonInt(10 << 2))
        self.assertEqual(a >> 2, HakkaJsonInt(10 >> 2))

    def test_reverse_bitwise_operations(self):
        a = HakkaJsonInt(10)
        b = 4
        self.assertEqual(b & a, HakkaJsonInt(4 & 10))
        self.assertEqual(b | a, HakkaJsonInt(4 | 10))
        self.assertEqual(b ^ a, HakkaJsonInt(4 ^ 10))
        # self.assertEqual(b << a, HakkaJsonInt(4 << 10)) # Python does not support this operation
        # self.assertEqual(b >> a, HakkaJsonInt(4 >> 10)) # Python does not support this operation

    def test_integer_ratio(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.as_integer_ratio(), (10, 1))

    def test_real_and_imag(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.real, a)
        with self.assertRaises(AttributeError):
            _ = a.imag

    def test_conjugate(self):
        a = HakkaJsonInt(10)
        with self.assertRaises(AttributeError):
            a.conjugate()

    def test_denominator(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.denominator(), 1)

    def test_numerator(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.numerator(), 10)

    def test_is_integer(self):
        a = HakkaJsonInt(10)
        self.assertTrue(a.is_integer())

    def test_ceil(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__ceil__(), a)

    def test_floor(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__floor__(), a)

    def test_round(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__round__(), a)
        self.assertEqual(a.__round__(1), a)

    def test_trunc(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__trunc__(), a)

    def test_getnewargs(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__getnewargs__(), (10,))

    def test_getstate(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__getstate__(), 10)

    def test_setstate(self):
        a = HakkaJsonInt(10)
        a.__setstate__(20)
        self.assertEqual(a.to_python(), 20)

    def test_sizeof(self):
        a = HakkaJsonInt(10)
        self.assertEqual(a.__sizeof__(), 8)

    def test_setattr(self):
        a = HakkaJsonInt(10)
        with self.assertRaises(AttributeError):
            a.some_attribute = 5

    def test_dir_all_are_in_dir(self):
        fun_list = dir(HakkaJsonInt)
        for name in fun_list:
            self.assertTrue(hasattr(HakkaJsonInt, name))


if __name__ == "__main__":
    unittest.main()
