from multiprocessing import cpu_count
from fornax.executor.command import Command
from fornax.executor import BashShellExecutor


class GitRepo:
    def __init__(self, manifest_path: str):
        self.__executor = BashShellExecutor()
        self.__manifest_path = manifest_path

    def sync(self) -> None:
        commands = [
            Command(["repo", "init", "-u", self.__manifest_path]),
            Command(["repo", "forall", "git", "reset", "--hard"]),
            Command(["repo", "forall", "git", "clean", "-dfx"]),
            Command(["repo", "sync", "-j", cpu_count()]),
        ]
        for command in commands:
            self.__executor.run(command)
