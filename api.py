from dataclasses import dataclass
from typing import Union

import numpy as np
import win32api
import win32gui
from colorama import Fore

np.seterr(divide='ignore', invalid='ignore')


@dataclass
class MouseInfo:
    """
    (still in test)
    MouseInfo dataclass for storing mouse information.
    inherit this dataclass for using.
    """
    pos: tuple[int, int]
    color: tuple[int, int, int]
    speed: float
    isStopped: bool
    currentWindow: int
    currentWindowTitle: str


def color_to_ansi(color: tuple[int, int, int]) -> str:
    """
    get the text of this color.
    :param color: color (Red, Green, Blue)
    :return: RED/GREEN/BLUE/BLACK/WHITE
    """
    if color[0] > color[1] and color[0] > color[2]:
        return Fore.RED
    elif color[1] > color[0] and color[1] > color[2]:
        return Fore.GREEN
    elif color[2] > color[0] and color[2] > color[1]:
        return Fore.BLUE
    else:
        return Fore.WHITE


def get_pixel_color(pos: tuple[int, int]) -> tuple[int, int, int]:
    """
    get current pixel RGB color.
    :param pos: current mouse position. (pos_x, pos_y)
    :return: pixel color (Red, Green, Blue)
    """
    hdc = win32gui.GetDC(0)
    color = win32gui.GetPixel(hdc, pos[0], pos[1])
    win32gui.ReleaseDC(0, hdc)
    return color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF


def get_mouse_speed(prev_pos: Union[tuple[int, int], None], prev_time: Union[float, None],
                    cur_pos: tuple[int, int], cur_time: float, numpy: bool = True) -> float:
    """
    get the mouse speed from previous position and time to current position and time.
    :param prev_pos: previous mouse position. (pos_x, pos_y)
    :param prev_time: previous time.
    :param cur_pos: current mouse position. (pos_x, pos_y)
    :param cur_time: current time.
    :param numpy: compute with numpy.
    :return: mouse speed.
    """
    if prev_pos is None or prev_time is None:
        return 0
    if numpy:
        distance = np.linalg.norm(np.array(cur_pos) - np.array(prev_pos))
    else:
        distance = ((cur_pos[0] - prev_pos[0]) ** 2 + (cur_pos[1] - prev_pos[1]) ** 2) ** 0.5
    time_diff = cur_time - prev_time
    try:
        return distance / time_diff
    except ZeroDivisionError:
        return np.nan


def get_mouse_position() -> tuple[int, int]:
    return win32api.GetCursorPos()


def get_window_title(window: int = None) -> str:
    return win32gui.GetWindowText(window)
