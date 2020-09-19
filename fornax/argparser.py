from argparse import ArgumentParser, Namespace


class ArgumentParser:
    
    def __init__(self):
        parser = ArgumentParser(description='Project build pipeline.')
        parser.add_argument('--workspace', dest='workspace', required=True, help='workspace')
        parser.add_argument('--repo', dest='repo', required=True, help='')
        parser.add_argument('--stage', dest='stage', help='')
        self._initial_args = parser.parse_known_args()
