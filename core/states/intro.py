from core import assets
from core.api import Renderer
from core.objects import IntroText
from core.types import State


class IntroState(State):
    def __init__(self):
        name = "intro"
        Renderer().bg_color = assets.colors.white
        super().__init__(name)

    def start(self):
        self.set_objects([IntroText()])
        super().start()
