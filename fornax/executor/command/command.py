import json
from typing import List, Optional


class Command:
    def __init__(self, args: List[str], cwd: Optional[str] = None, daemon: bool = False) -> None:
        """Initialize command.

        :param args: command args
        :type args: List[str]
        :param cwd: command working directory, defaults to None
        :type cwd: Optional[str], optional
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
    def cwd(self) -> Optional[str]:
        """Return command working directory.

        :return: command working directory
        :rtype: Optional[str]
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
                "cwd": self._cwd,
                "daemon": self._daemon,
            }
        )
