# _hakka_json_float.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HakkaJsonFloat class definition.
Represents a JSON float value in HakkaJson.
"""

from ctypes import byref, c_double, c_int32, c_uint64
from math import ceil, floor, trunc

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum


__all__ = ["HakkaJsonFloat"]

# Dispatch functions for float manipulation
_create_float_func = dispatch_table["CreateHakkaFloat"]
_get_float_func = dispatch_table["GetHakkaFloat"]
_compare_func = dispatch_table["HakkaCompare"]
_hash_func = dispatch_table["HakkaHash"]


class HakkaJsonFloat(HakkaJsonBase):
    """
    Represents a JSON float value in HakkaJson.
    """

    __slots__ = ()

    @staticmethod
    def _construct(value: float) -> CHakkaHandle:
        """
        Construct a HakkaJsonFloat object from a float value.

        Args:
            value (float): The float value.

        Returns:
            CHakkaHandle: The handle to the HakkaJsonFloat object.
        """
        c_hakka_handle = CHakkaHandle()
        result = _create_float_func(byref(c_hakka_handle), value)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to create HakkaJsonFloat.")
        return c_hakka_handle

    def __init__(self, value: float):
        """
        Initialize a HakkaJsonFloat object.

        Args:
            value (float or HakkaJsonBase or HakkaJsonFloat): The value to initialize.
        """
        if isinstance(value, HakkaJsonFloat):
            self._c_hakka_handle = HakkaJsonFloat._construct(value.to_python())
        elif isinstance(value, (int, float)):
            self._c_hakka_handle = HakkaJsonFloat._construct(float(value))
        elif isinstance(value, HakkaJsonBase):
            if value.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_FLOAT:
                raise TypeError("Invalid type for HakkaJsonFloat initialization.")
            out_float = c_double()
            result = _get_float_func(value._c_hakka_handle, byref(out_float))
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                raise RuntimeError(
                    "Failed to retrieve float value from HakkaJsonFloat."
                )
            self._c_hakka_handle = HakkaJsonFloat._construct(out_float.value)
        else:
            raise TypeError("Invalid type for HakkaJsonFloat initialization.")
        super().__init__(self._c_hakka_handle)

    def __bool__(self) -> bool:
        """
        Return the boolean value of the float.

        Returns:
            bool: False if the float is 0.0, True otherwise.
        """
        return self.to_python() != 0.0

    def to_python(self) -> float:
        """
        Convert the HakkaJsonFloat to a Python float.

        Returns:
            float: The float value.
        """
        out_float = c_double()
        result = _get_float_func(self._c_hakka_handle, byref(out_float))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to retrieve float value from HakkaJsonFloat.")
        return out_float.value

    @staticmethod
    def from_python(value: float) -> "HakkaJsonFloat":
        """
        Create a HakkaJsonFloat from a Python float.

        Args:
            value (float): The float value.

        Returns:
            HakkaJsonFloat: The corresponding HakkaJsonFloat object.
        """
        return HakkaJsonFloat(value)

    def _compare(self, other, op) -> bool:
        """
        Compare this HakkaJsonFloat with another value using a comparison operation.

        Args:
            other (HakkaJsonFloat or float): The value to compare against.
            op (callable): The comparison operation.

        Returns:
            bool: The result of the comparison.
        """
        if isinstance(other, HakkaJsonFloat):
            other_handle = other._c_hakka_handle  # pylint: disable=protected-access
        elif isinstance(other, (int, float)):
            other_handle = CHakkaHandle()
            # Create a temporary HakkaJsonFloat for comparison
            temp_float = HakkaJsonFloat.from_python(float(other))
            other_handle = (
                temp_float._c_hakka_handle  # pylint: disable=protected-access
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
        Get the hash of the HakkaJsonFloat object.

        Returns:
            int: The hash value.
        """
        hash_value = c_uint64()
        result = _hash_func(self._c_hakka_handle, byref(hash_value))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to compute hash for HakkaJsonFloat.")
        return hash_value.value

    def __reduce__(self):
        """
        Support for pickle.

        Returns:
            tuple: The reduction tuple.
        """
        return (HakkaJsonFloat, (self.to_python(),))

    def __repr__(self) -> str:
        return f"HakkaJsonFloat({self.to_python()})"

    def __str__(self) -> str:
        return str(self.to_python())

    def __float__(self) -> float:
        return self.to_python()

    def __int__(self) -> int:
        return int(self.to_python())

    def __set__(self, instance, value):
        """
        HakkaJsonFloat objects are immutable. Attempting to set a value raises an error.

        Args:
            instance: The instance being set.
            value: The value to set.

        Raises:
            AttributeError: Always, since objects are immutable.
        """
        raise AttributeError("HakkaJsonFloat objects are immutable")

    def __copy__(self) -> "HakkaJsonFloat":
        """
        Create a shallow copy of the HakkaJsonFloat object.

        Returns:
            HakkaJsonFloat: The copied object.
        """
        return HakkaJsonFloat(self.to_python())

    def __deepcopy__(self, memo) -> "HakkaJsonFloat":
        """
        Deep copy the HakkaJsonFloat object.

        Args:
            memo (dict): The memoization dictionary.

        Returns:
            HakkaJsonFloat: The copied object.
        """
        return self  # Float is immutable, return self

    def __getitem__(self, key):
        """
        Attempting to access items of a float raises a TypeError.

        Args:
            key: The key to access.

        Raises:
            TypeError: Always, since floats are not subscriptable.
        """
        raise TypeError("'float' object is not subscriptable")

    def __len__(self):
        """
        Attempting to get the length of a float raises a TypeError.

        Raises:
            TypeError: Always, since floats have no length.
        """
        raise TypeError("'float' object has no len()")

    def _arithmetic(self, other, op) -> "HakkaJsonFloat":
        """
        Perform an arithmetic operation and return a new HakkaJsonFloat.

        Args:
            other (HakkaJsonFloat or float): The value to operate with.
            op (callable): The arithmetic operation.

        Returns:
            HakkaJsonFloat: The result of the operation.

        Raises:
            TypeError: If the other operand is of unsupported type.
        """
        if isinstance(other, HakkaJsonFloat):
            other_value = other.to_python()
        elif isinstance(other, (int, float)):
            other_value = float(other)
        else:
            return NotImplemented
        result_value = op(self.to_python(), other_value)
        return HakkaJsonFloat(result_value)

    def __add__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: x + y)

    def __sub__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: x - y)

    def __mul__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: x * y)

    def __truediv__(self, other) -> float:
        """
        Perform true division and return a float.

        Args:
            other (HakkaJsonFloat or float): The divisor.

        Returns:
            float: The result of the division.

        Raises:
            ZeroDivisionError: If dividing by zero.
            TypeError: If the other operand is of unsupported type.
        """
        if isinstance(other, HakkaJsonFloat):
            other_value = other.to_python()
        elif isinstance(other, (int, float)):
            other_value = float(other)
        else:
            return NotImplemented
        if other_value == 0.0:
            raise ZeroDivisionError("division by zero")
        return self.to_python() / other_value

    def __floordiv__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: x // y)

    def __mod__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: x % y)

    def __pow__(self, other, modulo=None) -> "HakkaJsonFloat":
        if modulo is not None:
            if isinstance(other, (HakkaJsonFloat, int, float)):
                return HakkaJsonFloat(pow(self.to_python(), float(other), modulo))
            return NotImplemented
        return self._arithmetic(other, lambda x, y: pow(x, y))

    def __radd__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: y + x)

    def __rsub__(self, other) -> "HakkaJsonFloat":
        if isinstance(other, (HakkaJsonFloat, int, float)):
            return HakkaJsonFloat(float(other) - self.to_python())
        return NotImplemented

    def __rmul__(self, other) -> "HakkaJsonFloat":
        return self._arithmetic(other, lambda x, y: y * x)

    def __rtruediv__(self, other) -> float:
        """
        Perform true division with the HakkaJsonFloat as the divisor.

        Args:
            other (HakkaJsonFloat or float): The dividend.

        Returns:
            float: The result of the division.

        Raises:
            ZeroDivisionError: If dividing by zero.
            TypeError: If the other operand is of unsupported type.
        """
        if isinstance(other, (HakkaJsonFloat, int, float)):
            other_value = float(other)
            divisor = self.to_python()
            if divisor == 0.0:
                raise ZeroDivisionError("division by zero")
            return other_value / divisor
        return NotImplemented

    def __rfloordiv__(self, other) -> "HakkaJsonFloat":
        if isinstance(other, (HakkaJsonFloat, int, float)):
            other_value = float(other)
            divisor = self.to_python()
            if divisor == 0.0:
                raise ZeroDivisionError("floordiv by zero")
            return HakkaJsonFloat(other_value // divisor)
        return NotImplemented

    def __rmod__(self, other) -> "HakkaJsonFloat":
        if isinstance(other, (HakkaJsonFloat, int, float)):
            other_value = float(other)
            divisor = self.to_python()
            if divisor == 0.0:
                raise ZeroDivisionError("modulo by zero")
            return HakkaJsonFloat(other_value % divisor)
        return NotImplemented

    def __rpow__(self, other) -> "HakkaJsonFloat":
        if isinstance(other, (HakkaJsonFloat, int, float)):
            return HakkaJsonFloat(pow(float(other), self.to_python()))
        return NotImplemented

    # Unary Operations
    def __neg__(self) -> "HakkaJsonFloat":
        return HakkaJsonFloat(-self.to_python())

    def __pos__(self) -> "HakkaJsonFloat":
        return HakkaJsonFloat(+self.to_python())

    def __abs__(self) -> "HakkaJsonFloat":
        return HakkaJsonFloat(abs(self.to_python()))

    def __invert__(self):
        """
        Bitwise inversion is not applicable to floats. Raises AttributeError.

        Raises:
            AttributeError: Always, since bitwise inversion is not applicable.
        """
        raise AttributeError("'float' object has no attribute '__invert__'")

    # Mathematical Methods
    def conjugate(self):
        """
        Not applicable for floats.

        Raises:
            AttributeError: Always, since conjugate is not applicable.
        """
        raise AttributeError("'float' object has no attribute 'conjugate'")

    def is_integer(self) -> bool:
        """
        Checks if the float is an integer.

        Returns:
            bool: True if the float is an integer, False otherwise.
        """
        return self.to_python().is_integer()

    def as_integer_ratio(self) -> tuple:
        """
        Returns a pair of integers whose ratio is exactly equal to the original float
        and with a positive denominator.

        Returns:
            tuple: A tuple (numerator, denominator).
        """
        return self.to_python().as_integer_ratio()

    def fromhex(self, hexstr: str) -> "HakkaJsonFloat":
        """
        Converts a hexadecimal string to a float.

        Args:
            hexstr (str): The hexadecimal string.

        Returns:
            HakkaJsonFloat: The corresponding HakkaJsonFloat instance.
        """
        return HakkaJsonFloat.from_python(float.fromhex(hexstr))

    def hex(self) -> str:
        """
        Returns a hexadecimal string representation of the float.

        Returns:
            str: The hexadecimal representation.
        """
        return self.to_python().hex()

    def real(self) -> "HakkaJsonFloat":
        """
        Returns the real part of the float, which is itself.

        Returns:
            HakkaJsonFloat: The real part.
        """
        return self

    def imag(self):
        """
        Not applicable for floats.

        Raises:
            AttributeError: Always, since floats do not have an imaginary component.
        """
        raise AttributeError("'float' object has no attribute 'imag'")

    # Mathematical Operations
    def __ceil__(self) -> "HakkaJsonFloat":
        """
        Returns the smallest integer greater than or equal to the float.

        Returns:
            HakkaJsonFloat: The ceiling of the float.
        """
        return HakkaJsonFloat(ceil(self.to_python()))

    def __floor__(self) -> "HakkaJsonFloat":
        """
        Returns the largest integer less than or equal to the float.

        Returns:
            HakkaJsonFloat: The floor of the float.
        """
        return HakkaJsonFloat(floor(self.to_python()))

    def __trunc__(self) -> "HakkaJsonFloat":
        """
        Returns the truncated integer value of the float.

        Returns:
            HakkaJsonFloat: The truncated value.
        """
        return HakkaJsonFloat(trunc(self.to_python()))

    def __round__(self, ndigits=None) -> "HakkaJsonFloat":
        """
        Rounds the float to the given number of digits.

        Args:
            ndigits (int, optional): The number of digits to round to.

        Returns:
            HakkaJsonFloat: The rounded value.
        """
        return HakkaJsonFloat(round(self.to_python(), ndigits))

    # Additional Methods
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
            float: The float value.
        """
        return self.to_python()

    def __setstate__(self, state):
        """
        Set the state from unpickling.

        Args:
            state (float): The float value.
        """
        if not isinstance(state, float):
            raise TypeError("State must be a float.")
        # Release the current handle
        if self._c_hakka_handle:
            dispatch_table["HakkaRelease"](byref(self._c_hakka_handle))
        # Create a new handle with the new state
        result = _create_float_func(byref(self._c_hakka_handle), state)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to set state for HakkaJsonFloat.")

    def __sizeof__(self) -> int:
        """
        Return the memory size of the HakkaJsonFloat object.

        Returns:
            int: The size in bytes.
        """
        return 24  # Example size; adjust based on actual memory usage

    def __setattr__(self, name, value):
        """
        Prevent setting attributes after initialization to ensure immutability.

        Args:
            name (str): The attribute name.
            value: The attribute value.

        Raises:
            AttributeError: If attempting to set any attribute.
        """
        if name in self.__slots__:
            raise AttributeError("HakkaJsonFloat objects are immutable")
        super().__setattr__(name, value)

    def __format__(self, format_spec: str) -> str:
        """
        Implements the format protocol.

        Args:
            format_spec (str): The format specification.

        Returns:
            str: The formatted string.
        """
        return format(self.to_python(), format_spec)

    def __getformat__(self, format_type: str) -> str:
        """
        Returns the format of the float.

        Args:
            format_type (str): The format type ('float').

        Returns:
            str: The format string.

        Raises:
            TypeError: If the format type is not supported.
        """
        if format_type == "float":
            return "native"
        raise TypeError(f"unsupported format type {format_type!r}")

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
            "__float__",
            "__int__",
            "__set__",
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
            "conjugate",
            "is_integer",
            "as_integer_ratio",
            "fromhex",
            "hex",
            "real",
            "imag",
            "__ceil__",
            "__floor__",
            "__trunc__",
            "__round__",
            "__getnewargs__",
            "__getstate__",
            "__setstate__",
            "__sizeof__",
            "__setattr__",
            "__format__",
            "__getformat__",
            "__dir__",
        ]
