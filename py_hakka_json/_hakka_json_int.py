"""
HakkaJsonInt class definition.
"""

from ctypes import byref, c_int64, c_int32, c_uint64
from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum

__all__ = ["HakkaJsonInt"]

_create_int_func = dispatch_table["CreateHakkaInt"]
_get_int_func = dispatch_table["GetHakkaInt"]
_compare_func = dispatch_table["HakkaCompare"]
_hash_func = dispatch_table["HakkaHash"]


class HakkaJsonInt(HakkaJsonBase):
    """
    Represents a JSON integer value in HakkaJson.
    """

    __slots__ = ()

    @staticmethod
    def _construct(value: int) -> CHakkaHandle:
        """
        Construct a HakkaJsonInt object.

        Args:
            value (int): The integer value.

        Returns:
            CHakkaHandle: The handle to the HakkaJsonInt object.
        """
        if value > 9223372036854775807 or value < -9223372036854775808:
            raise OverflowError("Integer value out of range.")
        c_hakka_handle = CHakkaHandle()
        result = _create_int_func(byref(c_hakka_handle), value)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to create HakkaJsonInt.")
        return c_hakka_handle

    def __init__(self, value: int):
        """
        Initialize a HakkaJsonInt object.

        Args:
            value (int or HakkaJsonBase or HakkaJsonInt): The value to initialize.
        """
        if isinstance(value, HakkaJsonInt):
            self._c_hakka_handle = HakkaJsonInt._construct(value.to_python())
        elif isinstance(value, int):
            self._c_hakka_handle = HakkaJsonInt._construct(value)
        elif isinstance(value, HakkaJsonBase):
            if value.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_INT:
                raise TypeError("Unsupported type for HakkaJsonInt initialization.")
            out_int = c_int64()
            result = _get_int_func(value._c_hakka_handle, byref(out_int))
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                raise RuntimeError(
                    "Failed to retrieve integer value from HakkaJsonInt."
                )
            self._c_hakka_handle = HakkaJsonInt._construct(out_int.value)
        else:
            raise TypeError("Unsupported type for HakkaJsonInt initialization.")
        super().__init__(self._c_hakka_handle)

    def __bool__(self) -> bool:
        """
        Return the boolean value of the integer.

        Returns:
            bool: True if the integer is non-zero, False otherwise.
        """
        return self.to_python() != 0

    def to_python(self) -> int:
        """
        Convert the HakkaJsonInt to a Python integer.

        Returns:
            int: The integer value.
        """
        out_int = c_int64()
        result = _get_int_func(self._c_hakka_handle, byref(out_int))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to retrieve integer value from HakkaJsonInt.")
        return out_int.value

    @staticmethod
    def from_python(value: int) -> "HakkaJsonInt":
        """
        Create a HakkaJsonInt from a Python integer.

        Args:
            value (int): The integer value.

        Returns:
            HakkaJsonInt: The corresponding HakkaJsonInt object.
        """
        return HakkaJsonInt(value)

    def _compare(self, other, op) -> bool:
        """
        Compare this HakkaJsonInt with another value using a comparison operation.

        Args:
            other (HakkaJsonInt or int): The value to compare against.
            op (callable): The comparison operation.

        Returns:
            bool: The result of the comparison.
        """
        if isinstance(other, HakkaJsonInt):
            other_handle = other._c_hakka_handle
        elif isinstance(other, int):
            other_handle = CHakkaHandle()
            result = _create_int_func(byref(other_handle), other)
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                raise RuntimeError(
                    "Failed to create temporary HakkaJsonInt for comparison."
                )
        else:
            return NotImplemented

        comparison_result = c_int32()
        result = _compare_func(
            self._c_hakka_handle, other_handle, byref(comparison_result)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Comparison failed.")
        return op(comparison_result.value, 0)

    def __eq__(self, other) -> bool:
        return self._compare(other, lambda x, y: x == y)

    def __ge__(self, other) -> bool:
        return self._compare(other, lambda x, y: x >= y)

    def __gt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x > y)

    def __le__(self, other) -> bool:
        return self._compare(other, lambda x, y: x <= y)

    def __lt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x < y)

    def __ne__(self, other) -> bool:
        return self._compare(other, lambda x, y: x != y)

    def __hash__(self) -> int:
        """
        Get the hash of the HakkaJsonInt object.

        Returns:
            int: The hash value.
        """
        hash_value = c_uint64()
        result = _hash_func(self._c_hakka_handle, byref(hash_value))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to compute hash for HakkaJsonInt.")
        return hash_value.value

    def __reduce__(self):
        """
        Support for pickle.

        Returns:
            tuple: The reduction tuple.
        """
        return (HakkaJsonInt, (self.to_python(),))

    def __repr__(self) -> str:
        return f"HakkaJsonInt({self.to_python()})"

    def __str__(self) -> str:
        return str(self.to_python())

    def __int__(self) -> int:
        return self.to_python()

    def __float__(self) -> float:
        return float(self.to_python())

    def __set__(self, instance, value):
        """
        HakkaJsonInt objects are immutable. Attempting to set a value raises an error.

        Args:
            instance: The instance being set.
            value: The value to set.

        Raises:
            AttributeError: Always, since objects are immutable.
        """
        raise AttributeError("HakkaJsonInt objects are immutable")

    def __copy__(self) -> "HakkaJsonInt":
        """
        Create a shallow copy of the HakkaJsonInt object.

        Returns:
            HakkaJsonInt: The copied object.
        """
        return HakkaJsonInt(self.to_python())

    def __getitem__(self, key):
        """
        Attempting to access items of an integer raises a TypeError.

        Args:
            key: The key to access.

        Raises:
            TypeError: Always, since integers are not subscriptable.
        """
        raise TypeError("'int' object is not subscriptable")

    def __len__(self):
        """
        Attempting to get the length of an integer raises a TypeError.

        Raises:
            TypeError: Always, since integers have no length.
        """
        raise TypeError("'int' object has no len()")

    def _arithmetic(self, other, op) -> "HakkaJsonInt":
        """
        Perform an arithmetic operation and return a new HakkaJsonInt.

        Args:
            other (HakkaJsonInt or int): The value to operate with.
            op (callable): The arithmetic operation.

        Returns:
            HakkaJsonInt: The result of the operation.

        Raises:
            TypeError: If the other operand is of unsupported type.
        """
        if not isinstance(other, (HakkaJsonInt, int)):
            return NotImplemented
        other_value = other.to_python() if isinstance(other, HakkaJsonInt) else other
        return HakkaJsonInt(op(self.to_python(), other_value))

    def __add__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x + y)

    def __sub__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x - y)

    def __mul__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x * y)

    def __truediv__(self, other) -> float:
        """
        Perform true division and return a float.

        Args:
            other (HakkaJsonInt or int): The divisor.

        Returns:
            float: The result of the division.
        """
        if isinstance(other, HakkaJsonInt):
            other_value = other.to_python()
        elif isinstance(other, int):
            other_value = other
        else:
            return NotImplemented
        if other_value == 0:
            raise ZeroDivisionError("division by zero")
        return self.to_python() / other_value

    def __floordiv__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x // y)

    def __mod__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x % y)

    def __pow__(self, other, modulo=None) -> "HakkaJsonInt":
        if modulo is not None:
            if isinstance(other, (HakkaJsonInt, int)):
                return HakkaJsonInt(pow(self.to_python(), int(other), modulo))
            return NotImplemented
        return self._arithmetic(other, lambda x, y: pow(x, y))

    def __radd__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: y + x)

    def __rsub__(self, other) -> "HakkaJsonInt":
        if isinstance(other, (HakkaJsonInt, int)):
            return HakkaJsonInt(int(other) - self.to_python())
        return NotImplemented

    def __rmul__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: y * x)

    def __rtruediv__(self, other) -> float:
        """
        Perform true division with the HakkaJsonInt as the divisor.

        Args:
            other (HakkaJsonInt or int): The dividend.

        Returns:
            float: The result of the division.
        """
        if isinstance(other, (HakkaJsonInt, int)):
            other_value = int(other)
            if self.to_python() == 0:
                raise ZeroDivisionError("division by zero")
            return other_value / self.to_python()
        return NotImplemented

    def __rfloordiv__(self, other) -> "HakkaJsonInt":
        if isinstance(other, (HakkaJsonInt, int)):
            other_value = int(other)
            if self.to_python() == 0:
                raise ZeroDivisionError("floordiv by zero")
            return HakkaJsonInt(other_value // self.to_python())
        return NotImplemented

    def __rmod__(self, other) -> "HakkaJsonInt":
        if isinstance(other, (HakkaJsonInt, int)):
            other_value = int(other)
            if self.to_python() == 0:
                raise ZeroDivisionError("modulo by zero")
            return HakkaJsonInt(other_value % self.to_python())
        return NotImplemented

    def __rpow__(self, other) -> "HakkaJsonInt":
        if isinstance(other, (HakkaJsonInt, int)):
            return HakkaJsonInt(pow(int(other), self.to_python()))
        return NotImplemented

    def __neg__(self) -> "HakkaJsonInt":
        return HakkaJsonInt(-self.to_python())

    def __pos__(self) -> "HakkaJsonInt":
        return HakkaJsonInt(+self.to_python())

    def __abs__(self) -> "HakkaJsonInt":
        return HakkaJsonInt(abs(self.to_python()))

    def __invert__(self) -> "HakkaJsonInt":
        return HakkaJsonInt(~self.to_python())

    def __lshift__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x << y)

    def __rshift__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x >> y)

    def __and__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x & y)

    def __or__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x | y)

    def __xor__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: x ^ y)

    def __rand__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: y & x)

    def __ror__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: y | x)

    def __rxor__(self, other) -> "HakkaJsonInt":
        return self._arithmetic(other, lambda x, y: y ^ x)

    def bit_length(self) -> int:
        """
        Return the number of bits necessary to represent the integer in binary.

        Returns:
            int: The bit length.
        """
        return self.to_python().bit_length()

    def conjugate(self):
        """
        Integers do not have a conjugate. Raises AttributeError.

        Raises:
            AttributeError: Always, since integers have no conjugate.
        """
        raise AttributeError("'int' object has no attribute 'conjugate'")

    def denominator(self) -> int:
        """
        The denominator of an integer is always 1.

        Returns:
            int: The denominator, which is 1.
        """
        return 1

    @classmethod
    def from_bytes(self, source_bytes, byteorder, *, signed=False) -> "HakkaJsonInt":
        """
        Convert byte data to an integer.

        Args:
            source_bytes (bytes): The byte data.
            byteorder (str): The byte order ('big' or 'little').
            signed (bool): Whether two's complement is used to represent the integer.

        Returns:
            HakkaJsonInt: The resulting integer.
        """
        value = int.from_bytes(source_bytes, byteorder, signed=signed)
        return HakkaJsonInt(value)

    @property
    def imag(self):
        """
        Integers do not have an imaginary part. Raises AttributeError.

        Raises:
            AttributeError: Always, since integers have no imaginary part.
        """
        raise AttributeError("'int' object has no attribute 'imag'")

    @property
    def real(self) -> "HakkaJsonInt":
        """
        The real part of an integer is itself.

        Returns:
            HakkaJsonInt: The real part.
        """
        return self

    def is_integer(self) -> bool:
        """
        Always returns True for integers.

        Returns:
            bool: True.
        """
        return True

    def numerator(self) -> int:
        """
        The numerator of an integer is itself.

        Returns:
            int: The numerator.
        """
        return self.to_python()

    def to_bytes(self, length, byteorder, *, signed=False) -> bytes:
        """
        Convert the integer to byte data.

        Args:
            length (int): Number of bytes.
            byteorder (str): Byte order ('big' or 'little').
            signed (bool): Whether two's complement is used to represent the integer.

        Returns:
            bytes: The byte representation of the integer.
        """
        return self.to_python().to_bytes(length, byteorder, signed=signed)

    def __index__(self) -> int:
        """
        Return the integer value for indexing.

        Returns:
            int: The integer value.
        """
        return self.to_python()

    def as_integer_ratio(self) -> tuple:
        """
        Return the integer as a ratio of two integers.

        Returns:
            tuple: A tuple (numerator, denominator).
        """
        return (self.to_python(), 1)

    def __ceil__(self) -> "HakkaJsonInt":
        """
        Return the ceiling of the integer, which is itself.

        Returns:
            HakkaJsonInt: The ceiling value.
        """
        return self

    def __floor__(self) -> "HakkaJsonInt":
        """
        Return the floor of the integer, which is itself.

        Returns:
            HakkaJsonInt: The floor value.
        """
        return self

    def __round__(self, ndigits=None) -> "HakkaJsonInt":
        """
        Round the integer to the given number of digits.

        Args:
            ndigits (int, optional): Number of digits to round to.

        Returns:
            HakkaJsonInt: The rounded integer.
        """
        if ndigits is not None:
            return HakkaJsonInt(round(self.to_python(), ndigits))
        return HakkaJsonInt(round(self.to_python()))

    def __trunc__(self) -> "HakkaJsonInt":
        """
        Truncate the integer, which is itself.

        Returns:
            HakkaJsonInt: The truncated integer.
        """
        return self

    def __getnewargs__(self) -> tuple:
        """
        Support for pickle.

        Returns:
            tuple: Arguments for object creation.
        """
        return (self.to_python(),)

    def __getstate__(self):
        """
        Get the state for pickling.

        Returns:
            int: The integer value.
        """
        return self.to_python()

    def __setstate__(self, state):
        """
        Set the state during unpickling.

        Args:
            state (int): The integer value.
        """
        if not isinstance(state, int):
            raise TypeError("State must be an integer.")
        # Release the current handle
        if self._c_hakka_handle:
            dispatch_table["HakkaRelease"](byref(self._c_hakka_handle))
        # Create a new handle with the new state
        result = _create_int_func(byref(self._c_hakka_handle), state)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to set state for HakkaJsonInt.")

    def __sizeof__(self) -> int:
        """
        Return the size of the HakkaJsonInt object.

        Returns:
            int: The size in bytes.
        """
        return 8  # Assuming 64-bit integer

    def __setattr__(self, name, value):
        """
        Prevent setting attributes after initialization.

        Args:
            name (str): The attribute name.
            value: The attribute value.

        Raises:
            AttributeError: Always, since objects are immutable.
        """
        if name in self.__slots__:
            raise AttributeError("HakkaJsonInt objects are immutable")
        super().__setattr__(name, value)

    def __dir__(self):
        return super().__dir__() + [
            "_construct",
            "__init__",
            "__bool__",
            "to_python",
            "from_python",
            "_compare",
            "__eq__",
            "__ge__",
            "__gt__",
            "__le__",
            "__lt__",
            "__ne__",
            "__hash__",
            "__reduce__",
            "__repr__",
            "__str__",
            "__int__",
            "__float__",
            "__set__",
            "__copy__",
            "__getitem__",
            "__len__",
            "_arithmetic",
            "__add__",
            "__sub__",
            "__mul__",
            "__truediv__",
            "__floordiv__",
            "__mod__",
            "__pow__",
            "__radd__",
            "__rsub__",
            "__rmul__",
            "__rtruediv__",
            "__rfloordiv__",
            "__rmod__",
            "__rpow__",
            "__neg__",
            "__pos__",
            "__abs__",
            "__invert__",
            "__lshift__",
            "__rshift__",
            "__and__",
            "__or__",
            "__xor__",
            "__rand__",
            "__ror__",
            "__rxor__",
            "bit_length",
            "conjugate",
            "denominator",
            "from_bytes",
            "imag",
            "real",
            "is_integer",
            "numerator",
            "to_bytes",
            "__index__",
            "as_integer_ratio",
            "__ceil__",
            "__floor__",
            "__round__",
            "__trunc__",
            "__getnewargs__",
            "__getstate__",
            "__setstate__",
            "__sizeof__",
            "___setattr__",
            "__dir__",
        ]
