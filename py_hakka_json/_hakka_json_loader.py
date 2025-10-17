#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to load the CHakkaHandle shared library and define C API functions.
"""

import os
import sys
import ctypes

from ._hakka_json_enum import HakkaJsonResultEnum

__all__ = [
    "dispatch_table",
    "CHakkaHandle",
    "CHakkaStringIter",
    "CHakkaArrayIter",
    "CHakkaObjectIter",
]


def _platform_lib_mangling(name: str, sys_platform: str) -> str:
    """
    Mangle the shared library name based on the platform.

    Args:
        name (str): The base name of the library.
        sys_platform (str): The platform's identifier from sys.platform.

    Returns:
        str: The correct shared library filename for the current platform.
    """
    platform_lib_map = {
        "linux": f"lib{name}.so",
        "darwin": f"lib{name}.dylib",
        "win32": f"{name}.dll",
    }
    if sys_platform not in platform_lib_map:
        raise OSError(f"Unsupported platform: {sys_platform}")
    return platform_lib_map.get(sys_platform)


def _load_library() -> ctypes.CDLL:
    """
    Load the CHakkaHandle shared library based on the current platform.

    Returns:
        ctypes.CDLL: The loaded shared library.
    """
    name = "hakka_json"
    lib_name = _platform_lib_mangling(name, sys.platform)
    lib_path = os.path.join(
        os.path.dirname(__file__), "_core", "src", "hakka_json", "target", "release", lib_name
    )
    if not os.path.exists(lib_path):
        raise OSError(f"Library not found at {lib_path}")

    return ctypes.CDLL(lib_path)


_lib = _load_library()


# Define the CHakkaHandle structure
class CHakkaHandle(ctypes.c_int64):  # pylint: disable=too-few-public-methods
    """
    Placeholder for CHakkaHandle object. This struct is managed by the C library.
    """

    _pack_ = 1
    _fields_ = []


class CHakkaStringIter(ctypes.c_int64):  # pylint: disable=too-few-public-methods
    """
    Placeholder for CHakkaStringIter object. This struct is managed by the C library.
    """

    _pack_ = 1
    _fields_ = []


class CHakkaArrayIter(ctypes.c_int64):  # pylint: disable=too-few-public-methods
    """
    Placeholder for CHakkaArrayIter object. This struct is managed by the C library.
    """

    _pack_ = 1
    _fields_ = []


class CHakkaObjectIter(ctypes.c_int64):  # pylint: disable=too-few-public-methods
    """
    Placeholder for CHakkaObjectIter object. This struct is managed by the C library.
    """

    _pack_ = 1
    _fields_ = []


dispatch_table = {
    # Base functions
    "HakkaRelease": _lib.HakkaRelease,
    "HakkaDump": _lib.HakkaDump,
    "HakkaToBytes": _lib.HakkaToBytes,
    "HakkaIsValid": _lib.HakkaIsValid,
    "HakkaType": _lib.HakkaType,
    "HakkaCompare": _lib.HakkaCompare,
    "HakkaHash": _lib.HakkaHash,
    "HakkaDumpSize": _lib.HakkaDumpSize,
    "HakkaReclaim": _lib.HakkaReclaim,
    # Primitive functions
    "CreateHakkaInt": _lib.CreateHakkaInt,
    "CreateHakkaFloat": _lib.CreateHakkaFloat,
    "CreateHakkaNull": _lib.CreateHakkaNull,
    "CreateHakkaBool": _lib.CreateHakkaBool,
    "CreateHakkaInvalid": _lib.CreateHakkaInvalid,
    "GetHakkaInt": _lib.GetHakkaInt,
    "GetHakkaFloat": _lib.GetHakkaFloat,
    "GetHakkaBool": _lib.GetHakkaBool,
    # String functions
    "CreateHakkaString": _lib.CreateHakkaString,
    "GetHakkaString": _lib.GetHakkaString,
    "GetHakkaStringLength": _lib.GetHakkaStringLength,
    "GetHakkaStringCapitalize": _lib.GetHakkaStringCapitalize,
    "GetHakkaStringCasefold": _lib.GetHakkaStringCasefold,
    "GetHakkaStringCount": _lib.GetHakkaStringCount,
    "GetHakkaStringEndswith": _lib.GetHakkaStringEndswith,
    "GetHakkaStringFind": _lib.GetHakkaStringFind,
    "GetHakkaStringConcatenate": _lib.GetHakkaStringConcatenate,
    "GetHakkaStringMultiply": _lib.GetHakkaStringMultiply,
    "GetHakkaStringSlice": _lib.GetHakkaStringSlice,
    "GetHakkaStringLower": _lib.GetHakkaStringLower,
    "GetHakkaStringRemoveprefix": _lib.GetHakkaStringRemoveprefix,
    "GetHakkaStringRemovesuffix": _lib.GetHakkaStringRemovesuffix,
    "GetHakkaStringReplace": _lib.GetHakkaStringReplace,
    "GetHakkaStringRfind": _lib.GetHakkaStringRfind,
    "GetHakkaStringRsplit": _lib.GetHakkaStringRsplit,
    "GetHakkaStringSplit": _lib.GetHakkaStringSplit,
    "GetHakkaStringSplitlines": _lib.GetHakkaStringSplitlines,
    "GetHakkaStringStartswith": _lib.GetHakkaStringStartswith,
    "GetHakkaStringUpper": _lib.GetHakkaStringUpper,
    "GetHakkaStringSwapcase": _lib.GetHakkaStringSwapcase,
    "GetHakkaStringTitle": _lib.GetHakkaStringTitle,
    "GetHakkaStringZfill": _lib.GetHakkaStringZfill,
    "GetHakkaStringUTF8Length": _lib.GetHakkaStringUTF8Length,
    # String testing functions
    "GetHakkaStringIsalnum": _lib.GetHakkaStringIsalnum,
    "GetHakkaStringIsalpha": _lib.GetHakkaStringIsalpha,
    "GetHakkaStringIsascii": _lib.GetHakkaStringIsascii,
    "GetHakkaStringIsdecimal": _lib.GetHakkaStringIsdecimal,
    "GetHakkaStringIsdigit": _lib.GetHakkaStringIsdigit,
    "GetHakkaStringIsidentifier": _lib.GetHakkaStringIsidentifier,
    "GetHakkaStringIslower": _lib.GetHakkaStringIslower,
    "GetHakkaStringIsnumeric": _lib.GetHakkaStringIsnumeric,
    "GetHakkaStringIsprintable": _lib.GetHakkaStringIsprintable,
    "GetHakkaStringIsspace": _lib.GetHakkaStringIsspace,
    "GetHakkaStringIstitle": _lib.GetHakkaStringIstitle,
    "GetHakkaStringIsupper": _lib.GetHakkaStringIsupper,
    # String iterator functions
    "CreateHakkaStringBegin": _lib.CreateHakkaStringBegin,
    "MoveHakkaStringNext": _lib.MoveHakkaStringNext,
    "GetHakkaStringDeref": _lib.GetHakkaStringDeref,
    "HakkaStringIterRelease": _lib.HakkaStringIterRelease,
    # --- Array functions ---
    # Creation and Destruction
    "CreateHakkaArray": _lib.CreateHakkaArray,
    "LoadsHakkaArray": _lib.LoadsHakkaArray,
    "DumpHakkaArray": _lib.DumpHakkaArray,
    # Array Manipulation
    "GetHakkaArrayObject": _lib.GetHakkaArrayObject,
    "SetHakkaArray": _lib.SetHakkaArray,
    "GetHakkaArraySlice": _lib.GetHakkaArraySlice,
    "SetHakkaArraySlice": _lib.SetHakkaArraySlice,
    "RemoveHakkaArrayIndex": _lib.RemoveHakkaArrayIndex,
    "ClearHakkaArray": _lib.ClearHakkaArray,
    "InsertHakkaArray": _lib.InsertHakkaArray,
    # Additional methods to support C API operations with Python list-like behavior
    "MultiplyHakkaArray": _lib.MultiplyHakkaArray,
    "GetHakkaArraySize": _lib.GetHakkaArraySize,
    "CountHakkaArray": _lib.CountHakkaArray,
    "ExtendHakkaArrayArray": _lib.ExtendHakkaArrayArray,
    "FindFirstHakkaArray": _lib.FindFirstHakkaArray,
    "PushBackHakkaArray": _lib.PushBackHakkaArray,
    "PopHakkaArray": _lib.PopHakkaArray,
    "RemoveValueHakkaArray": _lib.RemoveValueHakkaArray,
    "ReverseHakkaArray": _lib.ReverseHakkaArray,
    # // Iters
    "CreateHakkaArrayIterBegin": _lib.CreateHakkaArrayIterBegin,
    "CreateHakkaArrayIterRBegin": _lib.CreateHakkaArrayIterRBegin,
    "MoveHakkaArrayIterNext": _lib.MoveHakkaArrayIterNext,
    "MoveHakkaArrayIterPrev": _lib.MoveHakkaArrayIterPrev,
    "GetHakkaArrayIterDeref": _lib.GetHakkaArrayIterDeref,
    "HakkaArrayIterRelease": _lib.HakkaArrayIterRelease,
    # --- Object functions ---
    # Creation and Destruction
    "CreateHakkaObject": _lib.CreateHakkaObject,
    "LoadsHakkaObject": _lib.LoadsHakkaObject,
    "DumpHakkaObject": _lib.DumpHakkaObject,
    # Object Manipulation
    "SetHakkaObjectInt": _lib.SetHakkaObjectInt,
    "SetHakkaObjectFloat": _lib.SetHakkaObjectFloat,
    "SetHakkaObjectString": _lib.SetHakkaObjectString,
    "SetHakkaObjectNull": _lib.SetHakkaObjectNull,
    "GetHakkaObjectInt": _lib.GetHakkaObjectInt,
    "GetHakkaObjectFloat": _lib.GetHakkaObjectFloat,
    "GetHakkaObjectString": _lib.GetHakkaObjectString,
    "GetHakkaObjectNull": _lib.GetHakkaObjectNull,
    "GetHakkaObjectObject": _lib.GetHakkaObjectObject,
    "SetHakkaObject": _lib.SetHakkaObject,
    # Additional Object Methods
    "RemoveHakkaObjectKey": _lib.RemoveHakkaObjectKey,
    "GetHakkaObjectSize": _lib.GetHakkaObjectSize,
    "ContainsHakkaObjectKey": _lib.ContainsHakkaObjectKey,
    "GetHakkaObjectKeys": _lib.GetHakkaObjectKeys,
    "GetHakkaObjectValues": _lib.GetHakkaObjectValues,
    "CreateHakkaObjectFromKeys": _lib.CreateHakkaObjectFromKeys,
    "PopHakkaObject": _lib.PopHakkaObject,
    "PopItemHakkaObject": _lib.PopItemHakkaObject,
    "ClearHakkaObject": _lib.ClearHakkaObject,
    "UpdateHakkaObject": _lib.UpdateHakkaObject,
    # Object Iterators
    "CreateHakkaObjectIterBegin": _lib.CreateHakkaObjectIterBegin,
    "MoveHakkaObjectIterNext": _lib.MoveHakkaObjectIterNext,
    "GetHakkaObjectIterDeref": _lib.GetHakkaObjectIterDeref,
    "HakkaObjectIterRelease": _lib.HakkaObjectIterRelease,
}

dispatch_table["HakkaRelease"].restype = None
dispatch_table["HakkaRelease"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
]

# Primitive.h Base functions
dispatch_table["HakkaDump"].restype = HakkaJsonResultEnum
dispatch_table["HakkaDump"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint64),
]

dispatch_table["HakkaToBytes"].restype = HakkaJsonResultEnum
dispatch_table["HakkaToBytes"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["HakkaIsValid"].restype = HakkaJsonResultEnum
dispatch_table["HakkaIsValid"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["HakkaType"].restype = HakkaJsonResultEnum
dispatch_table["HakkaType"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["HakkaCompare"].restype = HakkaJsonResultEnum
dispatch_table["HakkaCompare"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_int32),
]

dispatch_table["HakkaHash"].restype = HakkaJsonResultEnum
dispatch_table["HakkaHash"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint64),
]

dispatch_table["HakkaDumpSize"].restype = HakkaJsonResultEnum
dispatch_table["HakkaDumpSize"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint64),
]

dispatch_table["HakkaReclaim"].restype = HakkaJsonResultEnum
dispatch_table["HakkaReclaim"].argtypes = [
    CHakkaHandle,
]

# Primitive.h Primitive int, float, null, invalid functions
dispatch_table["CreateHakkaInt"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaInt"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
    ctypes.c_int64,
]

dispatch_table["CreateHakkaFloat"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaFloat"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
    ctypes.c_double,
]

dispatch_table["CreateHakkaNull"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaNull"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["CreateHakkaBool"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaBool"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
    ctypes.c_uint8,
]

dispatch_table["CreateHakkaInvalid"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaInvalid"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaInt"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaInt"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_int64),
]

dispatch_table["GetHakkaFloat"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaFloat"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_double),
]

dispatch_table["GetHakkaBool"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaBool"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

# Primitive.h string functions
dispatch_table["CreateHakkaString"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaString"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
]

dispatch_table["GetHakkaString"] = _lib.GetHakkaString
dispatch_table["GetHakkaString"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaString"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["GetHakkaStringLength"] = _lib.GetHakkaStringLength
dispatch_table["GetHakkaStringLength"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringLength"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["GetHakkaStringCapitalize"] = _lib.GetHakkaStringCapitalize
dispatch_table["GetHakkaStringCapitalize"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringCapitalize"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringCasefold"] = _lib.GetHakkaStringCasefold
dispatch_table["GetHakkaStringCasefold"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringCasefold"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringCount"] = _lib.GetHakkaStringCount
dispatch_table["GetHakkaStringCount"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringCount"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_int64),
]

dispatch_table["GetHakkaStringEndswith"] = _lib.GetHakkaStringEndswith
dispatch_table["GetHakkaStringEndswith"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringEndswith"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringFind"] = _lib.GetHakkaStringFind
dispatch_table["GetHakkaStringFind"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringFind"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_int64),
]

dispatch_table["GetHakkaStringConcatenate"] = _lib.GetHakkaStringConcatenate
dispatch_table["GetHakkaStringConcatenate"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringConcatenate"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringMultiply"] = _lib.GetHakkaStringMultiply
dispatch_table["GetHakkaStringMultiply"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringMultiply"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringSlice"] = _lib.GetHakkaStringSlice
dispatch_table["GetHakkaStringSlice"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringSlice"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringLower"] = _lib.GetHakkaStringLower
dispatch_table["GetHakkaStringLower"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringLower"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringRemoveprefix"] = _lib.GetHakkaStringRemoveprefix
dispatch_table["GetHakkaStringRemoveprefix"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringRemoveprefix"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringRemovesuffix"] = _lib.GetHakkaStringRemovesuffix
dispatch_table["GetHakkaStringRemovesuffix"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringRemovesuffix"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringReplace"] = _lib.GetHakkaStringReplace
dispatch_table["GetHakkaStringReplace"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringReplace"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringRfind"] = _lib.GetHakkaStringRfind
dispatch_table["GetHakkaStringRfind"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringRfind"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_int64),
]

dispatch_table["GetHakkaStringRsplit"] = _lib.GetHakkaStringRsplit
dispatch_table["GetHakkaStringRsplit"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringRsplit"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringSplit"] = _lib.GetHakkaStringSplit
dispatch_table["GetHakkaStringSplit"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringSplit"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringSplitlines"] = _lib.GetHakkaStringSplitlines
dispatch_table["GetHakkaStringSplitlines"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringSplitlines"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint8,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringStartswith"] = _lib.GetHakkaStringStartswith
dispatch_table["GetHakkaStringStartswith"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringStartswith"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringUpper"] = _lib.GetHakkaStringUpper
dispatch_table["GetHakkaStringUpper"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringUpper"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringSwapcase"] = _lib.GetHakkaStringSwapcase
dispatch_table["GetHakkaStringSwapcase"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringSwapcase"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringTitle"] = _lib.GetHakkaStringTitle
dispatch_table["GetHakkaStringTitle"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringTitle"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringZfill"] = _lib.GetHakkaStringZfill
dispatch_table["GetHakkaStringZfill"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringZfill"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaStringUTF8Length"] = _lib.GetHakkaStringUTF8Length
dispatch_table["GetHakkaStringUTF8Length"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringUTF8Length"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint64),
]

# Primitive.h: String testing functions
dispatch_table["GetHakkaStringIsalnum"] = _lib.GetHakkaStringIsalnum
dispatch_table["GetHakkaStringIsalnum"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsalnum"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsalpha"] = _lib.GetHakkaStringIsalpha
dispatch_table["GetHakkaStringIsalpha"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsalpha"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsascii"] = _lib.GetHakkaStringIsascii
dispatch_table["GetHakkaStringIsascii"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsascii"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsdecimal"] = _lib.GetHakkaStringIsdecimal
dispatch_table["GetHakkaStringIsdecimal"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsdecimal"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsdigit"] = _lib.GetHakkaStringIsdigit
dispatch_table["GetHakkaStringIsdigit"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsdigit"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsidentifier"] = _lib.GetHakkaStringIsidentifier
dispatch_table["GetHakkaStringIsidentifier"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsidentifier"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIslower"] = _lib.GetHakkaStringIslower
dispatch_table["GetHakkaStringIslower"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIslower"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsnumeric"] = _lib.GetHakkaStringIsnumeric
dispatch_table["GetHakkaStringIsnumeric"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsnumeric"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsprintable"] = _lib.GetHakkaStringIsprintable
dispatch_table["GetHakkaStringIsprintable"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsprintable"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsspace"] = _lib.GetHakkaStringIsspace
dispatch_table["GetHakkaStringIsspace"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsspace"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIstitle"] = _lib.GetHakkaStringIstitle
dispatch_table["GetHakkaStringIstitle"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIstitle"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaStringIsupper"] = _lib.GetHakkaStringIsupper
dispatch_table["GetHakkaStringIsupper"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringIsupper"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
]

# Primitive.h: String iterator functions
dispatch_table["CreateHakkaStringBegin"] = _lib.CreateHakkaStringBegin
dispatch_table["CreateHakkaStringBegin"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaStringBegin"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaStringIter),
]

dispatch_table["MoveHakkaStringNext"] = _lib.MoveHakkaStringNext
dispatch_table["MoveHakkaStringNext"].restype = HakkaJsonResultEnum
dispatch_table["MoveHakkaStringNext"].argtypes = [
    CHakkaStringIter,
]

dispatch_table["GetHakkaStringDeref"] = _lib.GetHakkaStringDeref
dispatch_table["GetHakkaStringDeref"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaStringDeref"].argtypes = [
    CHakkaStringIter,
    ctypes.POINTER(ctypes.c_uint32),  # UTF-32 code point
]

dispatch_table["HakkaStringIterRelease"] = _lib.HakkaStringIterRelease
dispatch_table["HakkaStringIterRelease"].restype = None
dispatch_table["HakkaStringIterRelease"].argtypes = [
    ctypes.POINTER(CHakkaStringIter),
]

# Array.h: Creation and Destruction
dispatch_table["CreateHakkaArray"] = _lib.CreateHakkaArray
dispatch_table["CreateHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaArray"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["LoadsHakkaArray"] = _lib.LoadsHakkaArray
dispatch_table["LoadsHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["LoadsHakkaArray"].argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
    ctypes.c_uint32,
]

dispatch_table["DumpHakkaArray"] = _lib.DumpHakkaArray
dispatch_table["DumpHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["DumpHakkaArray"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint64),
]

# Array Manipulation
dispatch_table["GetHakkaArrayObject"] = _lib.GetHakkaArrayObject
dispatch_table["GetHakkaArrayObject"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaArrayObject"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["SetHakkaArray"] = _lib.SetHakkaArray
dispatch_table["SetHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaArray"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    CHakkaHandle,
]
dispatch_table["GetHakkaArraySlice"] = _lib.GetHakkaArraySlice
dispatch_table["GetHakkaArraySlice"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaArraySlice"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["SetHakkaArraySlice"] = _lib.SetHakkaArraySlice
dispatch_table["SetHakkaArraySlice"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaArraySlice"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
    ctypes.c_int64,
    ctypes.c_int64,
    CHakkaHandle,
]

dispatch_table["RemoveHakkaArrayIndex"] = _lib.RemoveHakkaArrayIndex
dispatch_table["RemoveHakkaArrayIndex"].restype = HakkaJsonResultEnum
dispatch_table["RemoveHakkaArrayIndex"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
]

dispatch_table["ClearHakkaArray"] = _lib.ClearHakkaArray
dispatch_table["ClearHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["ClearHakkaArray"].argtypes = [
    CHakkaHandle,
]

dispatch_table["InsertHakkaArray"] = _lib.InsertHakkaArray
dispatch_table["InsertHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["InsertHakkaArray"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    CHakkaHandle,
]

dispatch_table["MultiplyHakkaArray"] = _lib.MultiplyHakkaArray
dispatch_table["MultiplyHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["MultiplyHakkaArray"].argtypes = [
    CHakkaHandle,
    ctypes.c_int64,
]

dispatch_table["GetHakkaArraySize"] = _lib.GetHakkaArraySize
dispatch_table["GetHakkaArraySize"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaArraySize"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["CountHakkaArray"] = _lib.CountHakkaArray
dispatch_table["CountHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["CountHakkaArray"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["ExtendHakkaArrayArray"] = _lib.ExtendHakkaArrayArray
dispatch_table["ExtendHakkaArrayArray"].restype = HakkaJsonResultEnum
dispatch_table["ExtendHakkaArrayArray"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
]

dispatch_table["FindFirstHakkaArray"] = _lib.FindFirstHakkaArray
dispatch_table["FindFirstHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["FindFirstHakkaArray"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["PushBackHakkaArray"] = _lib.PushBackHakkaArray
dispatch_table["PushBackHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["PushBackHakkaArray"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
]

dispatch_table["PopHakkaArray"] = _lib.PopHakkaArray
dispatch_table["PopHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["PopHakkaArray"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["RemoveValueHakkaArray"] = _lib.RemoveValueHakkaArray
dispatch_table["RemoveValueHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["RemoveValueHakkaArray"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
]

dispatch_table["ReverseHakkaArray"] = _lib.ReverseHakkaArray
dispatch_table["ReverseHakkaArray"].restype = HakkaJsonResultEnum
dispatch_table["ReverseHakkaArray"].argtypes = [
    CHakkaHandle,
]

# Array.h: Iterator Functions
dispatch_table["CreateHakkaArrayIterBegin"] = _lib.CreateHakkaArrayIterBegin
dispatch_table["CreateHakkaArrayIterBegin"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaArrayIterBegin"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaArrayIter),
]

dispatch_table["CreateHakkaArrayIterRBegin"] = _lib.CreateHakkaArrayIterRBegin
dispatch_table["CreateHakkaArrayIterRBegin"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaArrayIterRBegin"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaArrayIter),
]

dispatch_table["MoveHakkaArrayIterNext"] = _lib.MoveHakkaArrayIterNext
dispatch_table["MoveHakkaArrayIterNext"].restype = HakkaJsonResultEnum
dispatch_table["MoveHakkaArrayIterNext"].argtypes = [
    CHakkaArrayIter,
]

dispatch_table["MoveHakkaArrayIterPrev"] = _lib.MoveHakkaArrayIterPrev
dispatch_table["MoveHakkaArrayIterPrev"].restype = HakkaJsonResultEnum
dispatch_table["MoveHakkaArrayIterPrev"].argtypes = [
    CHakkaArrayIter,
]

dispatch_table["GetHakkaArrayIterDeref"] = _lib.GetHakkaArrayIterDeref
dispatch_table["GetHakkaArrayIterDeref"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaArrayIterDeref"].argtypes = [
    CHakkaArrayIter,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["HakkaArrayIterRelease"] = _lib.HakkaArrayIterRelease
dispatch_table["HakkaArrayIterRelease"].restype = HakkaJsonResultEnum
dispatch_table["HakkaArrayIterRelease"].argtypes = [
    ctypes.POINTER(CHakkaArrayIter),
]

# Object.h: Creation and Destruction
dispatch_table["CreateHakkaObject"] = _lib.CreateHakkaObject
dispatch_table["CreateHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaObject"].argtypes = [
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["LoadsHakkaObject"] = _lib.LoadsHakkaObject
dispatch_table["LoadsHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["LoadsHakkaObject"].argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
    ctypes.c_uint32,
]

dispatch_table["DumpHakkaObject"] = _lib.DumpHakkaObject
dispatch_table["DumpHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["DumpHakkaObject"].argtypes = [
    CHakkaHandle,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint64),
]

# Object Manipulation
dispatch_table["SetHakkaObjectInt"] = _lib.SetHakkaObjectInt
dispatch_table["SetHakkaObjectInt"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaObjectInt"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.c_int64,
]

dispatch_table["SetHakkaObjectFloat"] = _lib.SetHakkaObjectFloat
dispatch_table["SetHakkaObjectFloat"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaObjectFloat"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.c_double,
]

dispatch_table["SetHakkaObjectString"] = _lib.SetHakkaObjectString
dispatch_table["SetHakkaObjectString"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaObjectString"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
]

dispatch_table["SetHakkaObjectNull"] = _lib.SetHakkaObjectNull
dispatch_table["SetHakkaObjectNull"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaObjectNull"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
]

dispatch_table["GetHakkaObjectInt"] = _lib.GetHakkaObjectInt
dispatch_table["GetHakkaObjectInt"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectInt"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_int64),
]

dispatch_table["GetHakkaObjectFloat"] = _lib.GetHakkaObjectFloat
dispatch_table["GetHakkaObjectFloat"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectFloat"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_double),
]

dispatch_table["GetHakkaObjectString"] = _lib.GetHakkaObjectString
dispatch_table["GetHakkaObjectString"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectString"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["GetHakkaObjectNull"] = _lib.GetHakkaObjectNull
dispatch_table["GetHakkaObjectNull"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectNull"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_bool),
]

dispatch_table["GetHakkaObjectObject"] = _lib.GetHakkaObjectObject
dispatch_table["GetHakkaObjectObject"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectObject"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["SetHakkaObject"] = _lib.SetHakkaObject
dispatch_table["SetHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["SetHakkaObject"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    CHakkaHandle,
]

# Additional Object Methods
dispatch_table["RemoveHakkaObjectKey"] = _lib.RemoveHakkaObjectKey
dispatch_table["RemoveHakkaObjectKey"].restype = HakkaJsonResultEnum
dispatch_table["RemoveHakkaObjectKey"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
]

dispatch_table["GetHakkaObjectSize"] = _lib.GetHakkaObjectSize
dispatch_table["GetHakkaObjectSize"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectSize"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint32),
]

dispatch_table["ContainsHakkaObjectKey"] = _lib.ContainsHakkaObjectKey
dispatch_table["ContainsHakkaObjectKey"].restype = HakkaJsonResultEnum
dispatch_table["ContainsHakkaObjectKey"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint8),
]

dispatch_table["GetHakkaObjectKeys"] = _lib.GetHakkaObjectKeys
dispatch_table["GetHakkaObjectKeys"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectKeys"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["GetHakkaObjectValues"] = _lib.GetHakkaObjectValues
dispatch_table["GetHakkaObjectValues"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectValues"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["CreateHakkaObjectFromKeys"] = _lib.CreateHakkaObjectFromKeys
dispatch_table["CreateHakkaObjectFromKeys"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaObjectFromKeys"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["PopHakkaObject"] = _lib.PopHakkaObject
dispatch_table["PopHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["PopHakkaObject"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_uint32,
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["PopItemHakkaObject"] = _lib.PopItemHakkaObject
dispatch_table["PopItemHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["PopItemHakkaObject"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaHandle),
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["ClearHakkaObject"] = _lib.ClearHakkaObject
dispatch_table["ClearHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["ClearHakkaObject"].argtypes = [
    CHakkaHandle,
]

dispatch_table["UpdateHakkaObject"] = _lib.UpdateHakkaObject
dispatch_table["UpdateHakkaObject"].restype = HakkaJsonResultEnum
dispatch_table["UpdateHakkaObject"].argtypes = [
    CHakkaHandle,
    CHakkaHandle,
]

# Object Iterators
dispatch_table["CreateHakkaObjectIterBegin"] = _lib.CreateHakkaObjectIterBegin
dispatch_table["CreateHakkaObjectIterBegin"].restype = HakkaJsonResultEnum
dispatch_table["CreateHakkaObjectIterBegin"].argtypes = [
    CHakkaHandle,
    ctypes.POINTER(CHakkaObjectIter),
]

dispatch_table["MoveHakkaObjectIterNext"] = _lib.MoveHakkaObjectIterNext
dispatch_table["MoveHakkaObjectIterNext"].restype = HakkaJsonResultEnum
dispatch_table["MoveHakkaObjectIterNext"].argtypes = [
    CHakkaObjectIter,
]

dispatch_table["GetHakkaObjectIterDeref"] = _lib.GetHakkaObjectIterDeref
dispatch_table["GetHakkaObjectIterDeref"].restype = HakkaJsonResultEnum
dispatch_table["GetHakkaObjectIterDeref"].argtypes = [
    CHakkaObjectIter,
    ctypes.POINTER(CHakkaHandle),
    ctypes.POINTER(CHakkaHandle),
]

dispatch_table["HakkaObjectIterRelease"] = _lib.HakkaObjectIterRelease
dispatch_table["HakkaObjectIterRelease"].restype = HakkaJsonResultEnum
dispatch_table["HakkaObjectIterRelease"].argtypes = [
    ctypes.POINTER(CHakkaObjectIter),
]
