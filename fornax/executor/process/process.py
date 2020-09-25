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

import subprocess
from threading import Thread
from typing import Optional

from fornax.logger import console_logger
from ..command import Command


class Process:

    def __init__(self, command: Command) -> None:
        self._command = command
        self._return_code = None

        self._process = subprocess.Popen(
            self._command.args,
            cwd=self._command.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding='utf-8',
            errors='ignore',
        )
        self._stdout_thread = Thread(target=self._collect_stdout, daemon=True)
        self._stderr_thread = Thread(target=self._collect_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()
        if not self._command.daemon:
            self._return_code = self._process.wait()
            self._stdout_thread.join()
            self._stderr_thread.join()

    def _collect_stdout(self) -> None:
        for line in self._process.stdout:
            console_logger.info(line.strip())

    def _collect_stderr(self) -> None:
        for line in self._process.stderr:
            console_logger.error(line.strip())

    @property
    def return_code(self) -> Optional[int]:
        return self._return_code
