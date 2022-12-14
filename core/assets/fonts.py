from functools import lru_cache as _lru_cache

import pygame as _pg
from pygame.font import Font as _Font

from core.api import EventManager as _EventManager
from core.api import Renderer as _Renderer
from core.api import event_handler as _event_handler


@_lru_cache
def _load_font(path, size):
    return _Font(path, size)


class _PartialFont:
    def __init__(self, path):
        self.path = path

    def of_size(self, size):
        return _load_font(self.path, round(size * _Renderer().surface_h_scale))


gui_regular = _PartialFont("assets\\fonts\\ClearSans Regular.ttf")
gui_bold = _PartialFont("assets\\fonts\\ClearSans Bold.ttf")
gui_italic = _PartialFont("assets\\fonts\\ClearSans Italic.ttf")
gui_bolditalic = _PartialFont("assets\\fonts\\ClearSans BoldItalic.ttf")

cmu_roman = _PartialFont("assets\\fonts\\CMU Serif Roman.ttf")
cmu_bold = _PartialFont("assets\\fonts\\CMU Serif Bold.ttf")
cmu_italic = _PartialFont("assets\\fonts\\CMU Serif Italic.ttf")
cmu_bolditalic = _PartialFont("assets\\fonts\\CMU Serif BoldItalic.ttf")
