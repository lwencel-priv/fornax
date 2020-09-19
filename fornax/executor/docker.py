from abc import ABC

from .command import Command
from .process import Process
from .executor import Executor


class DockerExecutor(Executor):
    
    def run(self, command: Command) -> Process:
        return Process(command)
