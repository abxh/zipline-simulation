import pygame as pg

from pygame import Surface
from pygame.event import Event


class Scene():
    def __init__(self, name):
        self.name = name
        self.object_dict = {}
        self.next_scene_name = self.name
    
    def add_object(self, object):
        self.object_dict[object.name] = object
        object.scene = self
    
    def del_object(self, object_name):
        del self.object_dict[object_name]
        
    def start(self):
        for name, object in self.object_dict.items():
            object.start()
    
    def update(self, dt: int, events: list[Event]):
        for name, object in self.object_dict.items():
            object.update(dt, events)
    
    def draw(self, surface: Surface, scale_y: float):
        for name, object in self.object_dict.items():
            object.draw(surface, scale_y)