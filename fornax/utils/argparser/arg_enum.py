from enum import Enum


class ArgEnum(Enum):
    """Argparser argument enum."""

    def __str__(self) -> str:
        """Cast to string.

        :return: obj element as string
        :rtype: str
        """
        return self.name.lower()

    @classmethod
    def from_string(cls, value: str) -> "ArgEnum":
        """Create enum from a string.

        :raises ValueError: not supported enum value
        :return: ArgEnum instance
        :rtype: ArgEnum
        """
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError()
