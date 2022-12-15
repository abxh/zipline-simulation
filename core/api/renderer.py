from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable

import numpy as np
import pygame as pg

from core.api._singletontype import SingletonType

if TYPE_CHECKING:
    # Avoid non-actual recursive imports due to type hinting
    from core.api.eventmanager import EventManager
    from core.api.windowextended import WindowExtended


class Renderer(metaclass=SingletonType):
    """
    This class provides a centralised way of managing drawing tasks.

    It draws elements to the screen by the order of their layer index.

    Additionally, as a singleton class, it can be invoked anywhere in the code to
    draw things to the screen.

    Attributes
    ----------
        bg_color : pygame.Color
            The background color in the drawable area.

        layer_count : int
            The number of layers to use. Drawable layers are in the range
            between `0` and `layer_count` with the latter not included.

        outside_color : pygame.Color
            The color outside the drawable area.
    """

    def __init__(self, window: WindowExtended, eventmanager: EventManager):
        """
        Initialize the renderer.
        """
        self._window = window
        self._eventmanager = eventmanager

        self.outside_color = pg.Color(0, 0, 0)
        self.bg_color = pg.Color(225, 225, 225)

        self.layer_count = 5
        self._layers: list[list[Callable]] = [[] for _ in range(self.layer_count)]

        # Resize related things:
        self._w_to_h_ratio = self.screen_size[0] / self.screen_size[1]
        self._org_h = self.screen_size[1]
        self._h_scale = 1.00

        self.drect = pg.Rect((0, 0), self.screen_size)
        self.dsize = np.array(self.screen_size)
        self.dpos = np.array((0, 0))

        def on_resize(renderer: Renderer, window):
            win_size = window.size
            new_size = (renderer._w_to_h_ratio * win_size[1], win_size[1])

            # Prevent rectangle width from being larger than screen width.
            if new_size[0] > win_size[0]:
                window.size = new_size
                win_size = new_size

            new_pos = ((win_size[0] - new_size[0]) / 2, 0)
            new_rect = pg.Rect(new_pos, new_size)
            new_h_scale = win_size[1] / renderer._org_h
            left_outer_area = ((0, 0), new_rect.bottomleft)
            right_outer_area = (new_rect.topright, win_size)

            renderer.drect = new_rect
            renderer.dsize = np.array(new_size)
            renderer.dpos = np.array(new_pos)
            renderer._h_scale = new_h_scale

            pg.display.update((left_outer_area, right_outer_area))

        eventmanager.add_new_handler(
            on_resize, type=pg.VIDEORESIZE, renderer=self, window=window
        )

        self._on_resize = on_resize

    def _update(self):
        self.screen.fill(self.bg_color, self.drect)

        for layer in self._layers:
            for draw_callback in layer:
                draw_callback()

        pg.display.update(self.drect)

        self._layers = [[] for _ in range(self.layer_count)]

    def draw_surface(self, layer_id, surface, pos):
        def blit_callback(renderer):
            renderer.screen.blit(surface, pos)

        self._layers[layer_id].append(partial(blit_callback, self))

    def draw_color(self, layer_id, color, rect):
        def fill_callback(renderer):
            renderer.screen.fill(color, rect)

        self._layers[layer_id].append(partial(fill_callback, self))

    def draw_line(self, layer_id, color, start_pos, end_pos, width=1):
        def line_callback(renderer):
            pg.draw.line(renderer.screen, color, start_pos, end_pos, width)

        self._layers[layer_id].append(partial(line_callback, self))

    def draw_rect(
        self,
        layer_id,
        color,
        rect,
        border_radius: tuple[int, int, int, int] | None = None,
    ):
        def line_callback(renderer: Renderer):
            if border_radius:
                kwargs = {
                    "border_top_left_radius": border_radius[0],
                    "border_top_right_radius": border_radius[1],
                    "border_bottom_left_radius": border_radius[2],
                    "border_bottom_right_radius": border_radius[3],
                }
            else:
                kwargs = {}
            pg.draw.rect(renderer.screen, color, rect, **kwargs)

        self._layers[layer_id].append(partial(line_callback, self))

    @property
    def screen(self):
        return pg.display.get_surface()

    @property
    def screen_size(self):
        return np.array(pg.display.get_window_size())
