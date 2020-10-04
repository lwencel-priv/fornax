from fornax.utils.generics.factory import GenericFactory
from fornax.utils.argparser.consts import Environment
from .executor import Executor
from .bash_shell import BashShellExecutor
from .docker import DockerExecutor


class ExecutorFactory(GenericFactory[Environment, Executor]):
    def __init__(self) -> None:
        """Initailize executor factory."""
        super().__init__(prototype_class=Executor)
        self.add_builder(Environment.BARE, BashShellExecutor)
        self.add_builder(Environment.DOCKER, DockerExecutor)
