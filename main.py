import Debugger
import printer
import performance

import colorama
import time

printTool = printer.printer()
fpsCounter = performance.fpsCounter()
WINDOW_SWITCH_DELAY = 0.5

if __name__ == "__main__":
    colorama.init()
    prev_mouse_pos = None
    prev_time = None
    prev_speed = 0
    prev_window_title = ""

    while True:
        printTool.clear()
        printTool.join(f"FPS: {fpsCounter.getFPS()}")
        prev_mouse_pos, prev_time, prev_speed, prev_window_title = Debugger.print_debug_info(prev_mouse_pos, prev_time, prev_speed, prev_window_title, printTool)
        fpsCounter.update()
        printTool.update()
        # time.sleep(0.5)
