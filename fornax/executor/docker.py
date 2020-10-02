from .command import Command
from .process import Process
from .executor import Executor


class DockerExecutor(Executor):
    def run(self, command: Command) -> Process:
        """Run command inside docker container.

        :param command: command to run
        :type command: Command
        :return: process instance
        :rtype: Process
        """
        return Process(command)
