import pygame as pg

from zls.data.types.scene import Scene, Surface
from zls.data.assets import Assets as a
from zls.data.objects.introtext import IntroText

class IntroScene(Scene):
    def start(self):
        self.add_object(IntroText('Introduction Text'))
        self.bg_color = a.color_dict['white']
        super().start()
    
    def draw(self, surface: Surface):
        surface.fill(self.bg_color)
        super().draw(surface)

introscene = IntroScene('Introduction Scene')