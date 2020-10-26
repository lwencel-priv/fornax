import subprocess
import datetime
import uuid
from pathlib import Path
from threading import Thread
from typing import Optional, Iterable

from fornax.logger import console_logger, main_logger
from ..command import Command


class Process:
    def __init__(self, command: Command, workspace: Path) -> None:
        """Initialize process.
        :param command: command to run
        :type command: Command
        :param workspace: workspace for output
        :type workspace: Path
        """
        workspace.mkdir(parents=True, exist_ok=True)
        process_uuid = uuid.uuid4()
        self._stdout_log = workspace.joinpath(f"{process_uuid}_stdout.log")
        self._stderr_log = workspace.joinpath(f"{process_uuid}_stderr.log")
        self._command = command

        main_logger.debug(f"Running: {self._command}")
        self._return_code: Optional[int] = None
        self._start_time: datetime.datetime = datetime.datetime.utcnow()
        self._stop_time: Optional[datetime.datetime] = None
        self._process = subprocess.Popen(
            self._command.args,
            cwd=self._command.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="ignore",
        )
        self._data_collector_thread = Thread(target=self.__flow, daemon=True)
        self._data_collector_thread.start()
        if not self._command.daemon:
            self._data_collector_thread.join()

    def __flow(self) -> None:
        stdout_thread = Thread(target=self._collect_stdout, daemon=True)
        stderr_thread = Thread(target=self._collect_stderr, daemon=True)
        stdout_thread.start()
        stderr_thread.start()
        self._return_code = self._process.wait()
        self._stop_time = datetime.datetime.utcnow()
        stdout_thread.join()
        stderr_thread.join()

    def _collect_stdout(self) -> None:
        """Collect stdout."""
        with open(self._stdout_log, "w") as stdout_stream:
            for line in self._process.stdout:  # type: ignore
                console_logger.info(line.strip())
                stdout_stream.write(line)

    def _collect_stderr(self) -> None:
        """Collect stderr."""
        with open(self._stderr_log, "w") as stderr_stream:
            for line in self._process.stderr:  # type: ignore
                console_logger.warning(line.strip())
                stderr_stream.write(line)

    @property
    def stdout(self) -> Iterable[str]:
        """Return standard output iterator.

        :return: return standard output iterator
        :rtype: Iterable[str]
        """
        with open(self._stdout_log, "r") as stream:
            yield from stream

    @property
    def stderr(self) -> Iterable[str]:
        """Return standard error iterator.

        :return: return standard error iterator
        :rtype: Iterable[str]
        """
        with open(self._stderr_log, "r") as stream:
            yield from stream

    @property
    def return_code(self) -> Optional[int]:
        """Return process exit code.

        :return: process exit code or None if process is running
        :rtype: Optional[int]
        """
        return self._return_code

    @property
    def start_time(self) -> datetime.datetime:
        """Return command execution start time.

        :return: command execution start time
        :rtype: datetime.datetime
        """
        return self._start_time

    @property
    def stop_time(self) -> Optional[datetime.datetime]:
        """Return command execution stop time.

        :return: command execution stop time or None if command execution not finished
        :rtype: Optional[datetime.timedelta]
        """
        return self._stop_time

    @property
    def duration(self) -> Optional[float]:
        """Return command execution duration in.

        :return: command execution duration or None if command execution not finished
        :rtype: Optional[float]
        """
        if self._stop_time:
            return (self._stop_time - self._start_time).total_seconds()

        return None
