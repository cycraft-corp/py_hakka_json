#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HakkaJsonString class definition.
Represents a JSON string value in HakkaJson.
"""

from ctypes import byref, c_uint32, c_uint8, c_int64, c_ubyte, c_uint64, c_int32
from typing import Union
import re

from ._hakka_json_base import HakkaJsonBase, HakkaJsonIteratorBase
from ._hakka_json_loader import CHakkaHandle, CHakkaStringIter, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum
from ._hakka_json_type_dispatcher import handle_to_object

__all__ = ["HakkaJsonString"]

# Dispatch functions for string manipulation
_create_string_func = dispatch_table["CreateHakkaString"]
_get_string_func = dispatch_table["GetHakkaString"]
_get_string_length_func = dispatch_table["GetHakkaStringLength"]
_get_string_slice_func = dispatch_table["GetHakkaStringSlice"]
_get_string_concatenate_func = dispatch_table["GetHakkaStringConcatenate"]
_get_string_multiply_func = dispatch_table["GetHakkaStringMultiply"]

_get_string_count_func = dispatch_table["GetHakkaStringCount"]
_get_string_find_func = dispatch_table["GetHakkaStringFind"]
_get_string_rfind_func = dispatch_table["GetHakkaStringRfind"]
_get_string_rspilt_func = dispatch_table["GetHakkaStringRsplit"]
_get_string_split_func = dispatch_table["GetHakkaStringSplit"]
_get_string_splitlines_func = dispatch_table["GetHakkaStringSplitlines"]
_get_string_startswith_func = dispatch_table["GetHakkaStringStartswith"]
_get_string_endswith_func = dispatch_table["GetHakkaStringEndswith"]
_get_string_utf8_length_func = dispatch_table["GetHakkaStringUTF8Length"]

# String methods
_string_methods = {
    "capitalize": dispatch_table["GetHakkaStringCapitalize"],
    "casefold": dispatch_table["GetHakkaStringCasefold"],
    "lower": dispatch_table["GetHakkaStringLower"],
    "upper": dispatch_table["GetHakkaStringUpper"],
    "swapcase": dispatch_table["GetHakkaStringSwapcase"],
    "title": dispatch_table["GetHakkaStringTitle"],
    "zfill": dispatch_table["GetHakkaStringZfill"],
    "replace": dispatch_table["GetHakkaStringReplace"],
    "removeprefix": dispatch_table["GetHakkaStringRemoveprefix"],
    "removesuffix": dispatch_table["GetHakkaStringRemovesuffix"],
}

# String testing methods
_string_tests = {
    "isalnum": dispatch_table["GetHakkaStringIsalnum"],
    "isalpha": dispatch_table["GetHakkaStringIsalpha"],
    "isascii": dispatch_table["GetHakkaStringIsascii"],
    "isdecimal": dispatch_table["GetHakkaStringIsdecimal"],
    "isdigit": dispatch_table["GetHakkaStringIsdigit"],
    "isidentifier": dispatch_table["GetHakkaStringIsidentifier"],
    "islower": dispatch_table["GetHakkaStringIslower"],
    "isnumeric": dispatch_table["GetHakkaStringIsnumeric"],
    "isprintable": dispatch_table["GetHakkaStringIsprintable"],
    "isspace": dispatch_table["GetHakkaStringIsspace"],
    "istitle": dispatch_table["GetHakkaStringIstitle"],
    "isupper": dispatch_table["GetHakkaStringIsupper"],
}

# String iterator functions
_create_string_begin_func = dispatch_table["CreateHakkaStringBegin"]
_move_string_next_func = dispatch_table["MoveHakkaStringNext"]
_get_string_deref_func = dispatch_table["GetHakkaStringDeref"]
_string_iter_release_func = dispatch_table["HakkaStringIterRelease"]

_compare_func = dispatch_table["HakkaCompare"]
_hash_func = dispatch_table["HakkaHash"]


class HakkaJsonString(HakkaJsonBase):
    """
    Represents a JSON string value in HakkaJson.
    """

    __slots__ = ()

    @staticmethod
    def _construct(value: str) -> CHakkaHandle:
        """
        Construct a HakkaJsonString object.

        Args:
            value (str): The string value.

        Returns:
            CHakkaHandle: The handle to the string object.

        Raises:
            RuntimeError: If the C API call fails.
        """
        utf8_bytes = value.encode("utf-8")
        length = c_uint32(len(utf8_bytes))
        c_hakka_handle = CHakkaHandle()
        # Create a ctypes array from utf8_bytes
        byte_array = (c_uint8 * len(utf8_bytes)).from_buffer_copy(utf8_bytes)
        result = _create_string_func(byref(c_hakka_handle), byte_array, length)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to create HakkaJsonString {result.name}.")
        return c_hakka_handle

    def __init__(self, value: str):
        """
        Initialize a HakkaJsonString object.

        Args:
            value (str or HakkaJsonBase or HakkaJsonString): The value to initialize.

        Raises:
            TypeError: If the value is not a string.
        """
        if isinstance(value, HakkaJsonString):
            self._c_hakka_handle = HakkaJsonString._construct(value.to_python())
        elif isinstance(value, str):
            self._c_hakka_handle = HakkaJsonString._construct(value)
        elif isinstance(value, HakkaJsonBase):
            if value.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_STRING:
                raise TypeError(
                    f"Invalid HakkaJsonBase type for HakkaJsonString {value.name}."
                )
            self._c_hakka_handle = value._c_hakka_handle
            value._c_hakka_handle = None  # move from Base to Object
        else:
            raise TypeError("Invalid type for HakkaJsonString.")
        super().__init__(self._c_hakka_handle)

    def _utf8_length(self) -> int:
        """
        Get the length of the string in UTF-8 bytes.

        Returns:
            int: The length of the string in bytes.

        Raises:
            RuntimeError: If the C API call fails.
        """
        length = c_uint64()
        result = _get_string_utf8_length_func(self._c_hakka_handle, byref(length))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to get UTF-8 length of HakkaJsonString {result.name}."
            )
        return length.value

    def to_python(self) -> str:
        """
        Convert the HakkaJsonString to a Python string.

        Returns:
            str: The Python string representation.

        Raises:
            RuntimeError: If the C API call fails.
        """
        buffer_size = c_uint32(self._utf8_length() + 1)
        # Allocate buffer
        buffer = (c_uint8 * buffer_size.value)()
        result = _get_string_func(self._c_hakka_handle, buffer, byref(buffer_size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to get string from HakkaJsonString.")
        utf8_bytes = bytes(buffer[: buffer_size.value])
        return utf8_bytes.decode("utf-8")

    def __str__(self) -> str:
        """
        Get the python string representation of the HakkaJsonString.
        """
        return self.to_python()

    def __repr__(self) -> str:
        """
        Get the representation of the HakkaJsonString.
        """
        return f'HakkaJsonString("{self.to_python()}")'

    def __len__(self) -> int:
        """
        Get the length of the string.

        Returns:
            int: The length of the string.

        Raises:
            RuntimeError: If the C API call fails.
        """
        length = c_uint32()
        result = _get_string_length_func(self._c_hakka_handle, byref(length))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to get length of HakkaJsonString.")
        return length.value

    def __getitem__(self, key):
        """
        Get a character or substring from the string.

        Args:
            key (int or slice): The index or slice.

        Returns:
            HakkaJsonString: The resulting substring or character.

        Raises:
            TypeError: If the key is not an int or slice.
            IndexError: If the index is out of range.
        """
        if isinstance(key, int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("string index out of range")
            return self._slice(key, key + 1, 1)
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return self._slice(start, stop, step)
        else:
            raise TypeError("string indices must be integers or slices")

    def _slice(self, start: int, stop: int, step: int):
        """
        Helper method to perform slicing.

        Args:
            start (int): Start index.
            stop (int): Stop index.
            step (int): Step size.

        Returns:
            HakkaJsonString: The sliced string.

        Raises:
            RuntimeError: If the C API call fails.
        """
        c_start = c_int64(start)
        c_stop = c_int64(stop)
        c_step = c_int64(step)
        result_handle = CHakkaHandle()
        result = _get_string_slice_func(
            self._c_hakka_handle,
            c_start,
            c_stop,
            c_step,
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to slice HakkaJsonString.")
        return HakkaJsonString.from_handle(result_handle)

    @classmethod
    def from_handle(cls, handle: CHakkaHandle) -> "HakkaJsonString":
        """
        Create a HakkaJsonString from an existing handle.
        Performs move-semantics.

        Args:
            handle (CHakkaHandle): The handle to the string.

        Returns:
            HakkaJsonString: The created string object.
        """
        obj = cls.__new__(cls)
        obj._c_hakka_handle = handle
        return obj

    def __add__(self, other) -> "HakkaJsonString":
        """
        Concatenate strings.

        Args:
            other (HakkaJsonString or str): The string to concatenate.

        Returns:
            HakkaJsonString: The concatenated string.

        Raises:
            RuntimeError: If the C API call fails.
        """
        if not isinstance(other, (HakkaJsonString, str)):
            return NotImplemented

        other_str = other.to_python() if isinstance(other, HakkaJsonString) else other
        other_bytes = other_str.encode("utf-8")
        other_length = c_uint32(len(other_bytes))
        byte_array = (c_uint8 * len(other_bytes)).from_buffer_copy(other_bytes)
        result_handle = CHakkaHandle()
        result = _get_string_concatenate_func(
            self._c_hakka_handle,
            byte_array,
            other_length,
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to concatenate strings.")
        return HakkaJsonString.from_handle(result_handle)

    def __radd__(self, other) -> "HakkaJsonString":
        """
        Right-hand string concatenation.

        Args:
            other (str): The string to concatenate.

        Returns:
            HakkaJsonString: The concatenated string.
        """
        return HakkaJsonString(other) + self

    def __mul__(self, n) -> "HakkaJsonString":
        """
        Repeat the string n times.

        Args:
            n (int): The number of times to repeat.

        Returns:
            HakkaJsonString: The repeated string.

        Raises:
            TypeError: If n is not an integer.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(n, int):
            raise TypeError(
                "can't multiply sequence by non-int of type 'HakkaJsonString'"
            )

        result_handle = CHakkaHandle()
        result = _get_string_multiply_func(
            self._c_hakka_handle, c_int64(n), byref(result_handle)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to multiply string.")
        return HakkaJsonString.from_handle(result_handle)

    def __rmul__(self, n) -> "HakkaJsonString":
        return self.__mul__(n)

    def __contains__(self, item) -> bool:
        """
        Check if item is in the string.

        Args:
            item (str): The substring to check.

        Returns:
            bool: True if item is in the string, False otherwise.

        Raises:
            TypeError: If item is not a string.
        """
        if not isinstance(item, (HakkaJsonString, str)):
            raise TypeError("string expected")
        item_str = item.to_python() if isinstance(item, HakkaJsonString) else item
        return self.find(item_str) != -1

    def __iter__(self):
        """
        Return an iterator over the string.

        Returns:
            HakkaJsonStringIterator: The iterator object.
        """
        return HakkaJsonStringIterator(self)

    def __hash__(self) -> int:
        """
        Return the hash of the string.

        Returns:
            int: The hash value.

        Raises:
            RuntimeError: If the C API call fails.
        """
        hash_value = c_uint64()
        result = _hash_func(self._c_hakka_handle, byref(hash_value))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to compute hash for HakkaJsonString.")
        return hash_value.value

    def __eq__(self, other) -> bool:
        return self._compare(other, lambda x, y: x == y)

    def __ne__(self, other) -> bool:
        return self._compare(other, lambda x, y: x != y)

    def __lt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x < y)

    def __le__(self, other) -> bool:
        return self._compare(other, lambda x, y: x <= y)

    def __gt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x > y)

    def __ge__(self, other) -> bool:
        return self._compare(other, lambda x, y: x >= y)

    def _compare(self, other, op):
        """
        Helper method for comparisons.

        Args:
            other (HakkaJsonString or str): The other string.
            op (callable): The comparison operation.

        Returns:
            bool: The result of the comparison.

        Raises:
            TypeError: If other is not a string.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(other, (HakkaJsonString, str)):
            raise TypeError("Comparison with non-string type.")

        other_str = other.to_python() if isinstance(other, HakkaJsonString) else other
        other_hakka = HakkaJsonString(other_str)
        other_handle = other_hakka._c_hakka_handle  # pylint: disable=protected-access

        comparison_result = c_int32()
        result = _compare_func(
            self._c_hakka_handle, other_handle, byref(comparison_result)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Comparison failed.")
        return op(comparison_result.value, 0)

    def __mod__(self, values):
        """
        String formatting using % operator.

        Args:
            values: The values to format.

        Returns:
            str: The formatted string.

        Raises:
            TypeError: If values are not suitable for formatting.
            RuntimeError: If the C API call fails.
        """
        formatted_str = self.to_python() % values
        return formatted_str

    def __rmod__(self, template):
        """
        Reverse string formatting.

        Args:
            template (str): The format template.

        Returns:
            str: The formatted string.

        Raises:
            TypeError: If template is not a string or unsuitable for formatting.
        """
        formatted_str = template % self.to_python()
        return formatted_str

    def __getnewargs__(self):
        """
        Support for pickling.

        Returns:
            tuple: Arguments for object creation.
        """
        return (self.to_python(),)

    def __getstate__(self):
        """
        Get the state for pickling.

        Returns:
            str: The string value.
        """
        return self.to_python()

    def __setstate__(self, state):
        """
        Set the state from unpickling.

        Args:
            state (str): The string value.
        """
        self.__init__(state)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    # String Methods

    def capitalize(self) -> "HakkaJsonString":
        """
        Return a capitalized version of the string.
        """
        return self._string_method("capitalize")

    def casefold(self) -> "HakkaJsonString":
        """
        Return a casefolded version of the string.
        """
        return self._string_method("casefold")

    def lower(self) -> "HakkaJsonString":
        """
        Return a lowercased version of the string.
        """
        return self._string_method("lower")

    def upper(self) -> "HakkaJsonString":
        """
        Return an uppercased version of the string.
        """
        return self._string_method("upper")

    def swapcase(self) -> "HakkaJsonString":
        """
        Return a swapped case version of the string.
        """
        return self._string_method("swapcase")

    def title(self) -> "HakkaJsonString":
        """
        Return a titlecased version of the string.
        """
        return self._string_method("title")

    def zfill(self, width: int) -> "HakkaJsonString":
        """
        Pad the string with zeros to the specified width.

        Args:
            width (int): The width of the padded string.

        Returns:
            HakkaJsonString: The zero-padded string.

        Raises:
            TypeError: If width is not an integer.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(width, int):
            raise TypeError("zfill() integer argument required")
        method = _string_methods["zfill"]
        result_handle = CHakkaHandle()
        result = method(self._c_hakka_handle, c_int64(width), byref(result_handle))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to zfill HakkaJsonString.")
        return HakkaJsonString.from_handle(result_handle)

    def replace(
        self,
        old: Union[str, "HakkaJsonString"],
        new: Union[str, "HakkaJsonString"],
        count: int = -1,
    ) -> "HakkaJsonString":
        """
        Replace occurrences of a substring with another substring.

        Args:
            old (str or HakkaJsonString): The substring to replace.
            new (str or HakkaJsonString): The replacement substring.
            count (int): The number of replacements to make.

        Returns:
            HakkaJsonString: The resulting string.

        Raises:
            TypeError: If old or new are not strings, or count is not an integer.
            RuntimeError: If the C API call fails.
        """
        old = old.to_python() if isinstance(old, HakkaJsonString) else old
        new = new.to_python() if isinstance(new, HakkaJsonString) else new
        if not isinstance(old, str) or not isinstance(new, str):
            raise TypeError("replace() arguments must be str")
        if not isinstance(count, int):
            raise TypeError("replace() count must be an integer")
        method = _string_methods["replace"]
        old_bytes = old.encode("utf-8")
        new_bytes = new.encode("utf-8")
        old_length = c_uint32(len(old_bytes))
        new_length = c_uint32(len(new_bytes))
        result_handle = CHakkaHandle()
        result = method(
            self._c_hakka_handle,
            (c_uint8 * len(old_bytes)).from_buffer_copy(old_bytes),
            old_length,
            (c_uint8 * len(new_bytes)).from_buffer_copy(new_bytes),
            new_length,
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to replace in HakkaJsonString.")
        # If 'count' is specified and valid, apply it by repeating the replace operation.
        if count != -1:
            temp_str = HakkaJsonString.from_handle(result_handle)
            for _ in range(count - 1):
                temp_str = temp_str.replace(old, new)
            return temp_str
        return HakkaJsonString.from_handle(result_handle)

    def removeprefix(self, prefix: str) -> "HakkaJsonString":
        """
        Remove a prefix from the string.

        Args:
            prefix (str): The prefix to remove.

        Returns:
            HakkaJsonString: The resulting string.

        Raises:
            TypeError: If prefix is not a string.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(prefix, str):
            raise TypeError("removeprefix() argument must be str")
        method = _string_methods["removeprefix"]
        prefix_bytes = prefix.encode("utf-8")
        prefix_length = c_uint32(len(prefix_bytes))
        result_handle = CHakkaHandle()
        result = method(
            self._c_hakka_handle,
            (c_uint8 * len(prefix_bytes)).from_buffer_copy(prefix_bytes),
            prefix_length,
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to remove prefix.")
        return HakkaJsonString.from_handle(result_handle)

    def removesuffix(self, suffix: str) -> "HakkaJsonString":
        """
        Remove a suffix from the string.

        Args:
            suffix (str): The suffix to remove.

        Returns:
            HakkaJsonString: The resulting string.

        Raises:
            TypeError: If suffix is not a string.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(suffix, str):
            raise TypeError("removesuffix() argument must be str")
        method = _string_methods["removesuffix"]
        suffix_bytes = suffix.encode("utf-8")
        suffix_length = c_uint32(len(suffix_bytes))
        result_handle = CHakkaHandle()
        result = method(
            self._c_hakka_handle,
            (c_uint8 * len(suffix_bytes)).from_buffer_copy(suffix_bytes),
            suffix_length,
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to remove suffix.")
        return HakkaJsonString.from_handle(result_handle)

    def _string_method(self, method_name: str) -> "HakkaJsonString":
        """
        Helper method to call string methods.

        Args:
            method_name (str): The name of the method.

        Returns:
            HakkaJsonString: The resulting string.

        Raises:
            RuntimeError: If the C API call fails.
        """
        method = _string_methods[method_name]
        result_handle = CHakkaHandle()
        result = method(self._c_hakka_handle, byref(result_handle))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to {method_name} HakkaJsonString {result.name}."
            )
        return HakkaJsonString.from_handle(result_handle)

    # String Testing Methods

    def isalnum(self) -> bool:
        return self._string_test("isalnum")

    def isalpha(self) -> bool:
        return self._string_test("isalpha")

    def isascii(self) -> bool:
        return self._string_test("isascii")

    def isdecimal(self) -> bool:
        return self._string_test("isdecimal")

    def isdigit(self) -> bool:
        return self._string_test("isdigit")

    def isidentifier(self) -> bool:
        return self._string_test("isidentifier")

    def islower(self) -> bool:
        return self._string_test("islower")

    def isnumeric(self) -> bool:
        return self._string_test("isnumeric")

    def isprintable(self) -> bool:
        return self._string_test("isprintable")

    def isspace(self) -> bool:
        return self._string_test("isspace")

    def istitle(self) -> bool:
        return self._string_test("istitle")

    def isupper(self) -> bool:
        return self._string_test("isupper")

    def _string_test(self, test_name: str) -> bool:
        """
        Helper method to call string testing methods.

        Args:
            test_name (str): The name of the test.

        Returns:
            bool: The result of the test.

        Raises:
            RuntimeError: If the C API call fails.
        """
        method = _string_tests[test_name]
        result_bool = c_ubyte()
        result = method(self._c_hakka_handle, byref(result_bool))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to {test_name} HakkaJsonString {result.name}.")
        return result_bool.value

    # Additional String Methods

    def center(self, width: int, fillchar: str = " ") -> "HakkaJsonString":
        """
        Center the string within a given width.

        Args:
            width (int): The width of the centered string.
            fillchar (str): The character to pad with.

        Returns:
            HakkaJsonString: The centered string.
        """
        my_str = self.to_python()
        return HakkaJsonString(my_str.center(width, fillchar))

    def count(self, sub: str, start: int = 0, end: int = -1) -> int:
        """
        Count occurrences of a substring in the string.

        Args:
            sub (str): The substring to count.
            start (int): The start index.
            end (int): The end index.

        Returns:
            int: The number of occurrences.

        Raises:
            TypeError: If sub is not a string.
            RuntimeError: If the C API call fails.
        """
        if start != 0 or end != -1:
            sliced = self._slice(start, end if end != -1 else len(self), 1)
        else:
            sliced = self

        if not isinstance(sub, (HakkaJsonString, str)):
            raise TypeError("substring must be str")

        sub_str = sub.to_python() if isinstance(sub, HakkaJsonString) else sub
        sub_bytes = sub_str.encode("utf-8")
        sub_length = c_uint32(len(sub_bytes))
        byte_array = (c_uint8 * len(sub_bytes)).from_buffer_copy(sub_bytes)
        count = c_int64()
        result = _get_string_count_func(
            sliced._c_hakka_handle,  # pylint: disable=protected-access
            byte_array,
            sub_length,
            byref(count),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to count occurrences in HakkaJsonString {result.name}."
            )
        return count.value

    def find(self, sub: str, start: int = 0, end: int = -1) -> int:
        """
        Find the index of the first occurrence of a substring.

        Args:
            sub (str): The substring to find.
            start (int): The start index.
            end (int): The end index.

        Returns:
            int: The index of the first occurrence, or -1 if not found.

        Raises:
        """
        if start != 0 or end != -1:
            sliced = self._slice(start, end if end != -1 else len(self), 1)
        else:
            sliced = self

        if not isinstance(sub, (HakkaJsonString, str)):
            raise TypeError("substring must be str")

        sub_str = sub.to_python() if isinstance(sub, HakkaJsonString) else sub
        sub_bytes = sub_str.encode("utf-8")
        sub_length = c_uint32(len(sub_bytes))
        byte_array = (c_uint8 * len(sub_bytes)).from_buffer_copy(sub_bytes)
        position = c_int64()
        result = _get_string_find_func(
            sliced._c_hakka_handle,  # pylint: disable=protected-access
            byte_array,
            sub_length,
            byref(position),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to find substring: {result.name}.")
        return position.value

    def rfind(self, sub: str, start: int = 0, end: int = -1) -> int:
        """
        Find the index of the last occurrence of a substring.

        Args:
            sub (str): The substring to find.
            start (int): The start index.
            end (int): The end index.

        Returns:
            int: The index of the last occurrence, or -1 if not found.

        Raises:
            TypeError: If sub is not a string.
            RuntimeError: If the C API call fails.
        """
        start = 0 if (start is None) else start
        end = -1 if (end is None) else end
        if start != 0 or end != -1:
            sliced = self._slice(start, end if end != -1 else len(self), 1)
        else:
            sliced = self

        if not isinstance(sub, (HakkaJsonString, str)):
            raise TypeError("substring must be str")

        sub_str = sub.to_python() if isinstance(sub, HakkaJsonString) else sub
        sub_bytes = sub_str.encode("utf-8")
        sub_length = c_uint32(len(sub_bytes))
        byte_array = (c_uint8 * len(sub_bytes)).from_buffer_copy(sub_bytes)
        position = c_int64()
        result = _get_string_rfind_func(
            sliced._c_hakka_handle,  # pylint: disable=protected-access
            byte_array,
            sub_length,
            byref(position),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to rfind substring: {result.name}.")
        return position.value

    def finditer(self, sub: str, start: int = 0, end: int = -1):
        """
        Return an iterator yielding match objects over non-overlapping matches for the substring.

        Args:
            sub (str): The substring to find.
            start (int): The start index.
            end (int): The end index.

        Returns:
            Iterator: The iterator over match objects.
        """
        pattern = re.escape(sub)
        return re.finditer(pattern, self.to_python()[start:end])

    def format(self, *args, **kwargs) -> str:
        """
        Perform string formatting.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            str: The formatted string.

        Raises:
            ValueError: If formatting fails.
        """
        try:
            formatted_str = self.to_python().format(*args, **kwargs)
            return formatted_str
        except Exception as e:
            raise ValueError(f"String formatting failed: {e}") from e

    def format_map(self, mapping) -> str:
        """
        Perform string formatting using a mapping.

        Args:
            mapping (dict): The mapping for formatting.

        Returns:
            str: The formatted string.

        Raises:
            ValueError: If formatting fails.
        """
        try:
            formatted_str = self.to_python().format_map(mapping)
            return formatted_str
        except Exception as e:
            raise ValueError(f"String formatting failed: {e}") from e

    def encode(self, encoding="utf-8", errors="strict") -> bytes:
        """
        Encode the string using the specified encoding.

        Args:
            encoding (str): The encoding to use.
            errors (str): The error handling scheme.

        Returns:
            bytes: The encoded bytes.

        Raises:
            LookupError: If the encoding is unknown.
            UnicodeEncodeError: If encoding fails.
        """
        return self.to_python().encode(encoding, errors)

    def expandtabs(self, tabsize=8) -> "HakkaJsonString":
        """
        Expand tabs in the string.

        Args:
            tabsize (int): The tab size.

        Returns:
            HakkaJsonString: The expanded string.
        """
        return HakkaJsonString(self.to_python().expandtabs(tabsize))

    def join(self, iterable) -> "HakkaJsonString":
        """
        Join the elements of an iterable.
        """
        if isinstance(iterable, HakkaJsonString):
            iterable = iterable.to_python()
        else:
            iterable = [
                item.to_python() if isinstance(item, HakkaJsonString) else item
                for item in iterable
            ]
        return HakkaJsonString(self.to_python().join(iterable))

    def split(self, sep=None, maxsplit=-1) -> "HakkaJsonArray":
        """
        Split the string by the specified separator.

        Args:
            sep (str): The separator.
            maxsplit (int): The maximum number of splits.

        Returns:
            HakkaJsonArray: The array of substrings.

        Raises:
            TypeError: If the arguments are invalid.
            RuntimeError: If the C API call fails.
        """

        if not isinstance(maxsplit, int):
            raise TypeError("maxsplit must be an integer")
        if not isinstance(sep, (HakkaJsonString, str, type(None))):
            raise TypeError("split() argument must be str")
        if isinstance(sep, HakkaJsonString):
            sep = sep.to_python()

        sep_bytes = sep.encode("utf-8") if sep is not None else b""
        sep_length = c_uint32(len(sep_bytes))
        array_handle = CHakkaHandle()
        result = _get_string_split_func(
            self._c_hakka_handle,
            (c_uint8 * len(sep_bytes)).from_buffer_copy(sep_bytes),
            sep_length,
            c_int64(maxsplit),
            byref(array_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to split HakkaJsonString {result.name}.")
        return handle_to_object(array_handle)

    def rsplit(self, sep=None, maxsplit=-1) -> "HakkaJsonArray":
        """
        Split the string by the specified separator from the right

        Args:
            sep (str): The separator.
            maxsplit (int): The maximum number of splits.

        Returns:
            HakkaJsonArray: The array of substrings.

        Raises:
            TypeError: If the arguments are invalid.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(maxsplit, int):
            raise TypeError("maxsplit must be an integer")
        if not isinstance(sep, (HakkaJsonString, str, type(None))):
            raise TypeError("rsplit() argument must be str")
        if isinstance(sep, HakkaJsonString):
            sep = sep.to_python()

        sep_bytes = sep.encode("utf-8") if sep is not None else b""
        sep_length = c_uint32(len(sep_bytes))
        array_handle = CHakkaHandle()
        result = _get_string_rspilt_func(
            self._c_hakka_handle,
            (c_uint8 * len(sep_bytes)).from_buffer_copy(sep_bytes),
            sep_length,
            c_int64(maxsplit),
            byref(array_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to rsplit HakkaJsonString {result.name}.")
        return handle_to_object(array_handle)

    def splitlines(self, keepends: bool = False) -> "HakkaJsonArray":
        """
        Split the string into lines.

        Args:
            keepends (bool): Whether to keep line endings.

        Returns:
            HakkaJsonArray: The array of lines.

        Raises:
            TypeError: If keepends is not a boolean.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(keepends, bool):
            raise TypeError("keepends must be a boolean")

        array_handle = CHakkaHandle()
        result = _get_string_splitlines_func(
            self._c_hakka_handle, c_uint8(keepends), byref(array_handle)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to splitlines HakkaJsonString {result.name}.")
        return handle_to_object(array_handle)

    def startswith(self, prefix: str, start: int = 0, end: int = None) -> bool:
        """
        Check if the string starts with a prefix.

        Args:
            prefix (str): The prefix to check.
            start (int): The starting position.
            end (int): The ending position.

        Returns:
            bool: True if the string starts with the prefix, False otherwise.

        Raises:
            TypeError: If prefix is not a string.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(prefix, (str, HakkaJsonString)):
            raise TypeError("startswith() argument must be str")
        if isinstance(prefix, HakkaJsonString):
            prefix = prefix.to_python()

        if start != 0 or end is not None:
            sliced = self._slice(start, end if end is not None else len(self), 1)
        else:
            sliced = self

        prefix_bytes = prefix.encode("utf-8")
        prefix_length = c_uint32(len(prefix_bytes))
        result_bool = c_ubyte()

        result = _get_string_startswith_func(
            sliced._c_hakka_handle,  # pylint: disable=protected-access
            (c_uint8 * len(prefix_bytes)).from_buffer_copy(prefix_bytes),
            prefix_length,
            byref(result_bool),
        )

        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to execute startswith {result.name}.")

        return result_bool.value

    def endswith(self, suffix: str, start: int = 0, end: int = None) -> bool:
        """
        Check if the string ends with a suffix.

        Args:
            suffix (str): The suffix to check.
            start (int): The starting position.
            end (int): The ending position.

        Returns:
            bool: True if the string ends with the suffix, False otherwise.

        Raises:
            TypeError: If suffix is not a string.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(suffix, (str, HakkaJsonString)):
            raise TypeError("endswith() argument must be str")
        if isinstance(suffix, HakkaJsonString):
            suffix = suffix.to_python()

        if start != 0 or end is not None:
            sliced = self._slice(start, end if end is not None else len(self), 1)
        else:
            sliced = self

        suffix_bytes = suffix.encode("utf-8")
        suffix_length = c_uint32(len(suffix_bytes))
        result_bool = c_ubyte()

        result = _get_string_endswith_func(
            sliced._c_hakka_handle,  # pylint: disable=protected-access
            (c_uint8 * len(suffix_bytes)).from_buffer_copy(suffix_bytes),
            suffix_length,
            byref(result_bool),
        )

        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to execute endswith {result.name}.")

        return result_bool.value

    def partition(self, sep: str) -> tuple:
        return self.to_python().partition(sep)

    def rpartition(self, sep: str) -> tuple:
        return self.to_python().rpartition(sep)

    def ljust(self, width: int, fillchar: str = " ") -> "HakkaJsonString":
        return HakkaJsonString(self.to_python().ljust(width, fillchar))

    def rindex(self, sub: str, start: int = 0, end: int = None) -> int:
        """
        Like find(), but raises ValueError when the substring is not found.

        Args:
            sub (str): The substring to find.
            start (int): The starting position.
            end (int): The ending position.

        Returns:
            int: The highest index where the substring is found.

        Raises:
            ValueError: If the substring is not found.
            TypeError: If sub is not a string.
            RuntimeError: If the C API call fails.
        """
        pos = self.rfind(sub, start, end)
        if pos == -1:
            raise ValueError(f"substring not found: {sub}")
        return pos

    def rindexiter(self, sub: str, start: int = 0, end: int = None):
        """
        Return an iterator yielding match objects over non-overlapping matches for the substring,
        starting from the right.

        Args:
            sub (str): The substring to find.
            start (int): The starting position.
            end (int): The ending position.

        Returns:
            iterator: An iterator over match objects.

        Raises:
            TypeError: If sub is not a string.
        """
        pattern = re.escape(sub)
        return re.finditer(pattern, self.to_python()[start:end])

    def maketrans(self, x, y=None, z=None):
        """
        Return a translation table usable for str.translate().

        Args:
            x (dict or str): The first argument.
            y (str, optional): The second argument.
            z (str, optional): The third argument.

        Returns:
            dict: A translation table.

        Raises:
            TypeError: If arguments are of incorrect types.
        """
        if y is None and z is None:
            return self.to_python().maketrans(x)
        if y is not None and z is None:
            return self.to_python().maketrans(x, y)
        return self.to_python().maketrans(x, y, z)

    def translate(self, table):
        """
        Return a copy of the string in which each character has been mapped through the given translation table.
        """
        return HakkaJsonString(self.to_python().translate(table))

    def __dir__(self):
        return super().__dir__() + [
            "_construct",
            "__init__",
            "_utf8_length",
            "to_python",
            "__str__",
            "__repr__",
            "__len__",
            "__getitem__",
            "_slice",
            "from_handle",
            "__add__",
            "__radd__",
            "__mul__",
            "__rmul__",
            "__contains__",
            "__iter__",
            "__hash__",
            "__eq__",
            "__ne__",
            "__lt__",
            "__le__",
            "__gt__",
            "__ge__",
            "_compare",
            "__mod__",
            "__rmod__",
            "__getnewargs__",
            "__getstate__",
            "__setstate__",
            "__copy__",
            "__deepcopy__",
            "capitalize",
            "casefold",
            "lower",
            "upper",
            "swapcase",
            "title",
            "zfill",
            "replace",
            "removeprefix",
            "removesuffix",
            "_string_method",
            "isalnum",
            "isalpha",
            "isascii",
            "isdecimal",
            "isdigit",
            "isidentifier",
            "islower",
            "isnumeric",
            "isprintable",
            "isspace",
            "istitle",
            "isupper",
            "_string_test",
            "center",
            "count",
            "find",
            "rfind",
            "finditer",
            "format",
            "format_map",
            "encode",
            "expandtabs",
            "join",
            "split",
            "rsplit",
            "splitlines",
            "startswith",
            "endswith",
            "partition",
            "rpartition",
            "ljust",
            "rindex",
            "rindexiter",
            "maketrans",
            "translate",
            "__dir__",
        ]


class HakkaJsonStringIterator(HakkaJsonIteratorBase):
    """
    Iterator over HakkaJsonString characters.
    Inherits from HakkaJsonIteratorBase.
    """

    __slots__ = ("_end",)

    def __init__(self, hakka_string: HakkaJsonString):
        """
        Initialize the iterator with a HakkaJsonString object.

        Args:
            hakka_string (HakkaJsonString): The string to iterate over.

        Raises:
            RuntimeError: If the C API call fails.
        """
        self._c_iter = CHakkaStringIter()
        result = _create_string_begin_func(
            hakka_string._c_hakka_handle, byref(self._c_iter)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError("Failed to create string iterator.")
        self._end = False

    def __iter__(self):
        """
        Return the iterator object itself.

        Returns:
            HakkaJsonStringIterator: The iterator instance.
        """
        return self

    def __next__(self):
        """
        Return the next character from the iterator.

        Returns:
            str: The next character in the string.

        Raises:
            StopIteration: If the end of the string is reached.
            RuntimeError: If the C API call fails.
        """
        if self._end:
            self.__del__()
            raise StopIteration
        utf32_char = c_uint32()
        result = _get_string_deref_func(self._c_iter, byref(utf32_char))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            self.__del__()
            raise RuntimeError("Failed to dereference iterator.")
        char = chr(utf32_char.value)
        result = _move_string_next_func(self._c_iter)
        if result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
            self._end = True
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            self.__del__()
            raise RuntimeError("Failed to advance iterator.")
        return char

    def __del__(self):
        """
        Clean up the iterator by releasing resources.
        """
        if hasattr(self, "_c_iter") and self._c_iter:
            _string_iter_release_func(byref(self._c_iter))
            self._c_iter = None

    def __dir__(self):
        return ["__init__", "__iter__", "__next__", "__del__", "__dir__"]
