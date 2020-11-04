from multiprocessing import cpu_count
from pathlib import Path

from fornax.consts import SourcePathType
from fornax.executor.command import Command
from fornax.utils.client import ClientFactory
from fornax.logger import main_logger
from .repository import Repository


class GitRepo(Repository):
    def sync(self) -> None:
        """Synchronize repositories."""
        if self._source_path_type is SourcePathType.REPOSITORY_ADDRESS:
            repo_init_command = ["repo", "init", "-u", self._source_path]
            if self._branch is not None:
                repo_init_command += ["-b", self._branch]
        else:
            manifest_path = self._download_manifest()
            repo_init_command = ["repo", "init", "-m", str(manifest_path)]

        main_logger.info("Starting repositories synchronization.")
        self._executor.run(Command(repo_init_command, cwd=self._repo_storage))
        self.reset()
        self.clean()
        self._executor.run(
            Command(["repo", "sync", "--force-sync", "-j", str(max(cpu_count() - 2, 1))], cwd=self._repo_storage)
        )
        main_logger.info("Repositories synchronization done.")

    def reset(self) -> None:
        """Reset changes.

        Hard reset files to HEAD.
        """
        self._executor.run(Command(["repo", "forall", "-c", "git reset --hard"], cwd=self._repo_storage))

    def clean(self) -> None:
        """Remove untracked files and directories from the working tree."""
        self._executor.run(Command(["repo", "forall", "-c", "git clean -dfx"], cwd=self._repo_storage))

    def _download_manifest(self) -> Path:
        manifest_path = self._local_manifests_storage.joinpath("manifest.xml")
        client = ClientFactory().create(self._source_path_type, executor=self._executor)
        client.download(self._source_path, manifest_path)
        return manifest_path
