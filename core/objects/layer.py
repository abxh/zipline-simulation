from typing import Callable

import numpy as np
import pygame as pg

from core.api import EventManager, Renderer, event_handler
from core.assets import fonts
from core.types import Object


class Layer(Object):
    def __init__(
        self,
        name,
        rel_start_pos,
        rel_end_pos,
        title,
        color,
        line_color,
        line_thickness,
        border_height,
        border_color,
        text_size,
        text_x_offset,
        text_color,
    ):
        super().__init__(name)
        self.rel_start_pos = rel_start_pos
        self.rel_end_pos = rel_end_pos

        self.title = title
        self.color = color

        self.line_color = line_color
        self.line_thickness = line_thickness

        self.border_height = border_height
        self.border_height_org = border_height
        self.border_color = border_color

        self.text_size = text_size
        self.text_x_offset = text_x_offset
        self.text_offset_org = text_x_offset
        self.text_color = text_color

        self.start_pos = None
        self.end_pos = None
        self.size = None
        self.rect: pg.Rect = pg.Rect((0, 0), (0, 0))
        self.border_rect: pg.Rect = pg.Rect((0, 0), (0, 0))
        self.resize_points: Callable | None = None
        self.handler_id = -1

    def start(self):
        def on_resize(l: Layer, r: Renderer):
            l.start_pos = r.dpos + r.dsize * l.rel_start_pos
            l.end_pos = r.dpos + r.dsize * l.rel_end_pos
            l.size = l.end_pos - l.start_pos
            l.rect = pg.Rect(l.start_pos, l.size)
            l.border_height = r._h_scale * l.border_height_org
            l.border_rect = pg.Rect(*l.start_pos, l.rect.size[0], l.border_height)
            l.text_x_offset = r._h_scale * l.text_offset_org

        handler = event_handler(type=pg.VIDEORESIZE)(on_resize)
        self.handler_id = EventManager().add_handler(handler, l=self, r=Renderer())

        on_resize(l=self, r=Renderer())

        self.on_resize = on_resize
        super().start()

    def draw(self, renderer: Renderer):
        renderer.draw_color(0, self.color, self.rect)
        renderer.draw_rect(
            -2,
            self.border_color,
            self.border_rect,
        )
        fs = fonts.gui_regular.of_size(self.text_size).render(
            self.title, True, self.text_color
        )
        renderer.draw_surface(-1, fs, self.start_pos + (self.text_x_offset, 0))
        renderer.draw_line(
            -1,
            self.line_color,
            self.rect.topleft,
            self.rect.topright,
            self.line_thickness,
        )
        renderer.draw_line(
            -1,
            self.line_color,
            self.rect.topleft,
            self.rect.bottomleft,
            self.line_thickness,
        )
        renderer.draw_line(
            -1,
            self.line_color,
            self.rect.topright,
            self.rect.bottomright,
            self.line_thickness,
        )
        renderer.draw_line(
            -1,
            self.line_color,
            self.rect.bottomleft,
            self.rect.bottomright,
            self.line_thickness,
        )

    def end(self):
        EventManager().remove_handler(self.handler_id)
