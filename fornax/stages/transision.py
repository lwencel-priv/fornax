from typing import List, Type, Dict
from argparse import Namespace

from fornax.consts import StageType
from .base_stage import BaseStage


class Transition:
    def __init__(
        self,
        name: StageType,
        transition_class: Type[BaseStage],
        previous_stages: List[StageType],
        next_stages: List[StageType],
        allow_previous_stage_transition: bool = True,
    ) -> None:
        """Initialize transition.

        :param name: transition name
        :type name: StageType
        :param transition_class: transision class
        :type transition_class: BaseStage
        :param previous_stages: previous stage types
        :type previous_stages: List[StageType]
        :param next_stages: next stage types
        :type next_stages: List[StageType]
        :param allow_previous_stage_transition: allow transition to previous stages, defaults to True
        :type allow_previous_stage_transition: bool
        """
        self._name = name
        self._transition_class = transition_class
        self._previous_stages = previous_stages
        self._next_stages = next_stages
        self._allow_previous_stage_transition = allow_previous_stage_transition

    @property
    def name(self) -> StageType:
        """Return transition name.

        :return: transition name
        :rtype: StageType
        """
        return self._name

    def create_stage(self, prev_stages_args: Dict[StageType, Namespace], args: Namespace) -> BaseStage:
        """Create stage class instance.

        :param prev_stages_args: previous stages args
        :type prev_stages_args: Dict[StageType, Namespace]
        :param args: current stage args
        :type args: Namespace
        :return: transision class instance
        :rtype: Type[BaseStage]
        """
        instance = self._transition_class(prev_stages_args, args)
        return instance

    @property
    def previous_stages(self) -> List[StageType]:
        """Return previous stages.

        :return: previous stages
        :rtype: List[StageType]
        """
        return self._previous_stages

    @property
    def next_stages(self) -> List[StageType]:
        """Return next stages.

        :return: next stages
        :rtype: List[StageType]
        """
        return self._next_stages

    @property
    def allowed_transitions(self) -> List[StageType]:
        """Return possible target stage types.

        :return: possible target stage types
        :rtype: List[StageType]
        """
        if self._allow_previous_stage_transition:
            return self._previous_stages + self._next_stages

        return self._next_stages
