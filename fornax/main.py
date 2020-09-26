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

import os
import sys
from argparse import Namespace

from fornax.executor import BashShellExecutor
from fornax.executor.command import Command
from fornax.utils.repository.git_repo import GitRepo
from fornax.utils import DynamicArgumentParser


class Pipeline:

    def __init__(self, args: Namespace) -> None:
        self._args = args
        os.makedirs(self._args.workspace, exist_ok=True)
        self._repo = GitRepo(self._args.repository, self._args.branch, self._args.workspace)

    def execute(self):
        self._repo.sync()


if __name__ == "__main__":
    parser = DynamicArgumentParser(description='Project build pipeline.')
    args = parser.parse_args(sys.argv[1:])
    pipeline = Pipeline(args)
    pipeline.execute()
