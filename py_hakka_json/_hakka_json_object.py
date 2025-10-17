"""
HakkaJsonObject class definition.
Represents a JSON object value in HakkaJson.
Implements dict-like behavior.
"""

from ctypes import byref, c_uint32, c_uint8, c_int32, c_uint64
from typing import Any, Iterable, Optional, Tuple, Union

from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_loader import CHakkaHandle, CHakkaObjectIter, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum
from ._hakka_json_type_dispatcher import obj_from_python, handle_to_object

__all__ = ["HakkaJsonObject", "HakkaJsonObjectIterator"]

# Dispatch functions for object manipulation
_compare_func = dispatch_table["HakkaCompare"]
_create_object_func = dispatch_table["CreateHakkaObject"]
_loads_object_func = dispatch_table["LoadsHakkaObject"]
_dump_object_func = dispatch_table["DumpHakkaObject"]
_dump_size_object_func = dispatch_table["HakkaDumpSize"]

_set_object_func = dispatch_table["SetHakkaObject"]
_get_object_object_func = dispatch_table["GetHakkaObjectObject"]
_remove_object_key_func = dispatch_table["RemoveHakkaObjectKey"]
_get_object_size_func = dispatch_table["GetHakkaObjectSize"]
_contains_object_key_func = dispatch_table["ContainsHakkaObjectKey"]
_create_object_from_keys_func = dispatch_table["CreateHakkaObjectFromKeys"]
_pop_object_func = dispatch_table["PopHakkaObject"]
_pop_item_object_func = dispatch_table["PopItemHakkaObject"]
_clear_object_func = dispatch_table["ClearHakkaObject"]
_update_object_func = dispatch_table["UpdateHakkaObject"]

# Iterators
_create_object_iter_begin_func = dispatch_table["CreateHakkaObjectIterBegin"]
_move_object_iter_next_func = dispatch_table["MoveHakkaObjectIterNext"]
_get_object_iter_deref_func = dispatch_table["GetHakkaObjectIterDeref"]
_release_object_iter_func = dispatch_table["HakkaObjectIterRelease"]


class HakkaJsonObject(HakkaJsonBase):
    """
    Represents a JSON object value in HakkaJson.
    Implements dict-like behavior.
    """

    __slots__ = ()

    def __init__(self, initial: Optional[Union["HakkaJsonObject", dict]] = None):
        if isinstance(initial, HakkaJsonObject):
            self._c_hakka_handle = initial._c_hakka_handle
        elif isinstance(initial, HakkaJsonBase):
            if initial.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_OBJECT:
                raise TypeError("HakkaJsonObject initialization requires an object.")
            self._c_hakka_handle = initial._c_hakka_handle
            initial._c_hakka_handle = None  # move from Base to Object
        elif initial is None:
            self._c_hakka_handle = self._construct()
        elif isinstance(initial, dict):
            new_dict = HakkaJsonObject()
            for key, value in initial.items():
                new_dict[key] = value
            self._c_hakka_handle = new_dict._c_hakka_handle
            new_dict._c_hakka_handle = None  # move from dict to Object
        else:
            raise TypeError("Unsupported type for HakkaJsonObject initialization.")
        super().__init__(self._c_hakka_handle)

    @staticmethod
    def loads(json_str: str, max_depth: int = 512) -> "HakkaJsonObject":
        """
        Deserialize a JSON string into a HakkaJsonObject.

        Args:
            json_str (str): The JSON string to deserialize.
            max_depth (int, optional): Maximum recursion depth for deserialization.

        Returns:
            HakkaJsonObject: The deserialized HakkaJsonObject.

        Raises:
            TypeError: If json_str is not a string or bytes.
            ValueError: If the JSON string is invalid.
            RecursionError: If the recursion depth is exceeded.
            RuntimeError: If deserialization fails.
        """
        if not isinstance(json_str, (str, bytes)):
            raise TypeError("loads() expects a string or UTF-8 bytes.")
        if isinstance(json_str, str):
            json_str = json_str.encode("utf-8")
        buffer_size = c_uint32(len(json_str))
        buffer = (c_uint8 * buffer_size.value).from_buffer_copy(json_str)
        c_hakka_handle = CHakkaHandle()
        result = _loads_object_func(
            buffer, buffer_size, byref(c_hakka_handle), c_uint32(max_depth)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            HakkaJsonObject._handle_load_error(result)
        return HakkaJsonObject(HakkaJsonBase(c_hakka_handle))

    @staticmethod
    def _construct() -> CHakkaHandle:
        c_hakka_handle = CHakkaHandle()
        result = _create_object_func(byref(c_hakka_handle))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to create HakkaJsonObject: {result.name}.")
        return c_hakka_handle

    @staticmethod
    def _handle_load_error(result):
        if result == HakkaJsonResultEnum.HAKKA_JSON_PARSE_ERROR:
            raise ValueError("Invalid JSON string for HakkaJsonObject.")
        elif result == HakkaJsonResultEnum.HAKKA_JSON_RECURSION_DEPTH_EXCEEDED:
            raise RecursionError("Recursion depth exceeded in HakkaJsonObject.")
        else:
            raise RuntimeError(f"Failed to load HakkaJsonObject: {result.name}.")

    def to_python(self) -> dict:
        result_dict = {}
        iter_handle = CHakkaObjectIter()
        result = _create_object_iter_begin_func(
            self._c_hakka_handle, byref(iter_handle)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to create iterator: {result.name}.")

        try:
            while True:
                key_handle = CHakkaHandle()
                value_handle = CHakkaHandle()
                iter_result = _get_object_iter_deref_func(
                    iter_handle, byref(key_handle), byref(value_handle)
                )
                if iter_result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
                    break
                elif iter_result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                    raise RuntimeError(
                        f"Iterator dereference failed: {iter_result.name}."
                    )

                key_obj = handle_to_object(key_handle).to_python()
                value_obj = handle_to_object(value_handle).to_python()
                result_dict[key_obj] = value_obj

                move_result = _move_object_iter_next_func(iter_handle)
                if move_result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
                    break
                elif move_result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                    raise RuntimeError(f"Iterator move failed: {move_result.name}.")
        finally:
            _release_object_iter_func(byref(iter_handle))

        return result_dict

    @staticmethod
    def from_python(py_dict: dict) -> "HakkaJsonObject":
        if not isinstance(py_dict, dict):
            raise TypeError("from_python expects a dict.")
        return HakkaJsonObject(py_dict)

    def dumps(self, max_depth: int = 512) -> str:
        buffer_size = c_uint64()
        # _dump_size_object_func
        result = _dump_size_object_func(self._c_hakka_handle, byref(buffer_size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get dump size: {result.name}.")

        buffer = (c_uint8 * buffer_size.value)()
        result = _dump_object_func(
            self._c_hakka_handle, c_uint32(max_depth), buffer, byref(buffer_size)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to dump HakkaJsonObject: {result.name}.")
        return bytes(buffer[: buffer_size.value]).decode("utf-8")

    def __len__(self) -> int:
        size = c_uint32()
        result = _get_object_size_func(self._c_hakka_handle, byref(size))
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Failed to get size: {result.name}.")
        return size.value

    def __getitem__(self, key: str) -> Any:
        self._validate_key(key)
        key_buffer, key_length = self._encode_key(key)
        value_handle = CHakkaHandle()
        result = _get_object_object_func(
            self._c_hakka_handle, key_buffer, key_length, byref(value_handle)
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            raise KeyError(key)
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Get item failed: {result.name}.")
        return handle_to_object(value_handle)

    def __setitem__(self, key: str, value: Any):
        self._validate_key(key)
        key_buffer, key_length = self._encode_key(key)
        value_obj = (
            obj_from_python(value)
            if not issubclass(type(value), HakkaJsonBase)
            else value
        )
        result = _set_object_func(
            self._c_hakka_handle, key_buffer, key_length, value_obj._c_hakka_handle
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Set item failed: {result.name}.")

    def __delitem__(self, key: str):
        self._validate_key(key)
        key_buffer, key_length = self._encode_key(key)
        result = _remove_object_key_func(self._c_hakka_handle, key_buffer, key_length)
        if result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            raise KeyError(key)
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Delete item failed: {result.name}.")

    def __contains__(self, key: str) -> bool:
        self._validate_key(key)
        key_buffer, key_length = self._encode_key(key)
        result_bool = c_uint8()
        result = _contains_object_key_func(
            self._c_hakka_handle, key_buffer, key_length, byref(result_bool)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Contains check failed: {result.name}.")
        return bool(result_bool.value)

    def __iter__(self):
        return HakkaJsonObjectIterator(self)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key: str, default: Optional[Any] = None) -> Any:
        if key in self:
            return self[key]
        self[key] = default
        return default

    def pop(self, key: str, default: Optional[Any] = None) -> Any:
        self._validate_key(key)
        key_buffer, key_length = self._encode_key(key)
        value_handle = CHakkaHandle()
        result = _pop_object_func(
            self._c_hakka_handle, key_buffer, key_length, byref(value_handle)
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            return handle_to_object(value_handle)
        elif result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            if default is not None:
                return default
            raise KeyError(key)
        else:
            raise RuntimeError(f"Pop failed: {result.name}.")

    def popitem(self) -> Tuple[str, Any]:
        key_handle = CHakkaHandle()
        value_handle = CHakkaHandle()
        result = _pop_item_object_func(
            self._c_hakka_handle, byref(key_handle), byref(value_handle)
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            key = handle_to_object(key_handle).to_python()
            value = handle_to_object(value_handle)
            return key, value
        elif result == HakkaJsonResultEnum.HAKKA_JSON_KEY_NOT_FOUND:
            raise KeyError("popitem(): dictionary is empty")
        else:
            raise RuntimeError(f"Popitem failed: {result.name}.")

    def keys(self) -> Iterable[str]:
        return self.__iter__()

    def values(self) -> Iterable[Any]:
        return (self[key] for key in self)

    def items(self) -> Iterable[Tuple[str, Any]]:
        return ((key, self[key]) for key in self)

    def update(
        self, other: Union["HakkaJsonObject", dict, Iterable[Tuple[str, Any]]], **kwargs
    ):
        if other is None and not kwargs:
            return
        other_obj = other
        if not isinstance(other, (HakkaJsonObject, dict, Iterable)):
            raise TypeError(
                "update() argument must be a mapping or iterable of key/value pairs."
            )

        if isinstance(other, dict):
            other_obj = HakkaJsonObject(other)
        elif isinstance(other, Iterable):
            other_obj = HakkaJsonObject(dict(other))

        result = _update_object_func(
            self._c_hakka_handle,
            other_obj._c_hakka_handle,  # pylint: disable=protected-access
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Update failed: {result.name}.")
        if kwargs:
            self.update(kwargs)

    def clear(self):
        result = _clear_object_func(self._c_hakka_handle)
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Clear failed: {result.name}.")

    def copy(self) -> "HakkaJsonObject":
        return HakkaJsonObject(self)

    @classmethod
    def fromkeys(
        cls, iterable: Iterable[str], value: Optional[Any] = None
    ) -> "HakkaJsonObject":
        keys_array = obj_from_python(iterable)
        if keys_array.get_type() != HakkaJsonTypeEnum.HAKKA_JSON_ARRAY:
            raise TypeError("fromkeys() requires an iterable of strings.")

        value_obj = (
            obj_from_python(value)
            if not issubclass(type(value), HakkaJsonBase)
            else value
        )
        result_handle = CHakkaHandle()
        result = _create_object_from_keys_func(
            keys_array._c_hakka_handle,  # pylint: disable=protected-access
            value_obj._c_hakka_handle,  # pylint: disable=protected-access
            byref(result_handle),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"fromkeys() failed: {result.name}.")
        return handle_to_object(result_handle)

    def __repr__(self) -> str:
        return f"HakkaJsonObject({self.to_python()})"

    def __str__(self) -> str:
        return str(self.to_python())

    def __eq__(self, other):
        return self._compare(other, lambda x, y: x == y)

    def __ne__(self, other):
        return self._compare(other, lambda x, y: x != y)

    def __lt__(self, other):
        return self._compare(other, lambda x, y: x < y)

    def __le__(self, other):
        return self._compare(other, lambda x, y: x <= y)

    def __gt__(self, other):
        return self._compare(other, lambda x, y: x > y)

    def __ge__(self, other):
        return self._compare(other, lambda x, y: x >= y)

    def _compare(self, other, op):
        if not isinstance(other, (HakkaJsonObject, dict)):
            return NotImplemented
        if not isinstance(other, HakkaJsonObject):
            other = HakkaJsonObject(other)

        comparison_result = c_int32()
        result = _compare_func(
            self._c_hakka_handle,
            other._c_hakka_handle,  # pylint: disable=protected-access
            byref(comparison_result),
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Comparison failed: {result.name}.")
        return op(comparison_result.value, 0)

    def __or__(self, other):
        """
        OR operator.
        """
        if not isinstance(other, (HakkaJsonObject, dict)):
            return NotImplemented
        new_obj = self.copy()
        new_obj.update(other)
        return new_obj

    def __ior__(self, other):
        """
        In-place OR operator.
        """
        self.update(other)
        return self

    def __hash__(self):
        """
        HakkaJsonObject is not hashable. Alias to dict.__hash__.
        """
        raise TypeError("unhashable type: 'HakkaJsonObject'")

    def __reduce__(self):
        """
        Pickle support.
        """
        return (HakkaJsonObject.from_python, (self.to_python(),))

    @staticmethod
    def _validate_key(key):
        """
        Validate that a key is a string.
        """
        if not isinstance(key, str):
            raise TypeError("Keys must be strings.")

    @staticmethod
    def _encode_key(key):
        """
        Encode a key string to a buffer and length for use in HakkaJson functions.
        """
        key_bytes = key.encode("utf-8")
        key_length = c_uint32(len(key_bytes))
        key_buffer = (c_uint8 * key_length.value).from_buffer_copy(key_bytes)
        return key_buffer, key_length

    @staticmethod
    def __class__():
        """
        Return HakkaJsonObject class.
        """
        return HakkaJsonObject

    @classmethod
    def __class_getitem__(cls, item):
        """
        Return HakkaJsonObject class.
        """
        return HakkaJsonObject

    def __format__(self, format_spec: str) -> str:
        """
        Return the formatted string representation.

        Args:
            format_spec (str): The format specification.

        Returns:
            str: The formatted string.
        """
        return format(str(self), format_spec)

    def __sizeof__(self) -> int:
        """
        Return the size of the array in memory.

        Returns:
            int: The size of the array.
        """
        return super().__sizeof__() + self.__len__()

    def __getnewargs_ex__(self):
        """
        Return new arguments for object creation during unpickling.

        Returns:
            tuple: A tuple containing the arguments and keyword arguments.
        """
        return (self.to_python(),), {}

    def __getnewargs__(self):
        """
        Return new arguments for object creation during unpickling.

        Returns:
            tuple: The arguments tuple.
        """
        return (self.to_python(),)

    def __reduce_ex__(self, protocol: int):
        """
        Support for pickle.

        Args:
            protocol (int): The pickle protocol version.

        Returns:
            tuple: The reduction tuple.
        """
        return self.__reduce__()

    def __setstate__(self, state):
        """
        Set the state of the object during unpickling.

        Args:
            state (Any): The state to set.
        """
        self.__init__(state)

    def __dir__(self):
        return super().__dir__() + [
            "__init__",
            "loads",
            "_construct",
            "_handle_load_error",
            "to_python",
            "from_python",
            "dump",
            "__len__",
            "__getitem__",
            "__setitem__",
            "__delitem__",
            "__contains__",
            "__iter__",
            "get",
            "setdefault",
            "pop",
            "popitem",
            "keys",
            "values",
            "items",
            "update",
            "clear",
            "copy",
            "fromkeys",
            "__repr__",
            "__str__",
            "__eq__",
            "__ne__",
            "__lt__",
            "__le__",
            "__gt__",
            "__ge__",
            "_compare",
            "__or__",
            "__ior__",
            "__hash__",
            "__reduce__",
            "_validate_key",
            "_encode_key",
            "__class__",
            "__class_getitem__",
            "__format__",
            "__sizeof__",
            "__getnewargs_ex__",
            "__getnewargs__",
            "__reduce_ex__",
            "__setstate__",
            "__dir__",
        ]


class HakkaJsonObjectIterator:
    """
    Iterator over HakkaJsonObject keys.
    """

    __slots__ = ("_c_iter", "_end")

    def __init__(self, hakka_obj: HakkaJsonObject):
        self._c_iter = CHakkaObjectIter()
        result = _create_object_iter_begin_func(
            hakka_obj._c_hakka_handle, byref(self._c_iter)
        )
        if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Iterator creation failed: {result.name}.")
        self._end = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._end:
            raise StopIteration
        key_handle = CHakkaHandle()
        value_handle = CHakkaHandle()
        result = _get_object_iter_deref_func(
            self._c_iter, byref(key_handle), byref(value_handle)
        )
        if result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
            self._end = True
            raise StopIteration
        elif result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Iterator dereference failed: {result.name}.")

        move_result = _move_object_iter_next_func(self._c_iter)
        if move_result == HakkaJsonResultEnum.HAKKA_JSON_ITERATOR_END:
            self._end = True
        elif move_result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
            raise RuntimeError(f"Iterator move failed: {move_result.name}.")

        key_obj = handle_to_object(key_handle).to_python()
        return key_obj

    def __del__(self):
        if hasattr(self, "_c_iter") and self._c_iter:
            result = _release_object_iter_func(byref(self._c_iter))
            if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
                import warnings

                warnings.warn(
                    f"Iterator release failed: {result.name}.", ResourceWarning
                )

    def __dir__(self):
        return ["__iter__", "__next__", "__del__"]
