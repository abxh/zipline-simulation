import sys

import pygame as pg

from core.simulation import Simulation

if __name__ == "__main__":
    pg.init()
    Simulation().run()
    pg.quit()
    sys.exit()
