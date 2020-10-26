from multiprocessing import cpu_count

from fornax.executor.command import Command
from fornax.logger import main_logger
from .exceptions import SyncException
from .repository import Repository


class GitRepo(Repository):
    def sync(self) -> None:
        """Synchronize repositories."""
        repo_init_command = ["repo", "init", "-u", self._source_path]
        if self._branch is not None:
            repo_init_command += ["-b", self._branch]

        commands = [
            Command(repo_init_command, cwd=self._repo_storage),
            Command(["repo", "forall", "-c", "git reset --hard ; git clean -dfx"], cwd=self._repo_storage),
            Command(
                ["repo", "sync", "--force-sync", "-j", str(max(cpu_count() - 2, 1))],
                cwd=self._repo_storage,
            ),
        ]
        main_logger.info("Starting repositories synchronization.")
        for command in commands:
            process = self._executor.run(command)
            if process.return_code != 0:
                main_logger.error("Cannot sync repositories. ")
                raise SyncException()

        main_logger.info("Repositories synchronization done.")