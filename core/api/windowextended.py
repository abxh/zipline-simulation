import pygame as pg
from pygame.time import Clock

from core.api.eventmanager import EventManager, event_handler
from core.api.renderer import Renderer
from core.api.window import Window


class WindowExtended(Window):
    """
    This class extends the Window class with functionality for the 'main loop'.

    Attributes
    ----------
        dt : float
            The time between iterations of the main loop in seconds.
        eventmanager : EventManager
            The window's event manager responsible for handling events.
        flags : int
            The pygame flag to start the window with.
        fps : int
            The number of iterations of the main loop being run each second.
        icon : Surface
            The pygame surface used as the window's icon.
        max_fps : int
            The maximum number of iterations each second to keep the main loop around.
        renderer : Renderer
            The window's renderer responsible for drawing stuff to the screen.
        running : bool
            Whether the main loop is running.
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
        max_fps: int,
    ):
        """
        Initialize this class.

        Parameters
        ----------
            title : str
                The title or caption of the window.
            icon : Surface
                The pygame surface used as the window's icon.
            size : ArrayLike
                The size of the window.
            flags : int
                The pygame flag to start the window with.
            max_fps : int
                The maximum framerate to hold the window around approximately.
        """
        super().__init__(title, icon, size, flags)

        self._clock = Clock()
        self.eventmanager = EventManager()
        self.renderer = Renderer()

        self.dt = 0.0
        self.fps = 0
        self.max_fps = max_fps
        self.running = False

        @event_handler(type=pg.QUIT)
        def on_quit(window):
            window.running = False

        self.eventmanager.add_handler(on_quit, window=self)

    def run(self):
        """
        Run the main loop.
        """
        self.running = True
        while self.running:
            self.dt = self._clock.get_time() / 1000  # in seconds
            self.fps = round(self._clock.get_fps())  # in whole numbers.

            self.eventmanager._update()
            self.loop_method()
            self.renderer._update()

            self._clock.tick(self.max_fps)  # delay the main loop.

    def exit(self):
        """
        Exit the main loop in the next iteration of the main loop.
        """
        self.running = False

    def loop_method(self):
        """
        The additional method to be called in each iteration of the main loop.

        This method is meant to be inherited to add additional functionality
        to the main loop.

        Raises
        ------
            NotImplementedError
                If the method has not been inherited and made such so the `super`
                method is not called.
        """
        raise NotImplementedError
