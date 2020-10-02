from abc import ABC

from .command import Command
from .process import Process


class Executor(ABC):
    """Generic executor."""

    def run(self, command: Command) -> Process:
        """Run command.

        :param command: command to run
        :type command: Command
        :return: process instance
        :rtype: Process
        """
        raise NotImplementedError("run method not implemented.")
