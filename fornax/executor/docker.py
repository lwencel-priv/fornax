from pathlib import Path
from .command import Command
from .process import Process
from .executor import Executor
from .exceptions import ExecutorError


class DockerExecutor(Executor):
    def __init__(self, workspace: Path, image_name: str, container_name: str = "fornax_executor") -> None:
        """Initialize docker executor.

        :param workspace: workspace dedicated output files e.g. logs
        :type workspace: str
        :param image_name: docker image name with tag
        :type image_name: str
        :param container_name: container name, defaults to "fornax_executor"
        :type container_name: str, optional
        """
        super().__init__(workspace)
        self.__image_name = image_name
        self.__container_name = container_name

        command = Command(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "--name",
                self.__container_name,
                self.__image_name,
                "tail",
                "-f",
                "/dev/null",
            ]
        )
        process = super().run(command)
        if process.return_code != 0:
            raise ExecutorError("Cannot run docker container.")

    def run(self, command: Command) -> Process:
        """Run command.

        :param command: command to run
        :type command: Command
        :return: process instance
        :rtype: Process
        """
        cmd = ["docker", "exec", "--name", self.__container_name]
        if command.daemon:
            cmd.append("-d")

        if command.cwd:
            cmd.extend(["-w", str(command.cwd)])

        cmd.append(self.__image_name)
        cmd.extend(command.args)

        docker_command = Command(cmd)
        return super().run(docker_command)
