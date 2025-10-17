"""
HakkaJson Type Interface.
Provides serialization and deserialization methods for HakkaJson types.
"""

from typing import IO
from ._hakka_json_base import HakkaJsonBase
from ._hakka_json_array import HakkaJsonArray
from ._hakka_json_object import HakkaJsonObject


class HakkaJson:
    """
    General interface for serializing and deserializing HakkaJson types.
    Supports the following methods:
        - dump: Serialize a HakkaJsonBase object to a file.
        - dumps: Serialize a HakkaJsonBase object to a JSON string.
        - load: Deserialize a JSON string from a file into a HakkaJsonBase object.
        - loads: Deserialize a JSON string into a HakkaJsonBase object.
    """

    @staticmethod
    def dump(obj: HakkaJsonBase, file: IO, max_depth: int = 512):
        """
        Serialize a HakkaJsonBase object and write it to a file.

        Args:
            obj (HakkaJsonBase): The object to serialize.
            file (IO): A writable file-like object.
            max_depth (int, optional): Maximum recursion depth for serialization.

        Raises:
            TypeError: If obj is not an instance of HakkaJsonBase.
            RuntimeError: If serialization fails.
        """
        if not issubclass(type(obj), HakkaJsonBase):
            raise TypeError("obj must be an instance of HakkaJsonBase")
        return file.write(obj.dumps(max_depth))

    @staticmethod
    def dumps(obj: HakkaJsonBase, max_depth: int = 512) -> str:
        """
        Serialize a HakkaJsonBase object to a JSON string.

        Args:
            obj (HakkaJsonBase): The object to serialize.
            max_depth (int, optional): Maximum recursion depth for serialization.

        Returns:
            str: The JSON string.

        Raises:
            TypeError: If obj is not an instance of HakkaJsonBase.
            RuntimeError: If serialization fails.
        """
        if not issubclass(type(obj), HakkaJsonBase):
            raise TypeError("obj must be an instance of HakkaJsonBase")
        return obj.dumps(max_depth)

    @staticmethod
    def load(file: IO, max_depth: int = 512) -> HakkaJsonBase:
        """
        Deserialize a HakkaJsonBase object from a file.

        Args:
            file (IO): A readable file-like object.

        Returns:
            HakkaJsonBase: The deserialized object.

        Raises:
            RuntimeError: If deserialization fails.
        """
        # io to string and pass to HakkaJsonArray
        string = file.read()
        if string == "":
            raise ValueError("file must not be empty")
        # breakpoint()
        return (
            HakkaJsonArray.loads(string, max_depth)
            if string[0] == "["
            else HakkaJsonObject.loads(string, max_depth)
        )

    @staticmethod
    def loads(string: str, max_depth: int = 512) -> HakkaJsonBase:
        """
        Deserialize a HakkaJsonBase object from a JSON string.

        Args:
            string (str): The JSON string.

        Returns:
            HakkaJsonBase: The deserialized object.

        Raises:
            RuntimeError: If deserialization fails.
        """
        if string == "":
            raise ValueError("string must not be empty")
        return (
            HakkaJsonArray.loads(string, max_depth)
            if string[0] == "["
            else HakkaJsonObject.loads(
                string,
                max_depth,
            )
        )
