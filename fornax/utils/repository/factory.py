from fornax.utils.generics.factory import GenericFactory
from fornax.utils.argparser import SupportedRepositories
from .repository import Repository
from .git import Git
from .git_repo import GitRepo


class RepositoryFactory(GenericFactory[SupportedRepositories, Repository]):
    """Repository factory class."""

    def __init__(self) -> None:
        """Initailize repository factory."""
        super().__init__(prototype_class=Repository)
        self.add_builder(SupportedRepositories.GIT, Git)
        self.add_builder(SupportedRepositories.GIT_REPO, GitRepo)
