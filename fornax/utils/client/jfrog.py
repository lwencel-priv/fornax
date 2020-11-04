from pathlib import Path

from fornax.executor import Executor
from fornax.executor.command import Command
from .base import BaseClient


class JFrog(BaseClient):
    def __init__(self, executor: Executor) -> None:
        """Initialize JFrog client.

        :param executor: executor instance
        :type executor: Executor
        """
        super().__init__(executor)

    def download(self, source: str, destination: Path) -> None:
        """Download artifact.

        :param source: artifact source path e.g. https://artifacts.example.com/out_file.txt
        :type source: str
        :param destination: destination directory
        :type destination: Path
        """
        self._executor.run(Command(["jfrog", "rt", "download", source, str(destination)]))

    def upload(self, source: Path, destination: str, recursive: bool = False) -> None:
        """Upload artifact.

        :param source: artifact source path e.g. /home/user/example.log
        :type source: str
        :param destination: destination directory
        :type destination: Path
        """
        cmd = ["jfrog", "rt", "upload", str(source), destination, f"--recursive={str(recursive).lower()}"]
        self._executor.run(Command(cmd))
