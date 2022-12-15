import pygame as pg

from core import assets, states
from core.api import Win32Methods, WindowExtended


class Simulation(WindowExtended):
    def __init__(self):
        title = "Zipline Simulation"
        icon = assets.images.zls_icon.as_surface(convert=False)
        size = (800, 600)
        flags = pg.RESIZABLE
        max_fps = 60

        super().__init__(title, icon, size, flags, max_fps)

        assets.images.reconvert_on_resize()

        if Win32Methods.supported:
            Win32Methods.maximize()

        self._states = states.get_states_dict()
        self._prev_state_name = None
        self.next_state_name = "intro"

    def run(self):
        super().run()

    def loop_method(self):
        prev_name = self._prev_state_name
        next_name = self.next_state_name

        if next_name != prev_name:
            if prev_name is not None:
                self._states[prev_name].end()
            self._states[next_name].start()
            self._prev_state_name = next_name

        self._states[next_name].update(self.dt)
        self._states[next_name].draw(self.renderer)

    @property
    def current_state(self):
        return self._states[self.next_state_name]
