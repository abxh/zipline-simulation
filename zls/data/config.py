import pygame as pg

from pathlib import Path

window_title     = 'Zipline Simulation'
window_icon_path = 'assets/images/zls-icon.png'
window_size      = (800, 600)
window_flags     = pg.RESIZABLE | pg.SCALED | pg.DOUBLEBUF
window_fps       = 60

# From parent directory:
assets_path   = Path('assets')
data_path     = Path('data')

image_types = ('.png', '.jpeg', '.jpg', '.bmp')
font_types  = ('.ttf', '.otf')
font_sizes  = (18, 24, 32, 48)

color_palette = 'sweetie-16'
hex_file_path = assets_path / f'colors/{color_palette}.hex'
map_file_path = assets_path / f'colors/{color_palette}.map'

initial_scene = 'Introduction Scene'


