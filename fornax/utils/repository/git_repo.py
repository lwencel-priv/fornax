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

from multiprocessing import cpu_count

from fornax.executor.command import Command
from fornax.executor import BashShellExecutor
from fornax.logger import main_logger


class GitRepo:
    def __init__(self, manifest_path: str, branch: str, workspace: str):
        self.__executor = BashShellExecutor()
        self.__manifest_path = manifest_path
        self.__branch = branch
        self.__workspace = workspace

    def sync(self) -> None:
        repo_init_command = ["repo", "init", "-u", self.__manifest_path]
        if self.__branch is not None:
            repo_init_command += ["-b", self.__branch]

        commands = [
            Command(repo_init_command, cwd=self.__workspace),
            Command(["repo", "forall", "git reset --hard"], cwd=self.__workspace),
            Command(["repo", "forall", "git clean -dfx"], cwd=self.__workspace),
            Command(["repo", "sync", "-j", str(max(cpu_count() - 2, 1))], cwd=self.__workspace),
        ]
        main_logger.info("Starting repositories synchronization.")
        for command in commands:
            self.__executor.run(command)
        main_logger.info("Repositories synchronization done.")
