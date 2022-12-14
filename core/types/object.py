from core.api import Renderer


class Object:
    def __init__(self, name):
        self.name = name

    def start(self):
        pass

    def update(self, dt: float):
        pass

    def draw(self, renderer: Renderer):
        pass

    def end(self):
        pass
