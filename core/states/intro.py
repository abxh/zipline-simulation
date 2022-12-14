from core import assets
from core.api import Renderer
from core.objects import IntroText
from core.types import State


class IntroState(State):
    def __init__(self):
        name = "intro"
        super().__init__(name)
        Renderer().inner_color = assets.colors.white

    def start(self):
        self.set_objects([IntroText()])
        return super().start()
