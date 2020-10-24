from fornax.utils.generics.factory import GenericFactory
from fornax.consts import Stage
from .base_stage import BaseStage
from .sync import SyncStage
from .prepare_environment import PrepareEnvironmentStage


class StageFactory(GenericFactory[Stage, BaseStage]):
    """Stage factory class."""

    def __init__(self) -> None:
        """Initailize stage factory."""
        super().__init__(prototype_class=BaseStage)
        self.add_builder(Stage.SYNC, SyncStage)
        self.add_builder(Stage.PREPARE_ENVIRONMENT, PrepareEnvironmentStage)
