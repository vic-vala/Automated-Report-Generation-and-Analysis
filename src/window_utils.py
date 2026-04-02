"""
Helpers for DPI-aware tkinter window sizing on Windows.

Call `enable_dpi_awareness()` once before creating any Tk root.
Call `fit_window_to_screen(root, width, height)` after root creation
to request a size that's clamped to the available screen area.
"""

import sys


def enable_dpi_awareness() -> None:
    """
    Tell Windows this process handles DPI itself so tkinter
    reports real pixel dimensions instead of scaled-down values.
    Should have no effect on non-Windows platforms (yell at Joey if this isn't the case)
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes
        # Per-monitor V2 (Win10 1703+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def fit_window_to_screen(root, desired_w: int, desired_h: int, pad: int = 40) -> None:
    """
    Set window geometry clamped to available screen size.
    If the desired size exceeds the screen in either dimension,
    the window is maximized instead.

    Args:
        root:       Tk root window (must already exist)
        desired_w:  requested width in pixels
        desired_h:  requested height in pixels
        pad:        margin to leave around edges (accounts for taskbar, etc.)
    """
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    usable_w = screen_w - pad
    usable_h = screen_h - pad

    if desired_w > usable_w or desired_h > usable_h:
        # Window won't fit — maximize
        try:
            root.state("zoomed")  # Windows / some Linux WMs
        except Exception:
            root.attributes("-fullscreen", False)
            root.geometry(f"{usable_w}x{usable_h}+0+0")
    else:
        # Center the window
        x = max(0, (screen_w - desired_w) // 2)
        y = max(0, (screen_h - desired_h) // 2)
        root.geometry(f"{desired_w}x{desired_h}+{x}+{y}")
