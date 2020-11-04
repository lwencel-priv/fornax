from abc import ABC, abstractmethod
from argparse import Namespace
from shutil import rmtree
from typing import Dict

from fornax.consts import StageType


class BaseStage(ABC):
    def __init__(self, prev_stages_args: Dict[StageType, Namespace], args: Namespace):
        """Initialize sync stage.

        :param args: pipeline args
        :type args: Namespace
        :param prev_stages_args: pipeline args from previous stages
        :type prev_stages_args: Dict[StageType, Namespace]
        """
        self._args = args
        self._prev_stages_args = prev_stages_args
        self._workspace = self._args.workspace.joinpath("stage", type(self).__name__)
        self._local_manifests_dir = self._args.workspace.joinpath("manifests")

    @abstractmethod
    def _run(self) -> None:
        """Run sync stage."""
        pass

    def _create_stage_workspace(self) -> None:
        """Create stage workspace."""
        self._workspace.mkdir(parents=True)

    def _remove_stage_workspace(self) -> None:
        """Remove stage workspace."""
        rmtree(self._workspace, ignore_errors=True)

    @property
    def args(self) -> Namespace:
        """Return stage args.

        :return: stage args
        :rtype: Namespace
        """
        return self._args

    def run(self) -> None:
        """Run sync stage."""
        self._remove_stage_workspace()
        self._create_stage_workspace()
        self._run()
        self._remove_stage_workspace()
