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
