from typing import Sequence

from core.api import Renderer


class State:
    def __init__(self, name):
        self.name = name
        self.objects = {}

    def start(self):
        # Add objects here.
        for object in self.get_objects():
            object.start()

    def update(self, dt: float):
        for object in self.get_objects():
            object.update(dt)

    def draw(self, renderer: Renderer):
        for object in self.get_objects():
            object.draw(renderer)

    def end(self):
        for object in self.get_objects():
            object.end()
        self.objects.clear()

    def get_objects(self):
        return self.objects.values()

    def set_objects(self, sequence: Sequence):
        for object in sequence:
            self.objects[object.name] = object
