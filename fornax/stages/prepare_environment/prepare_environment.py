from argparse import Namespace

from ..base_stage import BaseStage


class PrepareEnvironmentStage(BaseStage):
    def __init__(self, args: Namespace):
        """Initialize prepare environment stage.

        :param args: pipeline args
        :type args: Namespace
        """
        super().__init__(args)

    def _run(self) -> None:
        """Run sync stage."""
        pass
