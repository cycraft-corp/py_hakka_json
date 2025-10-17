#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base class for all HakkaJson classes.
This class is designed to be memory efficient by setting the __slots__ attribute, 
which reduces memory consumption.

Additionally, a hack is used to hide "type" information in the __doc__ string.
The format for the __doc__ string is: "@@type@@, the description of that object".
"""

from ctypes import POINTER, byref, c_uint32, c_ubyte, c_uint64
from typing import Optional

from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum

__all__ = ["HakkaJsonBase", "HakkaJsonIteratorBase"]


_hakka_release = dispatch_table["HakkaRelease"]
_hakka_type = dispatch_table["HakkaType"]
_hakka_dump = dispatch_table["HakkaDump"]
_hakka_dump_size = dispatch_table["HakkaDumpSize"]


class HakkaJsonIteratorBase:
    """
    The base class for all HakkaJson iterators.
    """

    __slots__ = ("_c_iter",)

    def __init__(self, c_json: "HakkaJsonBase"):
        """
        Initialize the iterator with a pointer to a C HakkaJson object.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    def __iter__(self):
        """
        Return the iterator object itself.

        Returns:
            HakkaJsonIteratorBase: The iterator instance.
        """
        return self

    def __next__(self):
        """
        Return the next item from the iterator.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    def __del__(self):
        """ """
        raise NotImplementedError("This method must be implemented by subclasses.")


class HakkaJsonBase:
    """
    The base class for all HakkaJson objects.
    """

    __slots__ = ("_c_hakka_handle",)

    def __init__(self, c_hakka_handle: Optional[POINTER(CHakkaHandle)] = None):
        self._c_hakka_handle = (
            c_hakka_handle if c_hakka_handle is not None else CHakkaHandle()
        )

    def __del__(self) -> None:
        """
        Destructor to free the underlying C HakkaJson object.
        """
        if hasattr(self, "_c_hakka_handle") and self._c_hakka_handle:
            _hakka_release(byref(self._c_hakka_handle))
            self._c_hakka_handle = None

    def get_type(self) -> HakkaJsonTypeEnum:
        """
        Get the type of the HakkaJson object.

        Returns:
            HakkaJsonTypeEnum: The type of the JSON object.
        """
        type_id = c_uint32(-1)
        result = _hakka_type(self._c_hakka_handle, byref(type_id))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get type of HakkaJson object {result.name}.")
        return HakkaJsonTypeEnum(type_id.value)

    def dumps(self, max_depth: int = 512) -> str:
        """
        Dump the JSON object to a string.

        Args:
            max_depth (int): The maximum depth to dump.

        Returns:
            str: The JSON string.
        """
        # extern_c HakkaJsonResultEnum HakkaDump(HakkaHandle handle, uint32_t max_depth, uint8_t *buffer, uint32_t *buffer_size);
        # Get the capacity what we need to allocate.
        buffer_size = c_uint64()
        result = _hakka_dump_size(self._c_hakka_handle, byref(buffer_size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to get the size of the buffer.")

        # Allocate the buffer.
        buffer = (c_ubyte * buffer_size.value)()
        result = _hakka_dump(
            self._c_hakka_handle, max_depth, buffer, byref(buffer_size)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to dump HakkaJson object.")
        return bytes(buffer[: buffer_size.value]).decode("utf-8")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.dumps()

    def __dir__(self):
        return [
            "__init__",
            "__del__",
            "get_type",
            "dumps",
            "__repr__",
            "__str__",
            "__dir__",
        ]
