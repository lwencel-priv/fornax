from argparse import Namespace
from typing import Dict

from fornax.consts import StageType
from fornax.utils.repository.git import Git
from ..base_stage import BaseStage


class CheckoutStage(BaseStage):
    def __init__(self, prev_stages_args: Dict[StageType, Namespace], args: Namespace):
        """Initialize checkout stage.

        :param args: pipeline args
        :type args: Namespace
        :param prev_stages_args: pipeline args from previous stages
        :type prev_stages_args: Dict[StageType, Namespace]
        """
        super().__init__(prev_stages_args, args)
        sync_args = self._prev_stages_args[StageType.SYNC]
        self._repo = Git.init_from_path(
            project=self._args.project,
            repo_storage=sync_args.repository_storage_path,
            workspace=self._workspace,
            local_manifests_storage=self._local_manifests_dir,
        )

    def _run(self) -> None:
        """Run checkout stage."""
        self._repo.checkout(
            refs=self._args.refs,
            branch=self._args.branch,
            commit=self._args.commit,
        )
