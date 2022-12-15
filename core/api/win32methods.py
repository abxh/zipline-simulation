import functools
import os

import pygame as pg
import win32con as w32c
import win32gui as w32g


class Win32Methods:
    """
    This class uses Win32 API to extend the pygame window's functionality.
    """

    supported = os.name == "nt"

    @staticmethod
    @functools.lru_cache
    def get_hwnd():
        """
        Returns
        -------
            bool
                The hardware handle of the window to be used by the Win32 API.
        """
        return pg.display.get_wm_info()["window"]

    @classmethod
    def get_minimized(cls) -> bool:
        """
        Returns
        -------
            bool
                Whether the window is minimized.
        """
        hWnd = cls.get_hwnd()
        return w32g.GetWindowPlacement(hWnd)[1] == w32c.SW_SHOWMINIMIZED

    @classmethod
    def get_maximized(cls) -> bool:
        """
        Returns
        -------
            bool
                Whether the window is minimized.
        """
        hWnd = cls.get_hwnd()
        return w32g.GetWindowPlacement(hWnd)[1] == w32c.SW_SHOWMAXIMIZED

    @classmethod
    def maximize(cls):
        """
        Maximize the window.
        """
        hWnd = cls.get_hwnd()
        w32g.ShowWindow(hWnd, w32c.SW_MAXIMIZE)

    @classmethod
    def minimize(cls):
        """
        Minimize the window.
        """
        hWnd = cls.get_hwnd()
        w32g.ShowWindow(hWnd, w32c.SW_MINIMIZE)

    @classmethod
    def restore_state(cls):
        """
        Restore the state of the window after it was maximized or minimized.
        """
        hWnd = cls.get_hwnd()
        w32g.ShowWindow(hWnd, w32c.SW_RESTORE)
