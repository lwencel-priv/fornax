from fornax.utils.generics.factory import GenericFactory
from fornax.consts import SourcePathType
from .base import BaseClient
from .jfrog import JFrog


class ClientFactory(GenericFactory[SourcePathType, BaseClient]):
    """Repository factory class."""

    def __init__(self) -> None:
        """Initailize repository factory."""
        super().__init__(prototype_class=BaseClient)
        self.add_builder(SourcePathType.ARTIFACTORY, BaseClient)
        self.add_builder(SourcePathType.ARTIFACTORY, JFrog)
