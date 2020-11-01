import pickle
from typing import Any

from .abstract_processor import AbstractProcessor


class PickleProcessor(AbstractProcessor):
    def __init__(self) -> None:
        """Initialize pickle file processor."""
        super().__init__(pickle.load, self.__dump)
        self._read_mode = "rb"
        self._write_mode = "wb"

    def __dump(self, obj: Any, fp: Any) -> None:
        pickle.dump(obj, fp, protocol=pickle.HIGHEST_PROTOCOL)
