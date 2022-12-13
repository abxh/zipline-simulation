from functools import lru_cache as _lru_cache

import pygame as _pg

from core.api import EventManager as _EventManager
from core.api import event_handler as _event_handler


@_lru_cache
def _load_image(path):
    return _pg.image.load(path)


@_lru_cache
def _load_image_convert(path, alpha):
    if alpha:
        return _pg.image.load(path).convert_alpha()
    else:
        return _pg.image.load(path).convert()


def reconvert_on_resize():
    handler = _event_handler(_pg.VIDEORESIZE)(_load_image_convert.cache_clear)
    _EventManager().add_handler(handler)


class PartialImage:
    def __init__(self, path):
        self.path = path

    def as_surface(self, convert=True, alpha=False):
        if not convert:
            return _load_image(self.path)
        else:
            return _load_image_convert(self.path, alpha)


zls_icon = PartialImage("assets\\images\\zls_icon.png")
