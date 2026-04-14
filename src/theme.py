import os
import sys
import tkinter as tk
from tkinter import ttk
from src.resource_utils import get_resource_path


def _set_taskbar_icon_win32(root, ico_path):
    """Force taskbar icon via Win32 API with full resolution."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        WM_SETICON = 0x0080
        ICON_BIG = 1
        icon_handle = ctypes.windll.user32.LoadImageW(
            0, ico_path, 1, 256, 256, 0x00000010  # LR_LOADFROMFILE
        )
        if icon_handle:
            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, icon_handle)
    except Exception:
        pass


def apply_theme(root, theme: str = "light") -> None:
    """
    Apply the ttk theme to the given Tk root window
    Looks for 'azure.tcl' in the same directory as this file
    https://github.com/rdbende/Azure-ttk-theme
    """
    icon_png = get_resource_path("configuration/icon.png")
    icon_ico = get_resource_path("configuration/icon.ico")

    if os.path.exists(icon_png):
        try:
            icon = tk.PhotoImage(file=icon_png)
            root.iconphoto(True, icon)
            root._icon_ref = icon
        except Exception as e:
            print(f"Icon error (png): {e}")

    if os.path.exists(icon_ico):
        root.after(50, lambda: _set_taskbar_icon_win32(root, icon_ico))

    here = os.path.dirname(os.path.abspath(__file__))
    theme_file = os.path.join(here, "azure.tcl")

    if os.path.exists(theme_file):
        root.tk.call("source", theme_file)
        root.tk.call("set_theme", theme)
    else:
        # fall back to a standard ttk theme
        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except Exception:
            pass