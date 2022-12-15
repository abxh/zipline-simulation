"""
The main module of the zipline simulation.

Simply run this module by running 'py .\zls.pyw' or double-click on it from windows.

Do be aware that it has following dependencies:
 - python 3.11.0
 - pygame 2.1.3.dev8
 - pygame-textinput 1.0.1
 - pywin32 305
 - numpy 1.23.5
 - pandas 1.5.2
 - matplotlib 3.6.2

A standalone binary executable can be found in the 'bin' directory.
"""
import os
import sys

import pygame as pg

from core.simulation import Simulation

# https://stackoverflow.com/questions/28033003/pyinstaller-with-pygame
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

if __name__ == "__main__":
    pg.init()
    Simulation().run()
    pg.quit()
    sys.exit()
