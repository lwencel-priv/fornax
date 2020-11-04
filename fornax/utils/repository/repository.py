from abc import ABC
from pathlib import Path

from fornax.consts import SourcePathType
from fornax.executor import BashShellExecutor


class Repository(ABC):
    """Abstract repository class."""

    def __init__(
        self,
        source_path: str,
        source_path_type: SourcePathType,
        branch: str,
        repo_storage: Path,
        workspace: Path,
        local_manifests_storage: Path,
    ):
        """Initialize Git repository.

        :param source_path: repository with git repo manifest
        :type source_path: str
        :param source_path_type: repository with git repo manifest
        :type source_path_type: SourcePathType
        :param branch: branch with git repo manifest
        :type branch: str
        :param repo_storage: directory where repositories will be stored
        :type repo_storage: Path
        :param workspace: directory where logs are stored
        :type workspace: Path
        :param local_manifests_storage: local storage for manifests files
        :type local_manifests_storage: Path
        """
        self._source_path = source_path
        self._source_path_type = source_path_type
        self._branch = branch
        self._repo_storage = repo_storage
        self._workspace = workspace
        self._local_manifests_storage = local_manifests_storage
        self._executor = BashShellExecutor(self._workspace)

    def sync(self) -> None:
        """Synchronize repositories."""
        raise NotImplementedError()
