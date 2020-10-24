from fornax.utils.generics.string_enum import StringEnum


class Stage(StringEnum):
    """Pipeline stages."""

    SYNC = "sync"
    PREPARE_ENVIRONMENT = "prepare_environment"
    BUILD = "build"
    TEST = "test"


class Environment(StringEnum):
    """Environment types."""

    DOCKER = "docker"
    BARE = "bare"


class ManifestType(StringEnum):
    """Supported manifest types."""

    NONE = "none"
    GIT_REPO = "git_repo"


class SourcePathType(StringEnum):
    """Supported source path types."""

    REPOSITORY_ADDRESS = "repository_address"
