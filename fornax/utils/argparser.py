# MIT License

# Copyright (c) 2020 lwencel-priv

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from argparse import ArgumentParser, Namespace
from typing import Optional, List

from fornax.consts import Stages


class DynamicArgumentParser:

    def __init__(self, description: str) -> None:
        self._parser = ArgumentParser(description=description)
        self._parser.add_argument('--workspace', dest='workspace', required=True, help='workspace')
        self._parser.add_argument('--stage', dest='stage', help='')

    def _get_stage_parameters(self, stage: Stages) -> dict:
        stage_specific_params = {
            Stages.SYNC_REPOSITORIES: {
                "--repository": {"dest":"repository", "required": True, "help": ""},
                "--branch": {"dest":"branch", "required": False, "default": None, "help": ""},
            }
        }
        return stage_specific_params.get(Stages(stage), {})

    def parse_args(self, args: List[str]) -> Namespace:
        parsed_args, unknown_args = self._parser.parse_known_args(args)
        stage_specific_parameters = self._get_stage_parameters(parsed_args.stage)
        for key, value in stage_specific_parameters.items():
            self._parser.add_argument(key, **value)

        return self._parser.parse_args(args)
