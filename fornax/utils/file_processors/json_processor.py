import json

from .abstract_processor import AbstractProcessor


class JsonProcessor(AbstractProcessor):
    def __init__(self) -> None:
        """Initialize json file processor."""
        super().__init__(json.load, json.dump)
