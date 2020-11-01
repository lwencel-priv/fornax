from abc import ABC

from fornax.executor.executor import Executor


class BaseClient(ABC):
    def __init__(self, executor: Executor) -> None:
        """Initialize JFrog client.

        :param executor: executor instance
        :type executor: Executor
        """
        self._executor = executor
