"""
Dispatcher for Hakka JSON types.

Converts pure Python objects to HakkaJson objects.
"""

from typing import Union
from ctypes import c_uint32, byref

from ._hakka_json_null import HakkaJsonNull
from ._hakka_json_int import HakkaJsonInt
from ._hakka_json_float import HakkaJsonFloat
from ._hakka_json_bool import HakkaJsonBool
from ._hakka_json_invalid import HakkaJsonInvalid
from ._hakka_json_base import HakkaJsonBase

from ._hakka_json_loader import CHakkaHandle, dispatch_table
from ._hakka_json_enum import HakkaJsonResultEnum, HakkaJsonTypeEnum


__all__ = ["obj_from_python", "handle_to_object", "normalize_to_native"]

_hakka_type = dispatch_table["HakkaType"]
_release_func = dispatch_table["HakkaRelease"]

STATIC_CLASS_STRING = None
STATIC_CLASS_ARRAY = None
STATIC_CLASS_OBJECT = None
STATIC_COMPLETED = False


# import once to avoid circular imports
def _staic_imports():
    global STATIC_COMPLETED  # pylint: disable=global-statement
    if STATIC_COMPLETED:
        return

    from ._hakka_json_string import HakkaJsonString
    from ._hakka_json_array import HakkaJsonArray
    from ._hakka_json_object import HakkaJsonObject

    global STATIC_CLASS_STRING  # pylint: disable=global-statement
    global STATIC_CLASS_ARRAY  # pylint: disable=global-statement
    global STATIC_CLASS_OBJECT  # pylint: disable=global-statement

    if STATIC_CLASS_STRING is None:
        STATIC_CLASS_STRING = HakkaJsonString
    if STATIC_CLASS_ARRAY is None:
        STATIC_CLASS_ARRAY = HakkaJsonArray
    if STATIC_CLASS_OBJECT is None:
        STATIC_CLASS_OBJECT = HakkaJsonObject
    STATIC_COMPLETED = True


def obj_from_python(  # pylint: disable=too-many-return-statements
    obj,
) -> Union[
    HakkaJsonInvalid,
    HakkaJsonNull,
    HakkaJsonBool,
    HakkaJsonInt,
    HakkaJsonFloat,
    "HakkaJsonString",
    "HakkaJsonArray",
    "HakkaJsonObject",
]:
    """
    Convert a Python object to a HakkaJson object.

    Args:
        obj: The pure Python object to convert.

    Returns:
        HakkaJsonBase: The HakkaJson object.
    """
    _staic_imports()

    if obj is None:
        return HakkaJsonNull()
    elif isinstance(obj, bool):
        return HakkaJsonBool(obj)
    elif isinstance(obj, int):
        return HakkaJsonInt(obj)
    elif isinstance(obj, float):
        return HakkaJsonFloat(obj)
    elif isinstance(obj, str):
        return STATIC_CLASS_STRING(obj)
    elif isinstance(obj, list):
        return STATIC_CLASS_ARRAY(
            obj
        )  # pylint: disable=possibly-used-before-assignment
    elif isinstance(obj, dict):
        return STATIC_CLASS_OBJECT()
    else:
        return HakkaJsonInvalid()


def handle_to_object(
    handle: CHakkaHandle,
) -> Union[
    HakkaJsonInvalid,
    HakkaJsonNull,
    HakkaJsonBool,
    HakkaJsonInt,
    HakkaJsonFloat,
    "HakkaJsonString",
    "HakkaJsonArray",
    "HakkaJsonObject",
]:  # pylint: disable=too-many-return-statements
    """
    Convert a CHakkaHandle to the corresponding HakkaJson object.

    Args:
        handle (CHakkaHandle): The handle to convert.

    Returns:
        HakkaJsonBase: The corresponding HakkaJson object.
    """
    _staic_imports()

    type_id = c_uint32(-1)
    result = _hakka_type(handle, byref(type_id))
    if result != HakkaJsonResultEnum.HAKKA_JSON_SUCCESS:
        _release_func(byref(handle))
        raise RuntimeError(f"Failed to get type of HakkaJson object {result.name}.")

    base = HakkaJsonBase(handle)
    match HakkaJsonTypeEnum(type_id.value):
        case HakkaJsonTypeEnum.HAKKA_JSON_INT:
            return HakkaJsonInt(base)
        case HakkaJsonTypeEnum.HAKKA_JSON_FLOAT:
            return HakkaJsonFloat(base)
        case HakkaJsonTypeEnum.HAKKA_JSON_BOOL:
            return HakkaJsonBool.handle_to_instance(handle)
        case HakkaJsonTypeEnum.HAKKA_JSON_NULL:
            return HakkaJsonNull()
        case HakkaJsonTypeEnum.HAKKA_JSON_STRING:
            return STATIC_CLASS_STRING(base)
        case HakkaJsonTypeEnum.HAKKA_JSON_ARRAY:
            return STATIC_CLASS_ARRAY(base)
        case HakkaJsonTypeEnum.HAKKA_JSON_OBJECT:
            return STATIC_CLASS_OBJECT(base)
        case HakkaJsonTypeEnum.HAKKA_JSON_INVALID:
            return HakkaJsonInvalid()
        case _:
            _release_func(byref(handle))
            raise RuntimeError(f"Unsupported HakkaJson type {type_id.value}.")
    return HakkaJsonInvalid()


def normalize_to_native(obj: Union[list, dict, HakkaJsonBase]):
    """
    Normalize a Python object to a native object.

    Args:
        obj: The Python object to normalize.

    Returns:
        Union[list, dict]: The normalized object.
    """
    if isinstance(obj, HakkaJsonBase):
        return obj.to_python()
    if isinstance(obj, dict):
        return {
            normalize_to_native(key): normalize_to_native(value)
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [normalize_to_native(value) for value in obj]
    return obj
