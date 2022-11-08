import pygame as pg

from pathlib import Path

window_title     = 'Zipline Simulation'
window_icon_path = 'assets/images/zls-icon.png'
window_size      = (800, 600)
window_flags     = pg.RESIZABLE | pg.DOUBLEBUF # | pg.SCALED
window_fps       = 60

# From parent directory:
assets_path = Path('assets')
data_path   = Path('data')

image_types         = ('.png', '.jpeg', '.jpg', '.bmp')
font_types          = ('.ttf', '.otf')
font_sizes_original = (18, 24, 32, 48)

color_palette = 'sweetie-16'
color_hex_fp  = assets_path / f'colors/{color_palette}.hex'
color_map_fp  = assets_path / f'colors/{color_palette}.map'

initial_scene_name = 'Introduction Scene'
