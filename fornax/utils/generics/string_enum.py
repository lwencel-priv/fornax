from enum import Enum


class StringEnum(Enum):
    """Argparser argument enum."""

    def __str__(self) -> str:
        """Cast to string.

        :return: obj element as string
        :rtype: str
        """
        return self.name.lower()

    @classmethod
    def from_string(cls, value: str) -> "StringEnum":
        """Create enum from a string.

        :raises ValueError: not supported enum value
        :return: StringEnum instance
        :rtype: StringEnum
        """
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError()
