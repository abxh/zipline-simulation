import pygame as pg

from zls.types.scene import Scene, Surface
from zls.assets import Assets
from zls.objects.introtext import IntroText


class IntroScene(Scene):
    def start(self):
        self.add_object(IntroText('Introduction Text'))
        self.bg_color = Assets.color_dict['white']
        
        super().start()
    
    def draw(self, surface: Surface, scale_y: float):
        surface.fill(self.bg_color)
        
        super().draw(surface, scale_y)

introscene = IntroScene('Introduction Scene')