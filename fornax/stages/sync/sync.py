from argparse import Namespace

from ..base_stage import BaseStage
from .repository import RepositoryFactory


class SyncStage(BaseStage):
    def __init__(self, args: Namespace):
        """Initialize sync stage.

        :param args: pipeline args
        :type args: Namespace
        """
        super().__init__(args)
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
