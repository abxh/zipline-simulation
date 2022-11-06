from pygame import Surface
from pygame.color import Color
from pygame.font import Font

from zls.data.types.scene import Scene

class Assets():
    image_dict: dict[str, Surface] = {}
    font_dict : dict[str, Font]    = {}
    color_dict: dict[str, Color]   = {}
    scene_dict: dict[str, Scene]   = {}