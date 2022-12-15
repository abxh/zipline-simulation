import numpy as np
import numpy.typing as npt
import pygame as pg

from core.api._singletontype import SingletonType


class Window(metaclass=SingletonType):
    """
    This class provides a basic abstraction of the pygame window.

    It stores the icon and flags internally, but otherwise uses pygame's own
    `display` module to set and get attributes.
    
    Additionally, as a singleton class, it is only initialized once, so the
    flags and icon are saved until all references to this class are deleted.

    Attributes
    ----------
        flags : int
            An integer describing the display type(s). Multiple types can be
            combined using the bitwise operator `|`. A list of relevant types
            are as following (from the documentation):

        - pygame.FULLSCREEN    create a fullscreen display
        - pygame.RESIZABLE     display window should be sizeable
        - pygame.NOFRAME       display window will have no border or controls
        - pygame.SCALED        resolution depends on desktop size and scale graphics
        - pygame.SHOWN         window is opened in visible mode (default)
        - pygame.HIDDEN        window is opened in hidden mode

        icon : pygame.Surface
            The pygame Surface object used as the window's icon.

        size : numpy.typing.ArrayLike
            An integer array of size 2 describing the size of the window.

        title : str
            A string describing the title of the window.
    """

    def __init__(
        self,
        title: str,
        icon: pg.Surface,
        size: tuple[int, int],
        flags: int,
    ):
        """
        Initialize the window.

        Attributes
        ----------
            flags : int
                The pygame flag to start the window with.
            icon : Surface
                The pygame surface used as the window's icon.
            size : ArrayLike
                The size of the window.
            title : str
                The title or caption of the window.
        """
        self.title = title
        self.icon = icon
        self._flags = flags  # store flags internally.

        # Start window and set size and flags.
        pg.display.set_mode(size, flags)

    def _set_new_mode(self, **kwargs):
        """
        Start the window in a new mode with previous arguments.

        Keywords
        --------
            size : ArrayLike
                Overwrite previous window size.
            flags : int
                Overwrite previous window flags.

        Other keyword-arguments are used as parameters for `pygame.display.set_mode`.
        """
        params = {"size": self.size, "flags": self.flags}
        for k, v in kwargs.items():
            if k in params:
                params[k] = v
        pg.display.set_mode(**params)

    @property
    def flags(self) -> int:
        return self._flags

    @flags.setter
    def flags(self, value: int):
        self._flags = value
        self._set_new_mode(flags=value)

    @property
    def icon(self) -> pg.Surface:
        return self._icon

    @icon.setter
    def icon(self, value: pg.Surface):
        self._icon = value
        pg.display.set_icon(value)

    @property
    def size(self) -> npt.ArrayLike:
        return np.array(pg.display.get_window_size())

    @size.setter
    def size(self, value):
        self._set_new_mode(size=value)

    @property
    def title(self):
        return pg.display.get_caption()[0]

    @title.setter
    def title(self, value):
        pg.display.set_caption(value)
