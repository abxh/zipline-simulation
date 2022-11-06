import pygame as pg

from pathlib import Path
from pygame import Surface
from pygame.font import Font
from pygame.color import Color
from zls.data.types.scene import Scene

from zls.data.scenes.introscene import introscene


def set_display_mode(
    size: tuple[int, int],
    flags: int = pg.NOEVENT,
    title: str = None,
    icon_path: str = None,

) -> pg.Surface:
    """
    This function is a overlay function to pygame.display.set_mode.
    It contains additional arguments for title and icon path of the window.

    Args:
        flags (int, optional):           Defaults to pygame.NOEVENT.
        size (tuple[int,int], optional): Defaults to None.
        title (str, optional):           Defaults to None.
        icon_path (str, optional):       Defaults to None.

    Returns:
        pygame.Surface: The window surface.
    """

    if title:
        pg.display.set_caption(title)

    if icon_path:
        icon_surface = pg.image.load(icon_path)
        pg.display.set_icon(icon_surface)

    return pg.display.set_mode(size, flags)


def get_image_dict(path: Path, types: tuple[str]) -> dict[str, Surface]:
    """
    A function to recursively search for images in a given path.

    Note:
        Image names must be unique, no matter the image type/extension.

    Args:
        path (Path): The path to be used to search for.
        types (tuple[str]): The types of images to search for.

    Returns:
        dict[str, Surface]: A dictionary of images with their name as keys and
        pygame surfaces as values.
    """
    d = {}
    for t in types:
        for fp in path.rglob(f'*{t}'):
            d[fp.stem] = pg.image.load(fp).convert_alpha()
    return d


def get_font_dict(path: Path, types: tuple[str],
                  sizes: tuple[int]) -> dict[str, Surface]:
    """
    A function to recursively search for fonts in a given path.

    Note:
        Font names must be unique, no matter the image type/extension.

        Fonts with different sizes have a key like so: '<font name> <size>'.

        For example, a font with the name 'Arial' and sizes (16,32) will make
        the function return a dictionary with keys 'Arial 16' and 'Arial 32'
        with the respective pygame surfaces as keys.


    Args:
        path (Path): The path to be used to search for.
        types (tuple[str]): The types of fonts to search for.
        sizes (tuple[int]): The sizes of fonts to load the font with.

    Returns:
        dict[str, Surface]: A dictionary of fonts with their '<name> <size>'
        as keys and pygame surfaces as values.
    """
    d = {}
    for t in types:
        for fp in path.rglob(f'*{t}'):
            for size in sizes:
                d[f'{fp.stem} {str(size)}'] = Font(fp, size)
    return d


def get_color_dict(hex_file_path: Path, map_file_path: Path) -> dict[str, Color]:
    """
    A function to get the colors from a hex file and a custom defined map file.

    Note:
        The color names in each line of the map file must correspond to the
        colors in the hex file.

    Args:
        hex_file_path (Path): the path of the hex file.
        map_file_path (Path): the path of the map file.

    Returns:
        dict[str, Color]: A dictionary of colors with their names as keys and
        their pygame colors as values.
    """
    color_dict = {}
    with open(hex_file_path) as hf, open(map_file_path) as mf:
        mapping = [l.strip() for l in mf]
        for i, l in enumerate(hf):
            hex_val = l.strip()
            rgb_val = tuple(
                int(hex_val[j:j+2], 16) for j in (0, 2, 4)
            )
            color_dict[mapping[i]] = Color(*rgb_val)
    return color_dict


def get_scene_dict() -> dict[str, Scene]:
    """
    A function to get the scenes in the scenes module.

    Returns:
        dict[str, Scene]: A dictionary of scenes with their names as keys and
        themselves as values.
    """
    d = {}
    d[introscene.name] = introscene
    
    return d

