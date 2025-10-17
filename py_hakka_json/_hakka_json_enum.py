"""Enum for JSON data."""

from enum import IntEnum

# Refer to py_hakka_json/_core/src/hakka_json/include/hakka_json_enum.h

__all__ = [
    "HakkaJsonResultEnum",
    "HakkaJsonTypeEnum",
]


class HakkaJsonResultEnum(IntEnum):
    """Enum for JSON result."""

    HAKKA_JSON_SUCCESS = 0
    HAKKA_JSON_PARSE_ERROR = 1
    HAKKA_JSON_TYPE_ERROR = 2
    HAKKA_JSON_NOT_ENOUGH_MEMORY = 3
    HAKKA_JSON_KEY_NOT_FOUND = 4
    HAKKA_JSON_INDEX_OUT_OF_BOUNDS = 5
    HAKKA_JSON_INVALID_ARGUMENT = 6
    HAKKA_JSON_OVERFLOW = 7
    HAKKA_JSON_RECURSION_DEPTH_EXCEEDED = 8
    HAKKA_JSON_ITERATOR_END = 9
    HAKKA_JSON_INTERNAL_ERROR = -1


class HakkaJsonTypeEnum(IntEnum):
    """Enum for JSON type."""

    HAKKA_JSON_NULL = 0
    HAKKA_JSON_STRING = 1
    HAKKA_JSON_INT = 2
    HAKKA_JSON_FLOAT = 3
    HAKKA_JSON_BOOL = 4
    HAKKA_JSON_OBJECT = 5
    HAKKA_JSON_ARRAY = 6
    HAKKA_JSON_INVALID = -1
