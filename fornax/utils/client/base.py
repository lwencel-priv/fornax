from pathlib import Path
from fornax.executor.executor import Executor


class BaseClient:
    def __init__(self, executor: Executor) -> None:
        """Initialize JFrog client.

        :param executor: executor instance
        :type executor: Executor
        """
        self._executor = executor

    def download(self, source: str, destination: Path) -> None:
        """Download artifact.

        :param source: artifact source path e.g. https://artifacts.example.com/out_file.txt
        :type source: str
        :param destination: destination directory
        :type destination: Path
        """
        pass

    def upload(self, source: Path, destination: str, recursive: bool = False) -> None:
        """Upload artifact.

        :param source: artifact source path e.g. /home/user/example.log
        :type source: str
        :param destination: destination directory
        :type destination: Path
        """
        pass
