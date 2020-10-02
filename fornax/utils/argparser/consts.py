from .arg_enum import ArgEnum


class Stages(ArgEnum):
    """Pipeline stages."""

    SYNC_REPOSITORIES = "sync_repositories"
    PREPARE_ENVIRONMENT = "prepare_environment"
    BUILD = "build"
    TEST = "test"


class Environment(ArgEnum):
    """Environment types."""

    DOCKER = "docker"
    BARE = "bare"


class SupportedRepositories(ArgEnum):
    """Supported repositories types."""

    GIT = "git"
    GIT_REPO = "git_repo"
