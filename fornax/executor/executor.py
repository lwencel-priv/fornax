from abc import ABC, abstractmethod
from pathlib import Path

from .command import Command
from .process import Process


class Executor(ABC):
    """Generic executor."""

    def __init__(self, workspace: Path) -> None:
        """Initialize docker executor.

        :param workspace: workspace dedicated output files e.g. logs
        :type workspace: Path
        """
        self._workspace = workspace

    @abstractmethod
    def run(self, command: Command) -> Process:
        """Run command.

        :param command: command to run
        :type command: Command
        :return: process instance
        :rtype: Process
        """
        raise NotImplementedError("run method not implemented.")
