from abc import ABC

from fornax.executor import BashShellExecutor


class Repository(ABC):
    """Abstract repository class."""

    def __init__(self, repository_address: str, branch: str, workspace: str):
        """Initialize Git repository.

        :param repository_address: repository with git repo manifest
        :type repository_address: str
        :param branch: branch with git repo manifest
        :type branch: str
        :param workspace: directory where repositories will be stored
        :type workspace: str
        """
        self._executor = BashShellExecutor()
        self._repository_address = repository_address
        self._branch = branch
        self._workspace = workspace

    def sync(self) -> None:
        """Synchronize repositories."""
        raise NotImplementedError()
