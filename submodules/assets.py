"""
This module contains the following classes:
    (1) ColorPalette: A named tuple meant to store the paths to the relevant
    files to a given color palette.
    
    (2) Assets: A class with class attributes and methods meant to
    respectively store and interact with the assets.

The Assets class designed as such, so it is agnostic to the names of folders
containing the assets and the directory structure of the assets. It's only
requirements are:
    (1) Files with the same type of suffixes has unique names. For example,
    two fonts with different suffix (i.e. '.otf' and '.ttf') are still
    required to have different stems (names without suffixes).
    
    (2) Both the hex and the map file to a given color palette lies in the
    same folder and has the same stem (name without suffix).
"""

from pathlib import Path
from typing import NamedTuple

import pygame as pg
import numpy as np

from pygame import Surface
from pygame.color import Color
from pygame.font import Font
from numpy import ndarray


class ColorPalette(NamedTuple):
    """
    This named tuple should contain two values:
        (1) map_file_path: The path to the custom defined map file containing
        the mapped names of the colors.
        (2) hex_file_path: The path to the hex file containing the colors.
    """
    map_file_path : Path
    hex_file_path : Path

class Assets():
    """
    The Assets class contains the assets in the from of class attributes.
    
    The class attributes containing the paths to the assets are as following:
        (1) image_paths (dict[str, Path])
        (2) font_paths (dict[str, Path])
        (3) color_palettes (dict[str, ColorPalette])
    
    Their keys are decided by the file path stem (i.e. file name without the
    suffix).
    
    The attributes containing the assets themselves are as following:
        images (dict[str, Surface]), where the key is the image file name
        without suffix.
        
        fonts (dict[str, Font], where the key is the font file name without
        suffix and the size of the font seperated by a single space.
        
        colors (dict[str, Color]), where the key is the mapped color name of
        the color.
    
    Note for colors dictionary:    
        The mapped color names are retrieved from the map file, and the colors
        are retrieved from the hex file, and each line from the map file are
        mapped as the color name to the corresponding line in the hex file.
    
    It further contains following class methods:
        (1) load_paths: load all asset paths.
        (2) load_images: load all images.
        (4) load_fonts: load all fonts with given size.
        
        (5) _load_font: load a individual font with a given path and size.
        (6) _load_image: load a individual image with a given path.
        (7) _load_colors: load colors from a given hex and map file path.
    
    Note:
        (1) The load methods purposefully does not clear the dictionaries.
        This is to allow both adding to and replacing the respective
        dictionaries as needed.
    """
    image_paths    : dict[str, Path]         = {}
    font_paths     : dict[str, Path]         = {}
    color_palettes : dict[str, ColorPalette] = {}
    
    images : dict[str, Surface] = {}
    fonts  : dict[str, Font]    = {}
    colors : dict[str, Color]   = {}
    
    font_sizes_scaled : ndarray = np.zeros([0], np.int8)
    font_sizes_all    : ndarray = np.array([0], np.int8)
    
    @classmethod
    def load_paths(cls,
                     assets_path: str,
                     image_file_types: tuple[str],
                     font_file_types: tuple[str],
                     color_palette_file_types: tuple[str]):
        
        for file_path in Path(assets_path).rglob('*.*'):
            if file_path.suffix in image_file_types:
                cls.image_paths[file_path.stem] = file_path
                
            elif file_path.suffix in font_file_types:
                cls.font_paths[file_path.stem] = file_path
                
            elif file_path.stem not in cls.color_palettes.keys():
                if file_path.suffix in color_palette_file_types:
                    name        = file_path.stem
                    parent_path = file_path.parent
                    
                    cls.color_palettes[name] = ColorPalette(
                        hex_file_path = parent_path / f'{name}.hex',
                        map_file_path = parent_path / f'{name}.map')
    
    @classmethod
    def load_images(cls):
        for image_path in cls.image_paths.values():
            cls._load_image(image_path)

    @classmethod
    def load_fonts(cls, new_font_sizes: ndarray[int]):
        # The following code memoizes the fonts with the given sizes. This
        # prevents reloading a font with a size, that has already been loaded.
        
        cls.font_sizes_scaled = new_font_sizes
        
        unique_sizes = np.setdiff1d(new_font_sizes, cls.font_sizes_all)
        cls.font_sizes_all = np.append(cls.font_sizes_all, unique_sizes)
        
        if unique_sizes.size > 0:
            for font_path in cls.font_paths.values():
                cls._load_font(font_path, unique_sizes)
    
    @classmethod
    def load_color_palette(cls, color_palette_name: str):
        color_palette = cls.color_palettes[color_palette_name]
        cls._load_colors(
            map_file_path = color_palette.map_file_path,
            hex_file_path = color_palette.hex_file_path)
    
    @classmethod
    def _load_font(cls, file_path: Path, font_sizes: tuple[int]):
        for size in font_sizes:
            cls.fonts[f'{file_path.stem} {size}'] = Font(file_path, size)
    
    @classmethod
    def _load_image(cls, file_path: Path):
        cls.images[file_path.stem] = pg.image.load(file_path).convert_alpha()
        
    @classmethod
    def _load_colors(cls, map_file_path: Path, hex_file_path: Path):
        with open(map_file_path) as map_file:
            color_map = tuple(line.strip() for line in map_file)
            
        with open(hex_file_path) as hex_file:
            for i, line in enumerate(hex_file):
                hex_color = line.strip()
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
                cls.colors[color_map[i]] = Color(*rgb_color)
