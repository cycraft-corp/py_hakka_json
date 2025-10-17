#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HakkaJsonInvalid class definition.
Represents an invalid JSON value in HakkaJson.
Implements singleton pattern for efficiency.
"""

from ctypes import byref

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum


__all__ = ["HakkaJsonInvalid"]


# Dispatch function for creating an invalid JSON value
_create_invalid_func = dispatch_table["CreateHakkaInvalid"]


class HakkaJsonInvalid(HakkaJsonBase):
    """
    Represents an invalid JSON value in HakkaJson.
    Implements singleton pattern.
    """

    __slots__ = ("_initialized",)

    _instance = None  # Class attribute to hold the singleton instance

    def __new__(cls):
        """
        Ensure that only one instance exists for HakkaJsonInvalid.
        """
        if cls._instance is None:
            instance = super(HakkaJsonInvalid, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        """
        Initialize the HakkaJsonInvalid object.
        """
        if not hasattr(self, "_initialized"):
            c_hakka_handle = CHakkaHandle()
            result = _create_invalid_func(byref(c_hakka_handle))
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                raise RuntimeError("Failed to create HakkaJsonInvalid.")
            super().__init__(c_hakka_handle)
            self._initialized = True

    def __bool__(self) -> bool:
        """
        Return False for invalid JSON values.
        """
        return False

    def to_python(self):
        """
        Convert the HakkaJsonInvalid to Python's None, as Python has no direct equivalent.
        """
        # Since invalid corresponds to an error state, we return None
        return None

    @staticmethod
    def from_python():
        """
        Return the singleton instance of HakkaJsonInvalid.
        """
        return HakkaJsonInvalid()

    def __eq__(self, other) -> bool:
        """
        Equality comparison for HakkaJsonInvalid.
        """
        # Only equal to another HakkaJsonInvalid instance
        return isinstance(other, HakkaJsonInvalid)

    def __hash__(self) -> int:
        """
        Get the hash of the HakkaJsonInvalid object.
        """
        # Fixed hash for singleton
        return hash("HakkaJsonInvalid")

    def __reduce__(self):
        """
        Support for pickle.
        """
        return (HakkaJsonInvalid.from_python, ())

    def __repr__(self) -> str:
        return "HakkaJsonInvalid"

    def __str__(self) -> str:
        return "invalid"

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
            "__eq__",
            "__hash__",
            "__reduce__",
            "__repr__",
            "__str__",
            "__getnewargs__",
            "__getstate__",
            "__dir__",
        ]
