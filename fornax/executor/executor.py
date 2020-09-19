from abc import ABC

from .command import Command
from .process import Process


class Executor(ABC):

    def run(self, command: Command) -> Process:
        raise NotImplementedError("run method not implemented.")
