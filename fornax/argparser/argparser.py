from pathlib import Path
from argparse import ArgumentParser, Namespace
from typing import List, Dict, Any

from fornax.consts import StageType, ManifestType, SourcePathType


class DynamicArgumentParser:
    def __init__(self, description: str) -> None:
        """Initialize dynamic argparser.

        :param description: argparser description
        :type description: str
        """
        self._parser = ArgumentParser(description=description)
        self._parser.add_argument(
            "--stage",
            dest="stage",
            required=True,
            type=StageType.from_string,  # type: ignore
            choices=list(StageType),
            help="stage name",
        )
        default_workspace = str(Path.cwd().joinpath("fornax_data", "workspace"))
        self._parser.add_argument(
            "--workspace",
            dest="workspace",
            default=default_workspace,
            type=Path,
            help=f"workspace path. Default: {default_workspace}",
        )

    def _get_stage_parameters(self, stage: StageType) -> Dict[str, Any]:
        """Get stage specific parameters.

        :param stage: stage name
        :type stage: Stages
        :return: stage specific parameters
        :rtype: dict
        """
        default_repository_storage_path = str(Path.cwd().joinpath("fornax_data", "repositories"))
        stage_specific_params: Dict[StageType, Dict[str, Any]] = {
            StageType.SYNC: {
                "--repository_storage_path": {
                    "dest": "repository_storage_path",
                    "default": default_repository_storage_path,
                    "type": Path,
                    "help": f"workspace path. Default: {default_repository_storage_path}",
                },
                "--source_path": {
                    "dest": "source_path",
                    "required": True,
                    "help": "source path e.g. repository with manifest or git repository",
                },
                "--source_path_type": {
                    "dest": "source_path_type",
                    "required": False,
                    "default": SourcePathType.REPOSITORY_ADDRESS,
                    "type": SourcePathType.from_string,
                    "choices": list(SourcePathType),
                    "help": "type of source path",
                },
                "--manifest_type": {
                    "dest": "manifest_type",
                    "required": False,
                    "default": ManifestType.NONE,
                    "type": ManifestType.from_string,
                    "choices": list(ManifestType),
                    "help": "manifest type used to prepare sources and environment",
                },
                "--branch": {
                    "dest": "branch",
                    "required": False,
                    "default": "master",
                    "help": "used only if source_path_type is 'repository_address'.",
                },
            },
            StageType.CHECKOUT: {
                "--project": {
                    "dest": "project",
                    "required": True,
                    "help": "Project name",
                },
                "--refs": {
                    "dest": "refs",
                    "required": False,
                    "help": "Refs to checkout",
                },
                "--branch": {
                    "dest": "branch",
                    "required": False,
                    "help": "Branch to checkout",
                },
                "--commit": {
                    "dest": "commit",
                    "required": False,
                    "help": "Commit to checkout",
                },
            },
            StageType.PREPARE_ENVIRONMENT: {},
            StageType.BUILD: {},
            StageType.TEST: {},
        }
        return stage_specific_params.get(stage, {})

    def parse_args(self, raw_args: List[str]) -> Namespace:
        """Parser arguments.

        :param args: list of raw args
        :type args: List[str]
        :return: parsed args
        :rtype: Namespace
        """
        # Remove '-h' and '--help' at this step to prepare a final parser and then show help message.
        # Set is required to remove possible duplicates
        initial_args = set(raw_args)
        if any("--stage" in arg for arg in initial_args):
            initial_args.discard("-h")
            initial_args.discard("--help")

        parsed_args, unknown_args = self._parser.parse_known_args(list(initial_args))
        stage_specific_parameters = self._get_stage_parameters(parsed_args.stage)
        for key, value in stage_specific_parameters.items():
            self._parser.add_argument(key, **value)

        args = self._parser.parse_args(raw_args)
        return args
