"""
HakkaJsonArray class definition.
Represents a JSON array value in HakkaJson.
Implements list-like behavior.
"""

from ctypes import byref, c_int32, c_uint32, c_uint8, c_uint64
from typing import Any, Optional, Union

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, CHakkaArrayIter, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum
from ._hakka_json_type_dispatcher import obj_from_python, handle_to_object

__all__ = ["HakkaJsonArray", "HakkaJsonArrayIterator"]

# Dispatch functions for array manipulation
_compare_func = dispatch_table["HakkaCompare"]

_create_array_func = dispatch_table["CreateHakkaArray"]
_loads_array_func = dispatch_table["LoadsHakkaArray"]
_dump_array_func = dispatch_table["DumpHakkaArray"]
_dump_size_array_func = dispatch_table["HakkaDumpSize"]

_get_array_object_func = dispatch_table["GetHakkaArrayObject"]
_set_array_func = dispatch_table["SetHakkaArray"]
_get_array_slice_func = dispatch_table["GetHakkaArraySlice"]
_set_array_slice_func = dispatch_table["SetHakkaArraySlice"]
_remove_array_index_func = dispatch_table["RemoveHakkaArrayIndex"]
_clear_array_func = dispatch_table["ClearHakkaArray"]
_insert_array_func = dispatch_table["InsertHakkaArray"]

_multiply_array_func = dispatch_table["MultiplyHakkaArray"]
_get_array_size_func = dispatch_table["GetHakkaArraySize"]
_count_array_func = dispatch_table["CountHakkaArray"]
_extend_array_func = dispatch_table["ExtendHakkaArrayArray"]
_find_first_array_func = dispatch_table["FindFirstHakkaArray"]
_push_back_array_func = dispatch_table["PushBackHakkaArray"]
_pop_array_func = dispatch_table["PopHakkaArray"]
_remove_value_array_func = dispatch_table["RemoveValueHakkaArray"]
_reverse_array_func = dispatch_table["ReverseHakkaArray"]

# Iterators
_create_array_iter_begin_func = dispatch_table["CreateHakkaArrayIterBegin"]
_create_array_iter_rbegin_func = dispatch_table["CreateHakkaArrayIterRBegin"]
_move_array_iter_next_func = dispatch_table["MoveHakkaArrayIterNext"]
_get_array_iter_deref_func = dispatch_table["GetHakkaArrayIterDeref"]
_release_array_iter_func = dispatch_table["HakkaArrayIterRelease"]


class HakkaJsonArray(HakkaJsonBase):
    """
    Represents a JSON array value in HakkaJson.
    Implements list-like behavior.
    """

    __slots__ = ()

    def __init__(self, initial: Optional[Union["HakkaJsonArray", list, tuple]] = None):
        if isinstance(initial, HakkaJsonArray):
            self._c_hakka_handle = initial._c_hakka_handle
        elif isinstance(initial, HakkaJsonBase):  # Seems to be moved from HakkaJsonBase
            if initial.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_ARRAY:
                raise TypeError("HakkaJsonArray initialization requires an array.")
            self._c_hakka_handle = initial._c_hakka_handle
            initial._c_hakka_handle = None
        elif initial is None:
            self._c_hakka_handle = self._construct()
        elif isinstance(
            initial, (list, tuple)
        ):  # construct from other, so this is a new one
            new_array = HakkaJsonArray()
            for item in initial:
                new_array.append(item)
            self._c_hakka_handle = new_array._c_hakka_handle
            new_array._c_hakka_handle = None
        else:
            raise TypeError("Unsupported type for HakkaJsonArray initialization.")
        super().__init__(self._c_hakka_handle)

    @staticmethod
    def _construct() -> CHakkaHandle:
        c_hakka_handle = CHakkaHandle()
        result = _create_array_func(byref(c_hakka_handle))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to create HakkaJsonArray: {result.name}.")
        return c_hakka_handle

    @staticmethod
    def loads(json_str: str, max_depth: int = 512) -> "HakkaJsonArray":
        """
        Create a HakkaJsonArray object from a JSON string.

        Args:
            json_str (str): The JSON string.

        Returns:
            HakkaJsonArray: The HakkaJsonArray object.
        """
        json_str = json_str.encode("utf-8")
        json_str += b"\x00"
        buffer_size = c_uint32(len(json_str))
        buffer = (c_uint8 * buffer_size.value).from_buffer_copy(json_str)
        c_hakka_handle = CHakkaHandle()
        result = _loads_array_func(
            buffer,
            buffer_size,
            byref(c_hakka_handle),
            c_uint32(max_depth),
        )
        match result:
            case HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                return HakkaJsonArray(HakkaJsonBase(c_hakka_handle))
            case HakkaJsonResultEnum.HAKKA_JSON_RECURSION_DEPTH_EXCEEDED:
                raise RecursionError("Recursion depth exceeded in HakkaJsonArray.")
            case HakkaJsonResultEnum.HAKKA_JSON_PARSE_ERROR:
                raise ValueError("Invalid JSON string for HakkaJsonArray.")
            case _:
                raise RuntimeError(f"Failed to load HakkaJsonArray: {result.name}.")
        return HakkaJsonArray(HakkaJsonBase(c_hakka_handle))

    def to_python(self) -> list:
        """
        Convert the HakkaJsonArray to a Python list.

        Returns:
            list: The list representation.
        """
        import sys
        # Increase recursion limit temporarily for deeply nested structures
        old_limit = sys.getrecursionlimit()
        try:
            # Set a higher limit if needed (but not too high to avoid stack overflow)
            if old_limit < 2000:
                sys.setrecursionlimit(2000)

            result = []
            for item in self:
                # Recursively convert each item to Python
                # Check if it's a Hakka type with to_python method
                if hasattr(item, 'to_python') and callable(getattr(item, 'to_python')):
                    result.append(item.to_python())
                else:
                    # Already a Python primitive
                    result.append(item)
            return result
        finally:
            # Restore original recursion limit
            sys.setrecursionlimit(old_limit)

    @staticmethod
    def from_python(py_list: Union[list, tuple]) -> "HakkaJsonArray":
        """
        Create a HakkaJsonArray from a Python list or tuple.

        Args:
            py_list (list or tuple): The Python list or tuple.

        Returns:
            HakkaJsonArray: The corresponding HakkaJsonArray object.

        Raises:
            TypeError: If py_list is not a list or tuple.
        """
        if not isinstance(py_list, (list, tuple)):
            raise TypeError("from_python expects a list or tuple.")
        return HakkaJsonArray(py_list)

    def dumps(self, max_depth: int = 512) -> str:
        """
        Serialize the HakkaJsonArray to a JSON string.

        Args:
            max_depth (int, optional): Maximum recursion depth.

        Returns:
            str: The JSON string representation.

        Raises:
            RuntimeError: If dumping fails.
        """
        buffer_size = c_uint64()
        # First call to get required buffer size
        result = _dump_size_array_func(self._c_hakka_handle, byref(buffer_size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get size of HakkaJsonArray: {result.name}.")

        # Allocate buffer with the required size
        buffer = (c_uint8 * buffer_size.value)()
        result = _dump_array_func(
            self._c_hakka_handle, c_uint32(max_depth), buffer, byref(buffer_size)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to dump HakkaJsonArray: {result.name}.")
        return bytes(buffer[: buffer_size.value]).decode("utf-8")

    def __bool__(self) -> bool:
        """
        Return True if the array is non-empty, False otherwise.

        Returns:
            bool: The boolean value.
        """
        return self.__len__() != 0

    def __len__(self) -> int:
        """
        Return the number of elements in the array.

        Returns:
            int: The size of the array.

        Raises:
            RuntimeError: If the C API call fails.
        """
        size = c_uint32()
        result = _get_array_size_func(self._c_hakka_handle, byref(size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get size of HakkaJsonArray: {result.name}.")
        return size.value

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, "HakkaJsonArray"]:
        """
        Get the item at the specified index or slice.

        Args:
            index (int or slice): The index or slice.

        Returns:
            Any or HakkaJsonArray: The retrieved item or slice.

        Raises:
            TypeError: If index is not an int or slice.
            IndexError: If index is out of range.
            RuntimeError: If the C API call fails.
        """
        if isinstance(index, slice):
            return self._get_slice(index)
        elif isinstance(index, int):
            return self._get_item(index)
        else:
            raise TypeError("Index must be an integer or slice.")

    def __setitem__(self, index: Union[int, slice], value: Any):
        """
        Set the item at the specified index or slice.

        Args:
            index (int or slice): The index or slice.
            value (Any): The value to set.

        Raises:
            TypeError: If index type is invalid or value type is unsupported.
            IndexError: If index is out of range.
            RuntimeError: If the C API call fails.
        """
        if isinstance(index, slice):
            self._set_slice(index, value)
        elif isinstance(index, int):
            self._set_item(index, value)
        else:
            raise TypeError("Index must be an integer or slice.")

    def _get_item(self, index: int) -> Any:
        size = len(self)
        if index < 0:
            index += size
        if not (0 <= index < size):
            raise IndexError("HakkaJsonArray index out of range.")

        item_handle = CHakkaHandle()
        res = _get_array_object_func(self._c_hakka_handle, index, byref(item_handle))
        if res != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get item at index {index}: {res.name}.")
        return handle_to_object(item_handle)

    def _get_slice(self, index: slice) -> "HakkaJsonArray":
        start, stop, step = index.indices(len(self))
        new_array_handle = CHakkaHandle()
        result = _get_array_slice_func(
            self._c_hakka_handle, start, stop, step, byref(new_array_handle)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to get slice from HakkaJsonArray {result.name}."
            )
        return handle_to_object(new_array_handle)

    def _set_item(self, index: int, value: Any):
        size = len(self)
        if index < 0:
            index += size
        if not (0 <= index < size):
            raise IndexError("HakkaJsonArray assignment index out of range.")

        if not issubclass(type(value), HakkaJsonBase):
            value = obj_from_python(value)
        result = _set_array_func(
            self._c_hakka_handle,
            index,
            value._c_hakka_handle,  # pylint: disable=protected-access
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to set item at index {index}.")

    def _set_slice(self, index: slice, value: Any):
        if not isinstance(value, (HakkaJsonArray, list, tuple)):
            raise TypeError("Can only assign an iterable to a slice.")
        start, stop, step = index.indices(len(self))
        if isinstance(value, (list, tuple)):
            value = HakkaJsonArray(value)
        result = _set_array_slice_func(
            self._c_hakka_handle, start, stop, step, value._c_hakka_handle
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to set slice in HakkaJsonArray {result.value}.")

    def __delitem__(self, index: Union[int, slice]):
        """
        Delete the item at the specified index or slice.

        Args:
            index (int or slice): The index or slice.

        Raises:
            TypeError: If index type is invalid.
            IndexError: If index is out of range.
            RuntimeError: If the C API call fails.
        """
        if isinstance(index, slice):
            self.__setitem__(index, [])
        elif isinstance(index, int):
            self._remove_item(index)
        else:
            raise TypeError("Index must be an integer or slice.")

    def _remove_item(self, index: int):
        size = len(self)
        if index < 0:
            index += size
        if not (0 <= index < size):
            raise IndexError("HakkaJsonArray deletion index out of range.")

        result = _remove_array_index_func(self._c_hakka_handle, index)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to delete item at index {index}: {result.name}."
            )

    def __contains__(self, item: Any) -> bool:
        """
        Check if the array contains the specified item.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if the item is in the array, False otherwise.
        """
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def append(self, value: Any):
        """
        Append an item to the end of the array.

        Args:
            value (Any): The item to append.

        Raises:
            RuntimeError: If the C API call fails.
        """
        value_obj = (
            obj_from_python(value) if not isinstance(value, HakkaJsonBase) else value
        )
        result = _push_back_array_func(self._c_hakka_handle, value_obj._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to append to HakkaJsonArray: {result.name}.")

    def extend(self, iterable: Union["HakkaJsonArray", list, tuple]):
        """
        Extend the array by appending elements from the iterable.

        Args:
            iterable (HakkaJsonArray, list, or tuple): The iterable to extend from.

        Raises:
            TypeError: If iterable type is unsupported.
            RuntimeError: If the C API call fails.
        """
        if isinstance(iterable, (list, tuple)):
            iterable = HakkaJsonArray(iterable)
        elif not isinstance(iterable, HakkaJsonArray):
            raise TypeError(
                "extend expects a HakkaJsonArray or iterable of HakkaJsonBase."
            )
        result = _extend_array_func(self._c_hakka_handle, iterable._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to extend HakkaJsonArray: {result.name}.")

    def insert(self, index: int, value: Any):
        """
        Insert an item at a given position.

        Args:
            index (int): The position to insert at.
            value (Any): The item to insert.

        Raises:
            TypeError: If value type is unsupported.
            IndexError: If index is out of bounds.
            RuntimeError: If the C API call fails.
        """
        value_obj = (
            obj_from_python(value) if not isinstance(value, HakkaJsonBase) else value
        )
        result = _insert_array_func(
            self._c_hakka_handle, index, value_obj._c_hakka_handle
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_INDEX_OUT_OF_BOUNDS:
            raise IndexError("Index out of bounds for HakkaJsonArray.")
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to insert at index {index}: {result.name}.")

    def remove(self, value: Any):
        """
        Remove the first occurrence of a value.

        Args:
            value (Any): The value to remove.

        Raises:
            ValueError: If the value is not found.
            TypeError: If value type is unsupported.
            RuntimeError: If the C API call fails.
        """
        value_obj = (
            obj_from_python(value) if not isinstance(value, HakkaJsonBase) else value
        )
        result = _remove_value_array_func(
            self._c_hakka_handle, value_obj._c_hakka_handle
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            raise ValueError("Value not found in HakkaJsonArray.")
        elif result == HakkaJsonResultEnum.HAKKA_JSON_TYPE_ERROR:
            raise TypeError(f"Type error in HakkaJsonArray: {value}.")
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to remove value from HakkaJsonArray: {result.name}."
            )

    def pop(self, index: int = -1) -> Any:
        """
        Remove and return item at index (default last).

        Args:
            index (int, optional): The index to pop from.

        Returns:
            Any: The popped item.

        Raises:
            IndexError: If the array is empty or index is out of range.
            RuntimeError: If the C API call fails.
        """
        size = len(self)
        if size == 0:
            raise IndexError("pop from empty HakkaJsonArray.")
        if index < 0:
            index += size
        if not (0 <= index < size):
            raise IndexError("pop index out of range.")

        popped_handle = CHakkaHandle()
        result = _pop_array_func(self._c_hakka_handle, index, byref(popped_handle))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to pop item at index {index}: {result.name}.")
        return handle_to_object(popped_handle)

    def clear(self):
        """
        Remove all items from the array.

        Raises:
            RuntimeError: If the C API call fails.
        """
        result = _clear_array_func(self._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to clear HakkaJsonArray: {result.name}.")

    def count(self, value: Any) -> int:
        """
        Return the number of occurrences of a value.

        Args:
            value (Any): The value to count.

        Returns:
            int: The count of the value.

        Raises:
            RuntimeError: If the C API call fails.
        """
        value_obj = (
            obj_from_python(value)
            if not issubclass(type(value), HakkaJsonBase)
            else value
        )
        count = c_uint32()
        result = _count_array_func(
            self._c_hakka_handle, value_obj._c_hakka_handle, byref(count)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to count occurrences in HakkaJsonArray: {result.name}."
            )
        return count.value

    def index(self, value: Any, start: int = 0, stop: Optional[int] = None) -> int:
        """
        Return first index of value.

        Args:
            value (Any): The value to find.
            start (int, optional): Start index.
            stop (int, optional): Stop index.

        Returns:
            int: The index of the first occurrence.

        Raises:
            ValueError: If the value is not found.
            TypeError: If value type is unsupported.
            RuntimeError: If the C API call fails.
        """
        value_obj = (
            obj_from_python(value) if not isinstance(value, HakkaJsonBase) else value
        )
        stop = stop if stop is not None else len(self)

        index = c_uint32()
        result = _find_first_array_func(
            self._c_hakka_handle,
            value_obj._c_hakka_handle,
            start,
            stop,
            byref(index),
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            raise ValueError("Value not found in HakkaJsonArray.")
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Value not found in HakkaJsonArray: {result.name}.")
        return index.value

    def reverse(self):
        """
        Reverse the elements of the array in place.

        Raises:
            RuntimeError: If the C API call fails.
        """
        result = _reverse_array_func(self._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to reverse HakkaJsonArray: {result.name}.")

    def copy(self) -> "HakkaJsonArray":
        """
        Return a shallow copy of the array.

        Returns:
            HakkaJsonArray: The shallow copy.
        """
        return HakkaJsonArray([item for item in self])

    def sort(self, key=None, reverse: bool = False):
        """
        Sort the array in place.

        Args:
            key (callable, optional): The key function to use for sorting.
            reverse (bool, optional): True to sort in descending order.

        Raises:
            RuntimeError: If the C API call fails.
        """
        # Get list of Hakka objects (not converted to Python)
        items = [item for item in self]
        items.sort(key=key, reverse=reverse)
        self.clear()
        self.extend(items)

    def __add__(
        self, iterable: Union["HakkaJsonArray", list, tuple]
    ) -> "HakkaJsonArray":
        """
        Concatenate two HakkaJsonArrays.

        Args:
            iterable (HakkaJsonArray, list, or tuple): The iterable to add from.

        Returns:
            HakkaJsonArray: The concatenated array.

        Raises:
            TypeError: If iterable type is unsupported.
            RuntimeError: If the C API call fails.
        """
        if isinstance(iterable, (list, tuple)):
            iterable = HakkaJsonArray(iterable)
        elif not isinstance(iterable, HakkaJsonArray):
            raise TypeError("Can only concatenate HakkaJsonArray with HakkaJsonArray.")
        new_array = self.copy()
        result = _extend_array_func(new_array._c_hakka_handle, iterable._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to concatenate HakkaJsonArray: {result.name}.")
        return new_array

    def __iadd__(self, other: Union["HakkaJsonArray", list, tuple]) -> "HakkaJsonArray":
        """
        In-place concatenation of two HakkaJsonArrays.

        Args:
            other (HakkaJsonArray, list, or tuple): The array to concatenate.

        Returns:
            HakkaJsonArray: The updated array.

        Raises:
            TypeError: If other type is unsupported.
            RuntimeError: If the C API call fails.
        """
        self.extend(other)
        return self

    def __mul__(self, times: int) -> "HakkaJsonArray":
        """
        Multiply the array by a scalar.

        Args:
            times (int): The number of times to repeat the array.

        Returns:
            HakkaJsonArray: The multiplied array.

        Raises:
            TypeError: If times is not an integer.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(times, int):
            raise TypeError("Can only multiply HakkaJsonArray by an integer.")

        new_array = self.copy()
        result = _multiply_array_func(new_array._c_hakka_handle, times)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to multiply HakkaJsonArray: {result.name}.")
        return new_array

    def __rmul__(self, times: int) -> "HakkaJsonArray":
        """
        Reverse multiplication to support int * HakkaJsonArray.

        Args:
            times (int): The number of times to repeat the array.

        Returns:
            HakkaJsonArray: The multiplied array.

        Raises:
            TypeError: If times is not an integer.
            RuntimeError: If the C API call fails.
        """
        return self.__mul__(times)

    def __imul__(self, times: int) -> "HakkaJsonArray":
        """
        In-place multiplication of the array by a scalar.

        Args:
            times (int): The number of times to repeat the array.

        Returns:
            HakkaJsonArray: The updated array.

        Raises:
            TypeError: If times is not an integer.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(times, int):
            raise TypeError("Can only multiply HakkaJsonArray by an integer.")

        result = _multiply_array_func(self._c_hakka_handle, times)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to multiply HakkaJsonArray: {result.name}.")
        return self

    def __reversed__(self) -> "HakkaJsonArrayIterator":
        """
        Return a reverse iterator over the array.

        Returns:
            HakkaJsonArrayIterator: The reverse iterator.
        """
        return HakkaJsonArrayIterator(self, reverse=True)

    def __repr__(self) -> str:
        """
        Return the string representation of the array.

        Returns:
            str: The string representation.
        """
        # Show the actual Hakka objects, not their Python conversions
        items = [repr(item) for item in self]
        return f"HakkaJsonArray([{', '.join(items)}])"

    def __str__(self) -> str:
        """
        Return the informal string representation of the array.

        Returns:
            str: The string representation.
        """
        # Show the actual Hakka objects, not their Python conversions
        items = [repr(item) for item in self]
        return f"[{', '.join(items)}]"

    def __reduce__(self):
        """
        Support for pickle.

        Returns:
            tuple: The reduction tuple.
        """
        return (HakkaJsonArray.from_python, (self.to_python(),))

    def __hash__(self) -> int:
        """
        Compute the hash value of the array.

        Note:
            In Python, mutable objects like lists are unhashable.
            Implementing __hash__ can lead to unexpected behavior.
            It's recommended to remove this method unless immutability is enforced.

        Raises:
            TypeError: Always, as lists are unhashable.
        """
        raise TypeError("unhashable type: 'HakkaJsonArray'")

    def _compare(self, other: Union["HakkaJsonArray", list, tuple], op) -> bool:
        """
        Compare the array with another HakkaJsonArray.

        Args:
            other (HakkaJsonArray, list, or tuple): The other array to compare.
            op (callable): The comparison operator.

        Returns:
            bool: The result of the comparison.

        Raises:
            TypeError: If other type is unsupported.
            RuntimeError: If the C API call fails.
        """
        if not isinstance(other, (HakkaJsonArray, list, tuple)):
            return NotImplemented
        if not isinstance(other, HakkaJsonArray):
            other = HakkaJsonArray(other)

        comparison_result = c_int32()
        result = _compare_func(
            self._c_hakka_handle, other._c_hakka_handle, byref(comparison_result)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to compare HakkaJsonArray: {result.name}.")
        return op(comparison_result.value, 0)

    def __eq__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x == y)

    def __ne__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x != y)

    def __lt__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x < y)

    def __le__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x <= y)

    def __gt__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x > y)

    def __ge__(self, other: Any) -> bool:
        return self._compare(other, lambda x, y: x >= y)

    def __or__(self, other: Union["HakkaJsonArray", list, tuple]) -> "HakkaJsonArray":
        """
        OR operator to concatenate arrays.

        Args:
            other (HakkaJsonArray, list, or tuple): The array to concatenate.

        Returns:
            HakkaJsonArray: The concatenated array.

        Raises:
            TypeError: If other type is unsupported.
            RuntimeError: If the C API call fails.
        """
        if isinstance(other, (list, tuple)):
            other = HakkaJsonArray(other)
        elif not isinstance(other, HakkaJsonArray):
            raise TypeError("Can only concatenate HakkaJsonArray with HakkaJsonArray.")
        new_array = self.copy()
        result = _extend_array_func(new_array._c_hakka_handle, other._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to concatenate HakkaJsonArray: {result.name}.")
        return new_array

    def __ior__(self, other: Union["HakkaJsonArray", list, tuple]) -> "HakkaJsonArray":
        """
        In-place OR operator to concatenate arrays.

        Args:
            other (HakkaJsonArray, list, or tuple): The array to concatenate.

        Returns:
            HakkaJsonArray: The updated array.

        Raises:
            TypeError: If other type is unsupported.
            RuntimeError: If the C API call fails.
        """
        self.extend(other)
        return self

    def __dir__(self):
        return super().__dir__() + [
            "__init__",
            "_construct",
            "loads",
            "to_python",
            "from_python",
            "dumps",
            "__bool__",
            "__len__",
            "__getitem__",
            "__setitem__",
            "_get_item",
            "_get_slice",
            "_set_item",
            "_set_slice",
            "__delitem__",
            "_remove_item",
            "__contains__",
            "append",
            "extend",
            "insert",
            "remove",
            "pop",
            "clear",
            "count",
            "index",
            "reverse",
            "copy",
            "sort",
            "__add__",
            "__iadd__",
            "__mul__",
            "__rmul__",
            "__imul__",
            "__reversed__",
            "__repr__",
            "__str__",
            "__reduce__",
            "__hash__",
            "_compare",
            "__eq__",
            "__ne__",
            "__lt__",
            "__le__",
            "__gt__",
            "__ge__",
            "__or__",
            "__ior__",
            "__dir__",
        ]


class HakkaJsonArrayIterator:
    """
    Iterator for HakkaJsonArray.
    Supports forward and reverse iteration.
    """

    __slots__ = ("_c_iter", "_end")

    def __init__(self, array: HakkaJsonArray, reverse: bool = False):
        self._c_iter = CHakkaArrayIter()
        create_iter_fn = (
            _create_array_iter_rbegin_func if reverse else _create_array_iter_begin_func
        )
        result = create_iter_fn(array._c_hakka_handle, byref(self._c_iter))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(
                f"Failed to create HakkaJsonArrayIterator: {result.name}."
            )
        self._end = False

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if self._end:
            raise StopIteration

        value_handle = CHakkaHandle()
        result = _get_array_iter_deref_func(self._c_iter, byref(value_handle))
        if result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
            self._end = True
            raise StopIteration
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to dereference iterator: {result.name}.")

        value = handle_to_object(value_handle)

        # Move to next element
        move_result = _move_array_iter_next_func(self._c_iter)
        if move_result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
            self._end = True
        elif move_result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to move iterator: {move_result.name}.")

        return value

    def __del__(self):
        if hasattr(self, "_c_iter") and self._c_iter:
            _release_array_iter_func(byref(self._c_iter))

    def __dir__(self):
        return ["__init__", "__iter__", "__next__", "__del__", "__dir__"]
