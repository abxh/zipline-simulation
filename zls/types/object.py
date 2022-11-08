
from pygame import Surface
from pygame.event import Event


class Object():
    def __init__(self, name):
        self.name = name
        self.scene = None

    def start(self):
        pass
    
    def update(self, dt: int, events: list[Event]):
        pass
    
    def draw(self, surface: Surface, scale_y: float):
        pass