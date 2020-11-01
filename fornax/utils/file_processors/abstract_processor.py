from typing import Callable
from pathlib import Path


class AbstractProcessor:
    def __init__(self, decoder: Callable[..., dict], encoder: Callable[..., None]):
        """Initialize file processor.

        :param decoder: decoder function
        :type decoder: Callable[[Union[str, bytes, bytearray]], dict]
        :param encoder: encoder function
        :type encoder: Callable[[Union[dict,list]], None]
        """
        self.__decoder = decoder
        self.__encoder = encoder
        self._read_mode = "r"
        self._write_mode = "w"

    def read(self, path: Path) -> dict:
        """Decode file.

        :param path: path to file
        :type path: Path
        :return: data
        :rtype: dict
        """
        with open(path, self._read_mode) as stream:
            data = self.__decoder(stream)

        return data

    def write(self, path: Path, data: dict) -> None:
        """Encode data.

        :param path: path to file
        :type path: Path
        :param data: data to save
        :type data: dict
        """
        with open(path, self._write_mode) as stream:
            self.__encoder(data, stream)
