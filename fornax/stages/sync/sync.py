from argparse import Namespace
from typing import Dict
from shutil import rmtree

from fornax.utils.repository import RepositoryFactory
from fornax.consts import StageType
from ..base_stage import BaseStage


class SyncStage(BaseStage):
    def __init__(self, prev_stages_args: Dict[StageType, Namespace], args: Namespace):
        """Initialize sync stage.

        :param args: pipeline args
        :type args: Namespace
        :param prev_stages_args: pipeline args from previous stages
        :type prev_stages_args: Dict[StageType, Namespace]
        """
        super().__init__(prev_stages_args, args)
        rmtree(args.workspace, ignore_errors=True)
        args.workspace.mkdir(parents=True, exist_ok=True)
        args.repository_storage_path.mkdir(parents=True, exist_ok=True)
        self._repo = RepositoryFactory().create(
            self._args.manifest_type,
            source_path=self._args.source_path,
            source_path_type=self._args.source_path_type,
            branch=self._args.branch,
            repo_storage=self._args.repository_storage_path,
            workspace=self._workspace,
        )

    def _run(self) -> None:
        """Run sync stage."""
        self._repo.sync()
