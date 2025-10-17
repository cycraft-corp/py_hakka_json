#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HakkaJsonNull class definition.
Represents a JSON null value in HakkaJson.
Implements singleton pattern for efficiency.
"""

from ctypes import byref, c_int32, c_uint64

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum


__all__ = ["HakkaJsonNull"]


# Dispatch functions for null manipulation
_create_null_func = dispatch_table["CreateHakkaNull"]
_compare_func = dispatch_table["HakkaCompare"]
_hash_func = dispatch_table["HakkaHash"]


class HakkaJsonNull(HakkaJsonBase):
    """
    Represents a JSON null value in HakkaJson.
    Implements singleton pattern.
    """

    __slots__ = ("_initialized",)

    _instance = None  # Class attribute to hold the singleton instance

    def __new__(cls):
        """
        Ensure that only one instance exists for HakkaJsonNull.
        """
        if cls._instance is None:
            instance = super(HakkaJsonNull, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        """
        Initialize the HakkaJsonNull object.
        """
        if not hasattr(self, "_initialized"):
            c_hakka_handle = CHakkaHandle()
            result = _create_null_func(byref(c_hakka_handle))
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                raise RuntimeError("Failed to create HakkaJsonNull.")
            super().__init__(c_hakka_handle)
            self._initialized = True

    def __bool__(self) -> bool:
        """
        Return False for null.
        """
        return False

    def to_python(self):
        """
        Convert the HakkaJsonNull to Python's None.
        """
        # Since null corresponds to None in Python, we return None
        return None

    @staticmethod
    def from_python():
        """
        Return the singleton instance of HakkaJsonNull.
        """
        return HakkaJsonNull()

    def _compare(self, other, op) -> bool:
        """
        Compare this HakkaJsonNull with another value using a comparison operation.

        Args:
            other (HakkaJsonNull or None): The value to compare against.
            op (callable): The comparison operation.

        Returns:
            bool: The result of the comparison.
        """
        if isinstance(other, HakkaJsonNull):
            other_handle = other._c_hakka_handle  # pylint: disable=protected-access
        elif other is None:
            other_handle = (
                HakkaJsonNull.from_python()._c_hakka_handle  # pylint: disable=protected-access
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
        Get the hash of the HakkaJsonNull object.
        Typically, hash(None) is used.
        """
        hash_value = c_uint64()
        result = _hash_func(self._c_hakka_handle, byref(hash_value))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to compute hash for HakkaJsonNull.")
        return hash_value.value
    
    def __len__(self) -> int:
        """
        Get the length of the HakkaJsonNull object.
        """
        return 0

    def __reduce__(self):
        """
        Support for pickle.
        """
        return (HakkaJsonNull.from_python, ())

    def __repr__(self) -> str:
        return "HakkaJsonNull()"

    def __str__(self) -> str:
        return "null"

    def __getnewargs__(self) -> tuple:
        """
        Support for pickle.
        """
        return ()

    def __getstate__(self):
        """
        Get the state for pickling.
        """
        return self.to_python()

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
            "__getnewargs__",
            "__getstate__",
            "__dir__",
        ]
