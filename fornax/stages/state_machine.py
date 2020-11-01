from typing import Optional, Dict
from pathlib import Path
from argparse import Namespace

from fornax.consts import StageType
from fornax.utils.file_processors import PickleProcessor
from fornax.logger import main_logger
from .transision import Transition
from .base_stage import BaseStage
from .sync import SyncStage
from .checkout import CheckoutStage
from .prepare_environment import PrepareEnvironmentStage


class StageStateMachine:
    def __init__(self, workspace: Path) -> None:
        """Initialize stage state machine.

        :param workspace: workspace path
        :type workspace: Path
        """
        self._transitions = [
            Transition(
                name=StageType.SYNC,
                transition_class=SyncStage,
                previous_stages=[],
                next_stages=[StageType.SYNC, StageType.CHECKOUT, StageType.PREPARE_ENVIRONMENT],
            ),
            Transition(
                name=StageType.CHECKOUT,
                transition_class=CheckoutStage,
                previous_stages=[StageType.SYNC],
                next_stages=[StageType.CHECKOUT, StageType.PREPARE_ENVIRONMENT],
            ),
            Transition(
                name=StageType.PREPARE_ENVIRONMENT,
                transition_class=PrepareEnvironmentStage,
                previous_stages=[StageType.SYNC, StageType.CHECKOUT],
                next_stages=[StageType.PREPARE_ENVIRONMENT, StageType.BUILD],
            ),
        ]
        self._data_processor = PickleProcessor()
        self._state_file_path = workspace.joinpath("state.bin")

        self._args: Dict[StageType, Namespace] = {}
        self._current_transition: Optional[Transition] = None
        self._current_stage_instance: Optional[BaseStage] = None
        self.__load_sate()

    def next_stage(self, args: Namespace) -> None:
        """Execute next stage.

        :param args: stage args
        :type args: Namespace
        :return: next stage instance
        :rtype: Stage
        """
        if self._current_transition is None and args.stage != StageType.SYNC:
            raise ValueError(f"Cannot switch to {args.stage}. Allowed stages: {StageType.SYNC}.")

        if self._current_transition is not None and args.stage not in self._current_transition.allowed_transitions:
            raise ValueError(
                f"Cannot switch {self._current_transition.name} -> {args.stage}. "
                f"Allowed stages: {self._current_transition.allowed_transitions}."
            )

        self._current_transition = self._find_transition(args.stage)
        self._update_args(self._current_transition, args)
        self._current_stage_instance = self._current_transition.create_stage(self._args, args)
        self.__save_sate()

    def run(self) -> None:
        """Run current stage."""
        if self._current_stage_instance is None:
            raise ValueError("Cannot execute not initialized stage.")

        self._current_stage_instance.run()

    def _find_transition(self, name: StageType) -> Transition:
        """Find transition by name.

        :param name: transition name
        :type name: StageType
        :return: transition instance
        :rtype: Transition
        """
        for item in self._transitions:
            if item.name == name:
                return item

        raise ValueError(f"Unknown transition name {name}.")

    def _update_args(self, transition: Transition, new_args: Namespace) -> None:
        """Update known args.

        :param new_args: new args to add
        :type new_args: Namespace
        """
        for next_stage in transition.next_stages:
            if next_stage in self._args:
                self._args.pop(next_stage)

        self._args.update({new_args.stage: new_args})

    def __save_sate(self) -> None:
        """Save state."""
        self._data_processor.write(
            self._state_file_path,
            {"args": self._args, "current_transition": self._current_transition},
        )

    def __load_sate(self) -> None:
        """Load state."""
        if self._state_file_path.exists():
            data = self._data_processor.read(self._state_file_path)
            self._args = data["args"]
            self._current_transition = data["current_transition"]
