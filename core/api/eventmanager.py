from collections import deque
from functools import partial, wraps
from itertools import count
from typing import Callable

import pygame as pg

from core.api._singletontype import SingletonType


def event_handler(type: int, pass_event=False):
    """
    Decorate a function and convert it into a event handler.

    Parameters
    ----------
        type : int
            The pygame event type to listen to.
        pass_event : bool, default `False`
            Whether to pass the event to the function.

    Note
    ----
    If pass_event is set to `True`, then following conditions must apply:
    - The event is the first parameter to the function.
    - Other parameters are passed as keyword-arguments.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(event, **kwargs):
            correct_type = event.type == type
            if correct_type:
                if pass_event:
                    function(event, **kwargs)
                else:
                    function(**kwargs)
            return correct_type

        return wrapper

    return decorator


class EventManager(metaclass=SingletonType):
    """
    This class provides a centralised way of managing pygame events.

    Additionally, as a singleton class, it can be invoked anywhere in the code to
    create event handlers.

    Attributes
    ----------
        events : list[pygame.event.Event]
            The events pumped from pygame in the current iteration.
    """

    def __init__(self, window) -> None:
        self._window = window
        self._handlers: dict[str, Callable] = {}
        self._id_count = count()
        self._id_to_remove: deque[int] = deque()
        self.events: list[pg.event.Event] = []

    def add_new_handler(self, func, type, pass_event=False, **kwargs):
        """
        Convert a function to a handler and add it.

        Parameters
        ----------
            func : Callable
                The function to be decorated by `event_handler`.
            type : int
                The pygame event type for the function to listen to.
            pass_event : bool, default False
                Whether to pass the event to the function, when the event it
                was listening to is found, as the function's first parameter.

        Additional keyword-arguments can be passed, which will be passed to the
        function.

        Returns
        -------
            int
                The id of the event handler, which can be used to remove it.
        """
        handler = event_handler(type, pass_event)(func)
        return self.add_handler(handler, **kwargs)

    def add_handler(self, handlers, **kwargs):
        """
        Add a event handler to be used.

        Parameters
        ----------
            handler : Callable
                The function decorated by `event_handler` to call.

        Additional keyword-arguments can be passed, which will be passed to the
        event handler.

        Returns
        -------
            int
                The id of the event handler, which can be used to remove it.
        """
        id = next(self._id_count)
        self._handlers[id] = partial(handlers, **kwargs)
        return id

    def remove_handler(self, id):
        """
        Remove a event handler by it's id.

        Parameters
        ----------
            id : int
                The id of the event handler to be removed.
        """
        # Using a additional deque that events can remove themselves from
        # themselves.
        self._id_to_remove.append(id)

    def _update(self):
        """
        Update the event manager.
        """
        self.events = pg.event.get()

        # Create a clone of the collection of handlers.
        handlers = self._handlers.values()

        for event in self.events:
            # Filter handlers that return True i.e. they have found the event
            # they were listening to.
            handlers = [handler for handler in handlers if not handler(event)]

        # Check if queue is not empty.
        if self._id_to_remove:
            # Remove any events to be removed.
            for id in self._id_to_remove:
                # by iterating through the queue, the elements in the queue are
                # also removed.
                del self._handlers[id]
