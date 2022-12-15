import numpy as np
import pygame as pg

import core.simulation as s
from core.objects.layer import Layer
from core.types import Object


class AnimateButton(Object):
    def __init__(self):
        name = "animate_button"
        super().__init__(name)

    def start(self):
        pass
