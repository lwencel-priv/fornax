from argparse import Namespace
from typing import Dict

from fornax.consts import StageType
from ..base_stage import BaseStage


class PrepareEnvironmentStage(BaseStage):
    def __init__(self, prev_stages_args: Dict[StageType, Namespace], args: Namespace):
        """Initialize sync stage.

        :param args: pipeline args
        :type args: Namespace
        :param prev_stages_args: pipeline args from previous stages
        :type prev_stages_args: Dict[StageType, Namespace]
        """
        super().__init__(prev_stages_args, args)

    def _run(self) -> None:
        """Run sync stage."""
        pass
