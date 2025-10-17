"""
This module is the entry point for the hakka_json package. It imports all the
public classes and functions that are available from the package. The classes
and functions are imported from the other modules in the package.
"""

__version__ = "1.0.0"

from ._hakka_json_base import HakkaJsonBase, HakkaJsonIteratorBase
from ._hakka_json_int import HakkaJsonInt
from ._hakka_json_float import HakkaJsonFloat
from ._hakka_json_bool import HakkaJsonBool
from ._hakka_json_null import HakkaJsonNull
from ._hakka_json_invalid import HakkaJsonInvalid
from ._hakka_json_string import HakkaJsonString, HakkaJsonStringIterator
from ._hakka_json_array import HakkaJsonArray, HakkaJsonArrayIterator
from ._hakka_json_object import HakkaJsonObject, HakkaJsonObjectIterator
from ._hakka_json import HakkaJson

__all__ = [
    "__version__",
    "HakkaJsonBase",
    "HakkaJsonIteratorBase",
    "HakkaJsonInt",
    "HakkaJsonFloat",
    "HakkaJsonBool",
    "HakkaJsonNull",
    "HakkaJsonInvalid",
    "HakkaJsonString",
    "HakkaJsonArray",
    "HakkaJsonObject",
    "HakkaJson",
    # iterators
    "HakkaJsonStringIterator",
    "HakkaJsonArrayIterator",
    "HakkaJsonObjectIterator",
]
