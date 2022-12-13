import os
from functools import partial
from typing import Callable

import win32con as w32c
import win32gui as w32g


class Win32Methods:
    """
    This class contains static methods used to control the window using the
    Win32 API to extend the pygame window's functionality.

    Note
    ----
    The methods in this class only work in windows-based OS'es. One can check
    whether they are supported through the `get_supported` method.
    """

    @staticmethod
    def _call_while_resize(resize_callback: Callable | partial) -> None:
        """
        Call a function while the window is being resized i.e. the window borders
        are being dragged.

        This method is used to overcome a bug described in:
        https://github.com/libsdl-org/SDL/issues/1059

        Parameters
        ----------
            resize_callback : Callable | partial
                The function to call while the window is being resized. One can
                use partial functions to pass frozen arguments and keyword
                arguments to be used, when the function is called.
        """
        # Source for following code:
        # https://stackoverflow.com/questions/64543449/update-during-resize-in-pygame

        hWnd = w32g.GetForegroundWindow()

        def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
            if message == w32c.WM_SIZE:
                draw_callback()
                w32g.RedrawWindow(
                    hWnd, None, None, w32c.RDW_INVALIDATE | w32c.RDW_ERASE
                )
            return w32g.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

        oldWndProc = w32g.SetWindowLong(
            hWnd,
            w32c.GWL_WNDPROC,
            lambda *args: wndProc(oldWndProc, resize_callback, *args),
        )

    @staticmethod
    def get_minimized() -> bool:
        """
        Returns
        -------
            bool
                Whether the window is minimized.
        """
        hWnd = w32g.GetForegroundWindow()
        return w32g.GetWindowPlacement(hWnd)[1] == w32c.SW_SHOWMINIMIZED

    @staticmethod
    def get_maximized() -> bool:
        """
        Returns
        -------
            bool
                Whether the window is minimized.
        """
        hWnd = w32g.GetForegroundWindow()
        return w32g.GetWindowPlacement(hWnd)[1] == w32c.SW_SHOWMAXIMIZED

    @staticmethod
    def get_supported() -> bool:
        """
        Returns
        -------
            bool
                Whether the methods in this class are supported.
        """
        return os.name == "nt"

    @staticmethod
    def maximize():
        """
        Maximize the window.
        """
        hWnd = w32g.GetForegroundWindow()
        w32g.ShowWindow(hWnd, w32c.SW_MAXIMIZE)

    @staticmethod
    def minimize():
        """
        Minimize the window.
        """
        hWnd = w32g.GetForegroundWindow()
        w32g.ShowWindow(hWnd, w32c.SW_MINIMIZE)

    @staticmethod
    def restore_state():
        """
        Restore the state of the window from being minimized or maximized.
        """
        hWnd = w32g.GetForegroundWindow()
        w32g.ShowWindow(hWnd, w32c.SW_RESTORE)
