import win32api
import win32con
import time
import numpy as np
from colorama import Fore, Style, init
import win32gui
import os

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

def print_debug_info(prev_mouse_pos, prev_time, prev_speed, prev_window_title):
    cur_mouse_pos = get_mouse_position()
    cur_time = time.time()

    mouse_speed = get_mouse_speed(prev_mouse_pos, prev_time, cur_mouse_pos, cur_time)
    mouse_color = get_pixel_color(cur_mouse_pos[0], cur_mouse_pos[1])
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    os.system('cls')
    print(Style.BRIGHT + Fore.CYAN + f'WA Modern Console Debug Information' + Style.RESET_ALL)
    print(f'Mouse Position:')
    print(f'    X: {Fore.YELLOW}------> {cur_mouse_pos[0]}{Style.RESET_ALL}')
    print(f'    Y: {Fore.YELLOW}------> {cur_mouse_pos[1]}{Style.RESET_ALL}')
    print(f'Mouse Color: {color_to_ansi(mouse_color)}RGB({mouse_color[0]}, {mouse_color[1]}, {mouse_color[2]}){Style.RESET_ALL}')
    print(f'Mouse Speed: {mouse_speed:.2f} pixels per second')

    if mouse_speed == 0 and prev_speed == 0:
        print(f'Is Mouse Stopped: {Fore.RED}🛑 True{Style.RESET_ALL}')
    else:
        print(f'Is Mouse Stopped: {Fore.GREEN}✅ False{Style.RESET_ALL}')

    print(f'Mouse Sensitivity: {Fore.MAGENTA}Medium{Style.RESET_ALL}')

    print('\nColor Intensity:')
    print(f'    Red Intensity: {Fore.RED}🔴 {mouse_color[0]}{Style.RESET_ALL}')
    print(f'    Green Intensity: {Fore.GREEN}🟢 {mouse_color[1]}{Style.RESET_ALL}')
    print(f'    Blue Intensity: {Fore.BLUE}🔵 {mouse_color[2]}{Style.RESET_ALL}')

    print('\nWindow Information:')
    print(f'    Window Title: {window_title}')
    
    if window_title != prev_window_title:
        print(f'    {Fore.YELLOW}🔄 Window Changed!{Style.RESET_ALL}')

    return cur_mouse_pos, cur_time, mouse_speed, window_title

if __name__ == "__main__":
    init()
    prev_mouse_pos = None
    prev_time = None
    prev_speed = 0
    prev_window_title = ""

    while True:
        prev_mouse_pos, prev_time, prev_speed, prev_window_title = print_debug_info(prev_mouse_pos, prev_time, prev_speed, prev_window_title)
        time.sleep(0.5) 
