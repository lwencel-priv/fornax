from typing import List
from fornax.utils.generics.string_enum import StringEnum


class StageType(StringEnum):
    """Pipeline stages."""

    SYNC = "sync"
    CHECKOUT = "checkout"
    PREPARE_ENVIRONMENT = "prepare_environment"
    BUILD = "build"
    TEST = "test"

    @staticmethod
    def get_order() -> List["StageType"]:
        """Get stages order.

        :return: stages order
        :rtype: List["Stage"]
        """
        return [
            StageType.SYNC,
            StageType.CHECKOUT,
            StageType.PREPARE_ENVIRONMENT,
            StageType.BUILD,
            StageType.TEST,
        ]


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
    ARTIFACTORY = "artifactory"
