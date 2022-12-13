from functools import partial

import numpy as np
import pygame as pg

from core.api._singletontype import SingletonType
from core.api.eventmanager import EventManager, event_handler
from core.api.win32methods import Win32Methods


class Renderer(metaclass=SingletonType):
    """
    This class draws things to the screen.

    Attributes
    ----------
        bg_color : Color
            The color of the drawable surface.
        layer_count : int
            The number of layers that are drawable.
        surface : Surface
            The drawable surface of the screen.
        surface_size : NDArray
            The size of the drawable surface.
        surface_pos : NDArray
            The position of the drawable surface.
        surface_rect : Rect
            The pygame rect of the drawable surface.
    """

    def __init__(self):
        """
        Initialize the renderer.
        """
        self.bg_color = pg.Color(225, 225, 225)
        self._layers = [[], [], []]

        # Resize related things:
        self._ratio = self._screen_size[0] / self._screen_size[1]
        self.surface = pg.Surface(self._screen_size)
        self.surface_pos = np.array([0, 0])

        def on_resize(renderer):
            win_size = pg.display.get_window_size()
            new_size = (renderer._ratio * win_size[1], win_size[1])

            renderer.surface = pg.Surface(new_size)
            renderer.surface_pos = np.array([(win_size[0] - new_size[0]) / 2, 0])

        def while_resize(renderer):
            on_resize(renderer)
            renderer._update()

        if Win32Methods.get_supported():
            Win32Methods._call_while_resize(partial(while_resize, self))
        else:
            handler = event_handler(type=pg.VIDEORESIZE)(on_resize)
            EventManager().add_handler(handler, renderer=self)

    def _update(self):
        self.surface.fill(self.bg_color)
        self._screen.blit(self.surface, self.surface_pos)
        for layer in self._layers:
            for draw_callback in layer:
                draw_callback()
        pg.display.flip()
        self._layers = [[], [], []]

    @property
    def layer_count(self):
        return len(self._layers)

    @property
    def surface_size(self):
        return np.array(self.surface.get_size())

    @property
    def surface_rect(self):
        return self.surface.get_rect(topleft=self.surface_pos)

    @property
    def _screen(self):
        return pg.display.get_surface()

    @property
    def _screen_size(self):
        return np.array(pg.display.get_window_size())
