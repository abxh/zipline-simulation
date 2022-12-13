from core.types import State


class RuntimeTestState(State):
    def __init__(self):
        name = "runtime_test"
        super().__init__(name)
