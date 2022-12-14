from functools import partial
from typing import Callable

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
        draw_rect : Rect
            The part of the screen where things are drawn.
        inner_color : Color
            The color of the part of the screen to be drawn upon.
        layer_count : int
            The numbers of layers to draw.
        outer_color : Color
            The color of the part of the screen to be not be drawn upon.
        surface_h_scale : float
            The ratio between the screen current and original height.
    """

    def __init__(self):
        """
        Initialize the renderer.
        """
        self.outer_color = pg.Color(0, 0, 0)
        self.inner_color = pg.Color(225, 225, 225)
        self.layer_count = 3
        self._layers = [[] for _ in range(self.layer_count)]

        # Resize related things:
        self._ratio = self.screen_size[0] / self.screen_size[1]
        self._org_h = self.screen_size[1]
        self.surface_h_scale = 1.00

        self.draw_rect = pg.Rect((0, 0), self.screen_size)

        def on_resize(renderer):
            win_size = pg.display.get_window_size()
            new_size = (renderer._ratio * win_size[1], win_size[1])
            new_pos = ((win_size[0] - new_size[0]) / 2, 0)

            renderer.draw_rect = pg.Rect(new_pos, new_size)
            renderer.surface_h_scale = win_size[1] / renderer._org_h

        def while_resize(renderer):
            on_resize(renderer)
            renderer._update(entire_screen=True)

        if Win32Methods.get_supported():
            Win32Methods._call_while_resize(partial(while_resize, self))
        else:
            handler = event_handler(type=pg.VIDEORESIZE)(on_resize)
            EventManager().add_handler(handler, renderer=self)

    def _update(self, entire_screen=False):
        self.screen.fill(self.inner_color, self.draw_rect)

        for layer in self._layers:
            for draw_callback in layer:
                draw_callback()

        if entire_screen:
            pg.display.flip()
        else:
            pg.display.update(self.draw_rect)

        self._layers = [[] for _ in range(self.layer_count)]

    def blit(self, layer_id, surface, pos):
        def blit_callback(renderer):
            renderer.screen.blit(surface, pos)

        self._layers[layer_id].append(partial(blit_callback, self))

    @property
    def screen(self):
        return pg.display.get_surface()

    @property
    def screen_size(self):
        return np.array(pg.display.get_window_size())
