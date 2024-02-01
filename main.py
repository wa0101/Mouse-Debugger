import colorama
from multiprocessing import freeze_support
import Debugger
import performance
import printer
from lang import lang
import os

WINDOW_SWITCH_DELAY = 0.5
ALLOW_LAZY_COMPUTE = True


if __name__ == "__main__":
    debugUpdater = Debugger.debugUpdater(WINDOW_SWITCH_DELAY, ALLOW_LAZY_COMPUTE)
    fpsCounter = performance.fpsCounter()
    printTool = printer.printer()

    os.system(f"title {lang.title}")
    freeze_support()
    colorama.init()

    while True:
        printTool.clear()
        printTool.join(f"FPS: {fpsCounter.fps}      ")
        debugUpdater.print_debug_info(printTool)
        fpsCounter.update()
        printTool.update()
        debugUpdater.update()
