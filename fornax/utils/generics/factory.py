from typing import Dict, Any, Generic, TypeVar, Optional, Type


OBJECT_TYPE = TypeVar("OBJECT_TYPE")
KEY_TYPE = TypeVar("KEY_TYPE")


class GenericFactory(Generic[KEY_TYPE, OBJECT_TYPE]):
    """Generic factory implementation."""

    def __init__(self, prototype_class: Optional[Type[OBJECT_TYPE]] = None) -> None:
        """Initialize factory.

        :param prototype_class: prototype class, defaults to None
        :type prototype_class: Optional[OBJECT_TYPE], optional
        """
        self.__prototype_class = prototype_class
        self.__builders: Dict[KEY_TYPE, Type[OBJECT_TYPE]] = {}

    def add_builder(self, name: KEY_TYPE, builder: Type[OBJECT_TYPE]) -> None:
        """Add new builder.

        :param name: builder name
        :type name: str
        :param builder: builder class
        :type builder: OBJECT_TYPE
        :raises TypeError: if builder is not a subclass of prototype class when prototype class defined
        """
        if self.__prototype_class is not None and not issubclass(builder, self.__prototype_class):
            raise TypeError(f"{builder} is not a subclass of {self.__prototype_class}")

        self.__builders[name] = builder

    def create(self, name: KEY_TYPE, **kwargs: Any) -> OBJECT_TYPE:
        """Create class instance.

        :param name: builder name
        :type name: str
        :raises ValueError: when unknown builder name specified
        :return: class instance
        :rtype: OBJECT_TYPE
        """
        builder: Optional[Type[OBJECT_TYPE]] = self.__builders.get(name, None)
        if not builder:
            raise ValueError(f"Unknown builder {name}")

        return builder(**kwargs)  # type: ignore
