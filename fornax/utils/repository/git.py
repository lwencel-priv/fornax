import re
import os

from fornax.executor.command import Command
from fornax.logger import main_logger
from .repository import Repository


class Git(Repository):
    def sync(self) -> None:
        """Synchronize repositories."""
        repository_name = re.match(r".*\/([^\/]+)\.git.*", self._repository_address)
        if repository_name is None:
            raise ValueError(f"Unable to get repository name from repository address: {repository_name}")

        repository_path = os.path.join(self._workspace, repository_name.group(1))
        commands = []
        if not os.path.exists(repository_path):
            repo_clone = ["git", "clone", self._repository_address]
            if self._branch is not None:
                repo_clone += ["-b", self._branch]

            commands.append(Command(repo_clone, cwd=self._workspace))
        else:
            commands.append(Command(["git", "reset", "--hard"], cwd=repository_path))
            commands.append(Command(["git", "clean", "-dfx"], cwd=repository_path))
            commands.append(Command(["git", "fetch"], cwd=repository_path))
            if self._branch is not None:
                commands.append(Command(["git", "checkout", "-b", self._branch], cwd=repository_path))
                commands.append(Command(["git", "pull"], cwd=repository_path))

        main_logger.info("Starting repositories synchronization.")
        for command in commands:
            self._executor.run(command)

        main_logger.info("Repositories synchronization done.")
