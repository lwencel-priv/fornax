import sys
from argparse import Namespace

from fornax.argparser import DynamicArgumentParser
from fornax.stages import StageStateMachine


class Pipeline:
    def __init__(self, args: Namespace) -> None:
        """Initialize pipeline.

        :param args: pipeline args
        :type args: Namespace
        """
        self._stage_state = StageStateMachine(args.workspace)
        self._stage_state.next_stage(args)

    def execute(self) -> None:
        """Execute pipeline."""
        self._stage_state.run()


def main() -> None:
    """Entry point."""
    parser = DynamicArgumentParser(description="Project build pipeline.")
    args = parser.parse_args(sys.argv[1:])
    pipeline = Pipeline(args)
    pipeline.execute()


if __name__ == "__main__":
    main()
