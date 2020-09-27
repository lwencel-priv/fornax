from argparse import ArgumentParser, Namespace
from typing import List, Dict, Any

from .consts import Stages, SupportedRepositories


class DynamicArgumentParser:
    def __init__(self, description: str) -> None:
        """Initialize dynamic argparser.

        :param description: argparser description
        :type description: str
        """
        self._parser = ArgumentParser(description=description)
        self._parser.add_argument("--workspace", dest="workspace", required=True, help="workspace path")
        self._parser.add_argument(
            "--stage",
            dest="stage",
            required=True,
            type=Stages.from_string,  # type: ignore
            choices=list(Stages),
            help="stage name",
        )

    def _get_stage_parameters(self, stage: Stages) -> Dict[str, Any]:
        """Get stage specific parameters.

        :param stage: stage name
        :type stage: Stages
        :return: stage specific parameters
        :rtype: dict
        """
        stage_specific_params: Dict[Stages, Dict[str, Any]] = {
            Stages.SYNC_REPOSITORIES: {
                "--repository": {"dest": "repository", "required": True, "help": ""},
                "--repository_type": {
                    "dest": "repository_type",
                    "required": False,
                    "default": SupportedRepositories.GIT_REPO,
                    "type": SupportedRepositories.from_string,
                    "choices": list(SupportedRepositories),
                    "help": "",
                },
                "--branch": {
                    "dest": "branch",
                    "required": False,
                    "default": None,
                    "help": "",
                },
            },
            Stages.PREPARE_ENVIRONMENT: {},
            Stages.BUILD: {},
            Stages.TEST: {},
        }
        return stage_specific_params.get(stage, {})

    def parse_args(self, args: List[str]) -> Namespace:
        """Parser arguments.

        :param args: list of raw args
        :type args: List[str]
        :return: parsed args
        :rtype: Namespace
        """
        parsed_args, unknown_args = self._parser.parse_known_args(args)
        stage_specific_parameters = self._get_stage_parameters(parsed_args.stage)
        for key, value in stage_specific_parameters.items():
            self._parser.add_argument(key, **value)

        return self._parser.parse_args(args)
