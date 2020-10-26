import sys
from argparse import Namespace

from fornax.argparser import DynamicArgumentParser
from fornax.stages import StageFactory


class Pipeline:
    def __init__(self, args: Namespace) -> None:
        """Initialize pipeline.

        :param args: pipeline args
        :type args: Namespace
        """
        self._args = args
        self._args.workspace.mkdir(parents=True, exist_ok=True)
        self._args.repository_storage_path.mkdir(parents=True, exist_ok=True)
        self._stage = StageFactory().create(self._args.stage, args=self._args)

    def execute(self) -> None:
        """Execute pipeline."""
        self._stage.run()


def main() -> None:
    """Entry point."""
    parser = DynamicArgumentParser(description="Project build pipeline.")
    args = parser.parse_args(sys.argv[1:])
    pipeline = Pipeline(args)
    pipeline.execute()


if __name__ == "__main__":
    main()
