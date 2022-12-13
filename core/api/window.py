import numpy as np
import numpy.typing as npt
import pygame as pg

from core.api._singletontype import SingletonType


class Window(metaclass=SingletonType):
    """
    This class abstracts the pygame window.

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
        pg.display.set_mode(*params)

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value: int):
        self._flags = value
        self._set_new_mode(flags=value)

    @property
    def icon(self):
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
