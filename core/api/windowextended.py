import pygame as pg

from core.api.eventmanager import EventManager, event_handler
from core.api.renderer import Renderer
from core.api.window import Window


class WindowExtended(Window):
    """
    This class extends the `Window` class with functionality for the main loop.

    Additionally, as a singleton class, it can be invoked and be accessed such so
    the same instance is returned whenever it's constructor is called. Also it's
    constructor is only called once.

    Attributes
    ----------
        dt : float
            The time between iterations of the main loop in seconds.

        eventmanager : EventManager
            The window's event manager responsible for handling events.

        fps : int
            An integer describing the number of iterations the main loop is being
            run each second. In turn describes the number of frames being rendered
            each second.

        flags : int
            An integer describing the display type(s). Multiple types can be
            combined using the bitwise operator `|`. A list of relevant types
            are as following (from the documentation):

        - pygame.FULLSCREEN     create a fullscreen display
        - pygame.RESIZABLE      display window should be sizeable
        - pygame.NOFRAME        display window will have no border or controls
        - pygame.SCALED         resolution depends on desktop size and scale graphics
        - pygame.SHOWN          window is opened in visible mode (default)
        - pygame.HIDDEN         window is opened in hidden mode

        icon : pygame.Surface
            The pygame Surface object used as the window's icon.

        max_fps : int
            The maximum number of iterations each second to keep the main loop around.
            In turn controls how many frames, the renderer will render each second.

        renderer : Renderer
            The window's renderer responsible for managing drawing tasks.

        running : bool
            A boolean describing whether the main loop is running. Can be set
            to false to exit the main loop. Otherwise the `exit` method can be
            used for the same purpose.

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
        max_fps: int,
    ):
        """
        Initialize this class.

        Parameters
        ----------
            title : str
                The title of the window.
            flags : int
                The display type(s). Multiple types can be combined using the
                bitwise operator `|`. A list of relevant types are as following
                (from the documentation):

            - pygame.FULLSCREEN    create a fullscreen display
            - pygame.RESIZABLE     display window should be sizeable
            - pygame.NOFRAME       display window will have no border or controls
            - pygame.SCALED        resolution depends on desktop size and scale graphics
            - pygame.SHOWN         window is opened in visible mode (default)
            - pygame.HIDDEN        window is opened in hidden mode

            icon : pygame.Surface
                The window's icon.

            size : numpy.typing.ArrayLike
                The size of the window.

            max_fps : int
                The window's maximum framerate.
        """
        super().__init__(title, icon, size, flags)

        self._clock = pg.time.Clock()
        self.eventmanager = EventManager(self)
        self.renderer = Renderer(self, self.eventmanager)

        self.dt = 0.0
        self.fps = 0
        self.max_fps = max_fps
        self.running = False

        @event_handler(type=pg.QUIT)
        def on_quit(w: WindowExtended):
            w.running = False

        self.eventmanager.add_handler(on_quit, w=self)

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
