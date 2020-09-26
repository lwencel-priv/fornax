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

import json
from typing import List, Optional


class Command:

    def __init__(self, args: List[str], cwd: Optional[str] = None, daemon: bool = False) -> None:
        self._args: List[str] = args
        self._cwd = cwd
        self._daemon = daemon

    @property
    def args(self) -> List[str]:
        return self._args
    
    @property
    def cwd(self) -> List[str]:
        return self._cwd
        
    @property
    def daemon(self) -> List[str]:
        return self._daemon

    def __str__(self) -> str:
        return json.dumps({
            "args": self._args,
            "cwd": self._cwd,
            "daemon": self._daemon,
        })
