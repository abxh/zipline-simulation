"""
The main module of the zipline simulation.

Simply run this module by running 'py .\zls.pyw' or double-click on it from windows.

It has following dependencies:
 - python 3.11.0
 - pygame 2.1.3.dev8
 - pygame-gui 0.6.6
 - pywin32 305
 - numpy 1.23.5
 - pandas 1.5.2
 - matplotlib 3.6.2
"""

import sys

import pygame as pg

from core.simulation import Simulation

if __name__ == "__main__":
    pg.init()
    Simulation().run()
    pg.quit()
    sys.exit()
