import json

from pathlib import Path
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

from typing import List, Optional


class Command:
    def __init__(self, args: List[str], cwd: Optional[Path] = None, daemon: bool = False) -> None:
        """Initialize command.
        :param args: command args
        :type args: List[str]
        :param cwd: command working directory, defaults to None
        :type cwd: Optional[Path], optional
        :param daemon: run command as daemon, defaults to False
        :type daemon: bool, optional
        """
        :param daemon: run command as daemon, defaults to False
        :type daemon: bool, optional
        """
        self._args: List[str] = args
        self._cwd = cwd
        self._daemon = daemon

    @property
    def args(self) -> List[str]:
        """Return command args.

        :return: command args
        :rtype: List[str]
        """
        return self._args

    @property
    def cwd(self) -> Optional[Path]:
        """Return command working directory.

        :return: command working directory
        :rtype: Optional[Path]
        """
        return self._cwd

    @property
    def daemon(self) -> bool:
        """Check if command is a daemon.

        :return: True if command is a daemon else False
        :rtype: bool
        """
        return self._daemon

    def __str__(self) -> str:
        """Cast obj instance to string.

        :return: obj instance as a string
        :rtype: str
        """
        return json.dumps(
            {
                "args": self._args,
                "cwd": str(self._cwd),
                "daemon": self._daemon,
            }
        )
