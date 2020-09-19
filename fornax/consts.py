from enum import Enum


class Stages(Enum):
    SYNC_REPOSITORIES = "sync_repositories"
    PREPARE_ENVIRONMENT = "prepare_environment"
    BUILD = "build"
    TEST = "test"


class Environment(Enum):
    DOCKER = "docker"
    BARE = "bare"
