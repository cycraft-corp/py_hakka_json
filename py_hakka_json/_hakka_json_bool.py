#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HakkaJsonBool class definition.
Represents a JSON boolean value in HakkaJson.
Implements singleton pattern with HakkaJsonTrue and HakkaJsonFalse.
"""

from ctypes import byref, c_uint8, c_int32, c_uint64

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum


__all__ = ["HakkaJsonBool", "HakkaJsonTrue", "HakkaJsonFalse"]

# Dispatch functions for boolean manipulation
_create_bool_func = dispatch_table["CreateHakkaBool"]
_get_bool_func = dispatch_table["GetHakkaBool"]
_compare_func = dispatch_table["HakkaCompare"]
_hash_func = dispatch_table["HakkaHash"]


def setup_tf_handles(value: bool):
    c_hakka_handle = CHakkaHandle()
    c_bool_value = c_uint8(1 if value else 0)
    result = _create_bool_func(byref(c_hakka_handle), c_bool_value)
    if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
        raise RuntimeError("Failed to create HakkaJsonBool.")
    return c_hakka_handle


_true_handle = setup_tf_handles(True)
_false_handle = setup_tf_handles(False)


class HakkaJsonBool(HakkaJsonBase):
    """
    Represents a JSON boolean value in HakkaJson.
    Implements singleton pattern with HakkaJsonTrue and HakkaJsonFalse.
    """

    __slots__ = ()

    _internal_shared_bool_singleton = {}  # Class attribute to hold singleton instances

    def __new__(cls, value: bool):
        """
        Ensure that only one instance exists for True and False.
        """
        value = bool(value)
        if value not in cls._internal_shared_bool_singleton:
            instance = super(HakkaJsonBool, cls).__new__(cls)
            instance._initialize(value)
            cls._internal_shared_bool_singleton[value] = instance
        return cls._internal_shared_bool_singleton[value]

    @staticmethod
    def handle_to_tf(handle: CHakkaHandle) -> bool:
        """
        Convert a CHakkaHandle to a Python bool.
        """
        out_bool = c_uint8()
        result = _get_bool_func(handle, byref(out_bool))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to retrieve boolean value from HakkaJsonBool.")
        return bool(out_bool.value)

    def __init__(self, value: bool):  # pylint: disable=super-init-not-called
        """
        Initialize a HakkaJsonBool object.
        """

    @staticmethod
    def handle_to_instance(handle: CHakkaHandle) -> "HakkaJsonBool":
        """
        Convert a CHakkaHandle to a HakkaJsonBool instance.
        """
        tof = HakkaJsonBool.handle_to_tf(handle)
        return HakkaJsonTrue if tof else HakkaJsonFalse

    def _initialize(self, value: bool):
        """
        Internal method to initialize a HakkaJsonBool object.
        """
        if issubclass(type(value), HakkaJsonBase):
            value = self.handle_to_tf(value._c_hakka_handle)
        value = bool(value)
        if value:
            self._c_hakka_handle = _true_handle
        else:
            self._c_hakka_handle = _false_handle
        super().__init__(self._c_hakka_handle)

    def __bool__(self) -> bool:
        """
        Return the boolean value.
        """
        return self.to_python()

    def to_python(self) -> bool:
        """
        Convert the HakkaJsonBool to a Python bool.
        """
        out_bool = c_uint8()
        result = _get_bool_func(self._c_hakka_handle, byref(out_bool))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to retrieve boolean value from HakkaJsonBool.")
        return bool(out_bool.value)

    @staticmethod
    def from_python(value: bool) -> "HakkaJsonBool":
        """
        Create a HakkaJsonBool from a Python bool.
        """
        return HakkaJsonTrue if value else HakkaJsonFalse

    def _compare(self, other, op) -> bool:
        """
        Compare this HakkaJsonBool with another value using a comparison operation.

        Args:
            other (HakkaJsonBool or bool): The value to compare against.
            op (callable): The comparison operation.

        Returns:
            bool: The result of the comparison.
        """
        if isinstance(other, HakkaJsonBool):
            other_handle = other._c_hakka_handle  # pylint: disable=protected-access
        elif isinstance(other, bool):
            other_handle = HakkaJsonBool.from_python(other)._c_hakka_handle
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
        Get the hash of the HakkaJsonBool object.
        """
        hash_value = c_uint64()
        result = _hash_func(self._c_hakka_handle, byref(hash_value))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to compute hash for HakkaJsonBool.")
        return hash_value.value

    def __reduce__(self):
        """
        Support for pickle.
        """
        return (HakkaJsonBool.from_python, (self.to_python(),))

    def __repr__(self) -> str:
        return "HakkaJsonTrue" if self.to_python() else "HakkaJsonFalse"

    def __str__(self) -> str:
        return "True" if self.to_python() else "False"

    def __int__(self) -> int:
        return int(self.to_python())

    def __float__(self) -> float:
        return float(self.to_python())

    def __index__(self) -> int:
        return int(self.to_python())

    def __copy__(self) -> "HakkaJsonBool":
        return self

    def __deepcopy__(self, memo) -> "HakkaJsonBool":
        return self  # Singleton, no need to deepcopy

    def __getitem__(self, key):
        """
        Attempting to access items of a bool raises a TypeError.
        """
        raise TypeError("'bool' object is not subscriptable")

    def __len__(self):
        """
        Attempting to get the length of a bool raises a TypeError.
        """
        raise TypeError("'bool' object has no len()")

    def _arithmetic(self, other, op):
        """
        Perform an arithmetic operation and return a result.
        """
        if isinstance(other, HakkaJsonBool):
            other_value = other.to_python()
        elif isinstance(other, bool):
            other_value = other
        elif isinstance(other, (int, float)):
            other_value = other
        else:
            return NotImplemented
        return op(self.to_python(), other_value)

    # Arithmetic Operations
    def __add__(self, other):
        return self._arithmetic(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._arithmetic(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self._arithmetic(other, lambda x, y: x * y)

    def __truediv__(self, other):
        try:
            return self._arithmetic(other, lambda x, y: x / y)
        except ZeroDivisionError:
            raise ZeroDivisionError("division by zero") from None

    def __floordiv__(self, other):
        return self._arithmetic(other, lambda x, y: x // y)

    def __mod__(self, other):
        return self._arithmetic(other, lambda x, y: x % y)

    def __pow__(self, other, modulo=None):
        if modulo is not None:
            return self._arithmetic(other, lambda x, y: pow(x, y, modulo))
        return self._arithmetic(other, lambda x, y: pow(x, y))

    def __radd__(self, other):
        return self._arithmetic(other, lambda x, y: y + x)

    def __rsub__(self, other):
        return self._arithmetic(other, lambda x, y: y - x)

    def __rmul__(self, other):
        return self._arithmetic(other, lambda x, y: y * x)

    def __rtruediv__(self, other):
        try:
            return self._arithmetic(other, lambda x, y: y / x)
        except ZeroDivisionError:
            raise ZeroDivisionError("division by zero") from None

    def __rfloordiv__(self, other):
        return self._arithmetic(other, lambda x, y: y // x)

    def __rmod__(self, other):
        return self._arithmetic(other, lambda x, y: y % x)

    def __rpow__(self, other):
        return self._arithmetic(other, lambda x, y: pow(y, x))

    # Unary Operations
    def __neg__(self):
        return -self.to_python()

    def __pos__(self):
        return +self.to_python()

    def __abs__(self):
        return abs(self.to_python())

    def __invert__(self):
        return ~int(self.to_python())

    # Bitwise Operations
    def __and__(self, other):
        if isinstance(other, (HakkaJsonBool, bool, int)):
            return self.to_python() & other
        return NotImplemented

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        if isinstance(other, (HakkaJsonBool, bool, int)):
            return self.to_python() | other
        return NotImplemented

    def __ror__(self, other):
        return self.__or__(other)

    def __xor__(self, other):
        if isinstance(other, (HakkaJsonBool, bool, int)):
            return self.to_python() ^ other
        return NotImplemented

    def __rxor__(self, other):
        return self.__xor__(other)

    def __lshift__(self, other):
        if isinstance(other, int):
            return int(self.to_python()) << other
        return NotImplemented

    def __rlshift__(self, other):
        if isinstance(other, int):
            return other << int(self.to_python())
        return NotImplemented

    def __rshift__(self, other):
        if isinstance(other, int):
            return int(self.to_python()) >> other
        return NotImplemented

    def __rrshift__(self, other):
        if isinstance(other, int):
            return other >> int(self.to_python())
        return NotImplemented

    # Mathematical Methods
    def conjugate(self):
        """
        Booleans do not have a conjugate. Raises AttributeError.
        """
        raise AttributeError("'bool' object has no attribute 'conjugate'")

    def is_integer(self) -> bool:
        """
        Booleans are inherently integers (0 or 1).
        """
        return True

    def as_integer_ratio(self) -> tuple:
        """
        Returns a pair of integers whose ratio is exactly equal to the original boolean.
        """
        return (int(self.to_python()), 1)

    @classmethod
    def from_bytes(cls, source_bytes, byteorder, signed=False):
        value = bool(int.from_bytes(source_bytes, byteorder, signed=signed))
        return cls(True) if value else cls(False)

    def to_bytes(self, length: int, byteorder: str) -> bytes:
        """
        Convert the boolean to byte data.

        Args:
            length (int): Number of bytes (must be 1 for booleans).
            byteorder (str): Byte order ('big' or 'little').
            signed (bool): Not used for booleans.

        Returns:
            bytes: The byte representation of the boolean.

        Raises:
            ValueError: If length is not 1 or byteorder is invalid.
        """
        if length != 1:
            raise ValueError("Booleans require exactly 1 byte.")
        if byteorder not in ("big", "little"):
            raise ValueError("byteorder must be either 'big' or 'little'")
        return (1 if self.to_python() else 0).to_bytes(1, byteorder)

    # Representation and Pickling
    def __getnewargs__(self) -> tuple:
        """
        Support for pickle.
        """
        return (self.to_python(),)

    def __getstate__(self):
        """
        Get the state for pickling.
        """
        return self.to_python()

    def __setstate__(self, state):
        """
        Set the state from unpickling.
        """
        if not isinstance(state, bool):
            raise TypeError("State must be a bool.")
        self.__init__(state)

    # Formatting
    def __format__(self, format_spec: str) -> str:
        """
        Implements the format protocol.
        """
        return format(self.to_python(), format_spec)

    def __getformat__(self, format_type: str) -> str:
        """
        Returns the format of the bool.
        """
        if format_type == "bool":
            return "native"
        raise TypeError(f"unsupported format type {format_type!r}")

    # Additional Methods to Support Listed Methods
    def bit_count(self) -> int:
        """
        Return the number of set bits in the integer representation.
        """
        return int(self.to_python()).bit_count()

    def bit_length(self) -> int:
        """
        Return the number of bits necessary to represent the integer in binary.
        """
        return int(self.to_python()).bit_length()

    def denominator(self) -> int:
        """
        The denominator of a boolean is always 1.
        """
        return 1

    def numerator(self) -> int:
        """
        The numerator of a boolean is 1 for True and 0 for False.
        """
        return int(self.to_python())

    def real(self) -> "HakkaJsonBool":
        """
        Returns the real part of the boolean, which is itself.
        """
        return self

    def imag(self):
        """
        Booleans do not have an imaginary component. Raises AttributeError.
        """
        raise AttributeError("'bool' object has no attribute 'imag'")

    def __dir__(self):
        return super().__dir__() + [
            "__new__",
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
            "__index__",
            "__copy__",
            "__deepcopy__",
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
            "__and__",
            "__rand__",
            "__or__",
            "__ror__",
            "__xor__",
            "__rxor__",
            "__lshift__",
            "__rlshift__",
            "__rshift__",
            "__rrshift__",
            "conjugate",
            "is_integer",
            "as_integer_ratio",
            "from_bytes",
            "to_bytes",
            "__getnewargs__",
            "__getstate__",
            "__setstate__",
            "__format__",
            "__getformat__",
            "bit_count",
            "bit_length",
            "denominator",
            "numerator",
            "real",
            "imag",
        ]


# Singleton instances
HakkaJsonTrue = HakkaJsonBool(True)
HakkaJsonFalse = HakkaJsonBool(False)
