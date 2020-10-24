import re
from pathlib import Path

from fornax.consts import SourcePathType
from fornax.executor.command import Command
from fornax.logger import main_logger
from .repository import Repository


class Git(Repository):
    def __init__(
        self, source_path: str, source_path_type: SourcePathType, branch: str, repo_storage: Path, workspace: Path
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
        """
        super().__init__(source_path, source_path_type, branch, repo_storage, workspace)
        if self._source_path_type is not SourcePathType.REPOSITORY_ADDRESS:
            raise ValueError("Git class does not support 'SourcePathType' different than REPOSITORY_ADDRESS.")

        repository_name = re.match(r".*\/([^\/]+)\.git.*", self._source_path)
        if repository_name is None:
            raise ValueError(f"Unable to get repository name from repository address: {repository_name}")

        self._repository_path = self._repo_storage.joinpath(repository_name.group(1))

    def sync(self) -> None:
        """Synchronize repositories."""
        main_logger.info("Starting repositories synchronization.")
        if self._repository_path.exists():
            self._update()
        else:
            self.clone()

        main_logger.info("Repositories synchronization done.")

    def clone(self) -> None:
        """Clone repository."""
        repo_clone = ["git", "clone", self._source_path]
        if self._branch is not None:
            repo_clone += ["-b", self._branch]

        self._executor.run(Command(repo_clone, cwd=self._repo_storage))

    def reset(self) -> None:
        """Reset changes.

        Hard reset files to HEAD.
        """
        self._executor.run(Command(["git", "reset", "--hard"], cwd=self._repository_path))

    def clean(self) -> None:
        """Remove untracked files and directories from the working tree."""
        self._executor.run(Command(["git", "clean", "-dfx"], cwd=self._repository_path))

    def fetch(self) -> None:
        """Fetch changes."""
        self._executor.run(Command(["git", "fetch"], cwd=self._repository_path))

    def checkout(self, branch: str) -> None:
        """Checkout to specific branch."""
        self._executor.run(Command(["git", "checkout", self._branch], cwd=self._repository_path))

    def pull(self) -> None:
        """Pull changes."""
        self._executor.run(Command(["git", "pull"], cwd=self._repository_path))

    def _update(self) -> None:
        """Pull changes."""
        self.reset()
        self.clean()
        self.fetch()
        if self._branch is not None:
            if self._branch in self._executor.run(Command(["git", "branch"], cwd=self._repository_path)).stdout:
                self.checkout(self._branch)

            self.pull()
