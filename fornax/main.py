from argparse import ArgumentParser, Namespace

from fornax.executor import BashShellExecutor
from fornax.executor.command import Command
from fornax.repository.git_repo import GitRepo


class Pipeline:

    def __init__(self, args: Namespace) -> None:
        self._args = args

    def execute(self):
        repo = GitRepo(self._args.repo)
        repo.sync()


if __name__ == "__main__":
    # https://android.googlesource.com/platform/manifest/+/refs/heads/master/default.xml
    parser = ArgumentParser(description='Project build pipeline.')
    parser.add_argument('--repo', dest='repo', required=True, help='')
    parser.add_argument('--workspace', dest='workspace', required=True, help='workspace')
    parser.add_argument('--stage', dest='stage', help='')
    args = parser.parse_known_args()

    pipeline = Pipeline(args[0])
    pipeline.execute()
