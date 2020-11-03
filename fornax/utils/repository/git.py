import re
from pathlib import Path
from typing import Optional

from fornax.executor import BashShellExecutor
from fornax.consts import SourcePathType
from fornax.executor.command import Command
from fornax.logger import main_logger
from .repository import Repository


class Git(Repository):
    def __init__(
        self,
        source_path: str,
        source_path_type: SourcePathType,
        branch: str,
        repo_storage: Path,
        workspace: Path,
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

        repository_name_match = re.match(r".*\/([^\/]+)\.git.*", self._source_path)
        if repository_name_match is None:
            raise ValueError(f"Unable to get repository name from repository address: {repository_name_match}")

        self._repository_path = self._repo_storage.joinpath(repository_name_match.group(1))

    @classmethod
    def init_from_path(cls, workspace: Path, repo_storage: Path, project: str) -> "Git":
        """Initialize repository from path.

        :param workspace: directory where logs are stored
        :type workspace: Path
        :param repo_storage: directory where repositories will be stored
        :type repo_storage: Path
        :param project: project name
        :type project: str
        """
        remote = cls._get_remote(repo_storage.joinpath(project), workspace)
        return cls(remote, SourcePathType.REPOSITORY_ADDRESS, "master", repo_storage, workspace)

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

    def checkout(self, refs: Optional[str] = None, branch: Optional[str] = None, commit: Optional[str] = None) -> None:
        """Checkout to specific revision.

        :param refs: refs, defaults to None
        :type refs: Optional[str], optional
        :param branch: branch name, defaults to None
        :type branch: Optional[str], optional
        :param commit: commit sha, defaults to None
        :type commit: Optional[str], optional
        :raises ValueError: Not supported option
        """
        if refs is not None:
            self._executor.run(Command(["git", "fetch", self._source_path, refs], cwd=self._repository_path))
            self._executor.run(Command(["git", "checkout", "FETCH_HEAD"], cwd=self._repository_path))
        elif branch is not None:
            self._executor.run(Command(["git", "checkout", branch], cwd=self._repository_path))
        elif commit is not None:
            self._executor.run(Command(["git", "checkout", commit], cwd=self._repository_path))
        else:
            raise ValueError("Not supported option.")

    def pull(self) -> None:
        """Pull changes."""
        self._executor.run(Command(["git", "pull"], cwd=self._repository_path))

    def _update(self) -> None:
        """Pull changes."""
        self.reset()
        self.clean()
        self.fetch()
        self.checkout(branch=self._branch)
        self.pull()

    @staticmethod
    def _get_remote(repository_path: Path, workspace: Path) -> str:
        """Return repository remote address.

        :param repository_path: path to repository
        :type repository_path: Path
        :return: repository remote address
        :rtype: str
        """
        executor = BashShellExecutor(workspace)
        process = executor.run(Command(["git", "remote", "-v"], cwd=repository_path))
        remote = next(process.stdout).strip()  # type: ignore
        remote_match = re.match(r"(^.*?)\s+(.*?)\s+", remote)
        if remote_match is None:
            raise ValueError("Remote not found.")

        return str(remote_match.group(2))
