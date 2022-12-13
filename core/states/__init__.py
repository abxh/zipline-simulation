from core.states.intro import IntroState
from core.states.runtime_test import RuntimeTestState
from core.states.visual import VisualState
from core.types import State


def get_states_dict() -> dict[str, State]:
    states = [IntroState(), RuntimeTestState(), VisualState()]
    return {state.name: state for state in states}
