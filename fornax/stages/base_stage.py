from abc import ABC
from argparse import Namespace
from shutil import rmtree


class BaseStage(ABC):
    def __init__(self, args: Namespace):
        """Initialize sync stage.

        :param args: pipeline args
        :type args: Namespace
        """
        self._args = args
        self._workspace = self._args.workspace.joinpath("stage", type(self).__name__)

    def _run(self) -> None:
        """Run sync stage."""
        raise NotImplementedError()

    def _create_stage_workspace(self) -> None:
        """Create stage workspace."""
        print(self._workspace)
        self._workspace.mkdir(parents=True)

    def _remove_stage_workspace(self) -> None:
        """Remove stage workspace."""
        rmtree(self._workspace, ignore_errors=True)

    def run(self) -> None:
        """Run sync stage."""
        self._remove_stage_workspace()
        self._create_stage_workspace()
        self._run()
        self._remove_stage_workspace()
