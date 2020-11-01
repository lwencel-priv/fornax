from fornax.utils.generics.factory import GenericFactory
from fornax.consts import ManifestType
from .repository import Repository
from .git import Git
from .git_repo import GitRepo


class RepositoryFactory(GenericFactory[ManifestType, Repository]):
    """Repository factory class."""

    def __init__(self) -> None:
        """Initailize repository factory."""
        super().__init__(prototype_class=Repository)
        self.add_builder(ManifestType.NONE, Git)
        self.add_builder(ManifestType.GIT_REPO, GitRepo)
