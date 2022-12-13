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
    This class manages events.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, Callable] = {}
        self._id_count = count()
        self._id_to_remove: deque[int] = deque()

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
        # Create a collection of clones of the handlers.
        handlers = self._handlers.values()

        for event in pg.event.get():
            # Filter handlers that return True i.e. they have found the event
            # they were listening to.
            handlers = [handler for handler in handlers if not handler(event)]

        if self._id_to_remove:  # If not empty.
            # Remove any events to be removed.
            for id in self._id_to_remove:
                del self._handlers[id]
