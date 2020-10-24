from pathlib import Path
from argparse import ArgumentParser, Namespace
from typing import List, Dict, Any

from fornax.consts import Stage, ManifestType, SourcePathType


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
            type=Stage.from_string,  # type: ignore
            choices=list(Stage),
            help="stage name",
        )

    def _get_stage_parameters(self, stage: Stage) -> Dict[str, Any]:
        """Get stage specific parameters.

        :param stage: stage name
        :type stage: Stages
        :return: stage specific parameters
        :rtype: dict
        """
        default_workspace = str(Path.cwd().joinpath("fornax_data", "workspace"))
        default_repository_storage_path = str(Path.cwd().joinpath("fornax_data", "repositories"))
        parameters: Dict[str, Any] = {
            "--workspace": {
                "dest": "workspace",
                "default": default_workspace,
                "type": Path,
                "help": f"workspace path. Default: {default_workspace}",
            },
            "--repository_storage_path": {
                "dest": "repository_storage_path",
                "default": default_repository_storage_path,
                "type": Path,
                "help": f"directory where all repositories will be stored. Default: {default_repository_storage_path}",
            },
        }
        stage_specific_params: Dict[Stage, Dict[str, Any]] = {
            Stage.SYNC: {
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
            Stage.PREPARE_ENVIRONMENT: {},
            Stage.BUILD: {},
            Stage.TEST: {},
        }
        parameters.update(stage_specific_params.get(stage, {}))
        return parameters

    def parse_args(self, args: List[str]) -> Namespace:
        """Parser arguments.

        :param args: list of raw args
        :type args: List[str]
        :return: parsed args
        :rtype: Namespace
        """
        # Remove '-h' and '--help' at this step to prepare a final parser and then show help message.
        # Set is required to remove possible duplicates
        initial_args = set(args)
        if any("--stage" in arg for arg in initial_args):
            initial_args.discard("-h")
            initial_args.discard("--help")

        parsed_args, unknown_args = self._parser.parse_known_args(list(initial_args))
        stage_specific_parameters = self._get_stage_parameters(parsed_args.stage)
        for key, value in stage_specific_parameters.items():
            self._parser.add_argument(key, **value)

        return self._parser.parse_args(args)
