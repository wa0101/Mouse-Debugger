import win32api
import time
import numpy as np
from colorama import Fore, Style
import win32gui
import printer

def get_mouse_position():
    return win32api.GetCursorPos()


def get_mouse_speed(prev_pos, prev_time, cur_pos, cur_time):
    if prev_pos is None or prev_time is None:
        return 0
    distance = np.linalg.norm(np.array(cur_pos) - np.array(prev_pos))
    time_diff = cur_time - prev_time
    return distance / time_diff


def get_pixel_color(x, y):
    hdc = win32gui.GetDC(0)
    color = win32gui.GetPixel(hdc, x, y)
    win32gui.ReleaseDC(0, hdc)
    return color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF


def color_to_ansi(rgb):
    if rgb[0] > rgb[1] and rgb[0] > rgb[2]:
        return Fore.RED
    elif rgb[1] > rgb[0] and rgb[1] > rgb[2]:
        return Fore.GREEN
    elif rgb[2] > rgb[0] and rgb[2] > rgb[1]:
        return Fore.BLUE
    else:
        return Fore.WHITE


def print_debug_info(prev_mouse_pos, prev_time, prev_speed, prev_window_title, printTool: printer.printer):
    cur_mouse_pos = get_mouse_position()
    cur_time = time.time()

    mouse_speed = get_mouse_speed(prev_mouse_pos, prev_time, cur_mouse_pos, cur_time)
    mouse_color = get_pixel_color(cur_mouse_pos[0], cur_mouse_pos[1])
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    printTool.join(Style.BRIGHT + Fore.CYAN + f'WA Modern Console Debug Information' + Style.RESET_ALL)
    printTool.join(f'Mouse Position:')
    printTool.join(f'    X: {Fore.YELLOW}------> {cur_mouse_pos[0]}{Style.RESET_ALL}       ')
    printTool.join(f'    Y: {Fore.YELLOW}------> {cur_mouse_pos[1]}{Style.RESET_ALL}       ')
    printTool.join(f'Mouse Color: {color_to_ansi(mouse_color)}RGB({mouse_color[0]}, {mouse_color[1]}, {mouse_color[2]}){Style.RESET_ALL}      ')
    printTool.join(f'Mouse Speed: {mouse_speed:.2f} pixels per second                                    ')

    if mouse_speed == 0 and prev_speed == 0:
        printTool.join(f'Is Mouse Stopped: {Fore.RED}🛑 True{Style.RESET_ALL}  ')
    else:
        printTool.join(f'Is Mouse Stopped: {Fore.GREEN}✅ False{Style.RESET_ALL}')

    printTool.join(f'Mouse Sensitivity: {Fore.MAGENTA}Medium{Style.RESET_ALL}')

    printTool.join('\nColor Intensity:')
    printTool.join(f'    Red Intensity: {Fore.RED}🔴 {mouse_color[0]}{Style.RESET_ALL}     ')
    printTool.join(f'    Green Intensity: {Fore.GREEN}🟢 {mouse_color[1]}{Style.RESET_ALL}     ')
    printTool.join(f'    Blue Intensity: {Fore.BLUE}🔵 {mouse_color[2]}{Style.RESET_ALL}     ')

    printTool.join('\nWindow Information:')
    printTool.join(f'    Window Title: {window_title}                                       ')
    
    if window_title != prev_window_title:
        printTool.join(f'    {Fore.YELLOW}🔄 Window Changed!{Style.RESET_ALL}')
    else:
        printTool.join(f'    {Fore.YELLOW}                   {Style.RESET_ALL}')

    return cur_mouse_pos, cur_time, mouse_speed, window_title
