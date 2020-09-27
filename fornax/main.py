import os
import sys
from argparse import Namespace

from fornax.utils.repository import RepositoryFactory
from fornax.utils.argparser import DynamicArgumentParser


class Pipeline:
    def __init__(self, args: Namespace) -> None:
        """Initialize pipeline.

        :param args: pipeline args
        :type args: Namespace
        """
        self._args = args
        os.makedirs(self._args.workspace, exist_ok=True)
        self._repo = RepositoryFactory().create(
            self._args.repository_type,
            repository_address=self._args.repository,
            branch=self._args.branch,
            workspace=self._args.workspace,
        )

    def execute(self) -> None:
        """Execute pipeline."""
        self._repo.sync()


if __name__ == "__main__":
    parser = DynamicArgumentParser(description="Project build pipeline.")
    args = parser.parse_args(sys.argv[1:])
    pipeline = Pipeline(args)
    pipeline.execute()
