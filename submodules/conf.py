import numpy as np
import pygame.locals as pl


WIN_TITLE   = 'Zipline Simulation'
WIN_SIZE    = (800, 600)
WIN_FLAGS   = pl.RESIZABLE
WIN_ICON_FP = 'assets/images/zls-icon.png'

ASSETS_PATH              = 'assets/'
IMAGE_FILE_TYPES         = ('.png', '.jpg', '.jpeg', '.bmp')
FONT_FILE_TYPES          = ('.ttf', '.otf')
COLOR_PALETTE_FILE_TYPES = ('.hex', '.map')

COLOR_PALETTE_NAME = 'sweetie-16'

FONT_SIZES = np.array([18, 32, 48])