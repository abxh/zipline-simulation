import pygame as pg
from zls.types.scene import Scene

class Assets():
    image_dict: dict[str, pg.Surface]     = {}
    font_dict : dict[str, pg.font.Font]   = {}
    color_dict: dict[str, pg.color.Color] = {}
    scene_dict: dict[str, Scene]          = {}
    
    font_sizes: tuple[int] = ()