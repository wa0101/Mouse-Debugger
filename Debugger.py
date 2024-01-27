from colorama import Fore, Style
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Union, Any
import win32gui
import time
import printer
import api


class lazyColorCompute:
    """
    test feature.
    lazy compute color in another process pool.
    """
    _process: Union[Process, None]
    _resultQueue: Queue
    _argQueue: Queue
    isRunning: bool
    func: Any
    lastResult: Any
    maxDelay: int

    def __init__(self, default_result=None, max_delay: int = 10):
        """
        initialize this lazyCompute.
        :param default_result: default result if function is not running.
        :param max_delay: max delay of the color compute. (tick)
        :return: None.
        """
        self.func = api.get_pixel_color
        self.maxDelay = max_delay
        self._argQueue = Queue(maxsize=self.maxDelay)
        self._resultQueue = Queue(1)
        self._process = Process(target=self._compute, args=(self.func,), name="Lazy Color Compute")
        self.isRunning = True
        self.lastResult = default_result

    def start(self):
        self._process.start()

    def _compute(self, func):
        while self.isRunning:
            self._resultQueue.put(func(self._argQueue.get()))

    def stop(self):
        self.isRunning = False
        self._process.terminate()

    def postArgs(self, args):
        if self._argQueue.qsize() < self.maxDelay:
            self._argQueue.put(args)

    def getResult(self):
        if self._resultQueue.qsize() != 0:
            self.lastResult = self._resultQueue.get()
        return self.lastResult


class debugUpdater:
    """
    DebugUpdater class constructor.
    """
    prevPos: Union[tuple[int, int], None]
    prevTime: Union[float, None]
    prevSpeed: float
    prevColor: Union[tuple[int, int, int], None]
    prevWindow: Union[int, None]
    prevWindowTitle: Union[str, None]

    curPos: tuple[int, int]
    curTime: float
    curSpeed: float
    curColor: tuple[int, int, int]
    curWindow: int
    curWindowTitle: str

    isMoved: bool
    isWindowChanged: bool
    WINDOW_SWITCH_DELAY: float

    __windowChangedKeeperExecutor: ThreadPoolExecutor
    __windowChangedKeeperFuture: Future
    __isKeepWindowChanged: bool

    __LazyComputeColor: lazyColorCompute

    def __init__(self, window_switch_delay: float = 0.5,
                 allow_lazy_compute: bool = False,
                 prev_pos: Union[tuple[int, int], None] = None,
                 prev_time: Union[float, None] = None,
                 prev_speed: float = 0,
                 prev_color: Union[tuple[int, int, int], None] = None,
                 prev_window: Union[int, None] = None,
                 prev_window_title: Union[str, None] = None):
        self.WINDOW_SWITCH_DELAY = window_switch_delay
        self.ALLOW_LAZY_COMPUTE = allow_lazy_compute
        self.curPos = prev_pos
        self.curTime = prev_time
        self.curSpeed = prev_speed
        self.curColor = prev_color
        self.curWindow = prev_window
        self.curWindowTitle = prev_window_title
        self.isMoved = False
        self.isWindowChanged = False

        self.__windowChangedKeeperExecutor = ThreadPoolExecutor(max_workers=1,
                                                                thread_name_prefix='WindowChangedKeeper')
        self.__windowChangedKeeperFuture = self.__windowChangedKeeperExecutor.submit(self.__window_changed_keeper)
        if self.ALLOW_LAZY_COMPUTE:
            self.__LazyComputeColor = lazyColorCompute((0, 0, 0))
            self.__LazyComputeColor.postArgs((0, 0))
            self.__LazyComputeColor.start()
        self.update()

    def update(self):
        self.prevPos = self.curPos
        self.prevTime = self.curTime
        self.prevSpeed = self.curSpeed
        self.prevColor = self.curColor
        self.prevWindow = self.curWindow
        self.prevWindowTitle = self.curWindowTitle

        self.curPos = api.get_mouse_position()
        self.curTime = time.time()
        self.curSpeed = api.get_mouse_speed(self.prevPos, self.prevTime, self.curPos, self.curTime, numpy=False)
        if not self.ALLOW_LAZY_COMPUTE:
            self.curColor = api.get_pixel_color(self.curPos)
        else:
            self.__LazyComputeColor.postArgs(self.curPos)
            self.curColor = self.__LazyComputeColor.getResult()
        self.curWindow = win32gui.GetForegroundWindow()
        self.curWindowTitle = api.get_window_title(self.curWindow)

        self.isMoved = True if self.curPos != self.prevPos else False
        if self.curWindowTitle == self.prevWindowTitle:
            self.isWindowChanged = False
        else:
            self.isWindowChanged = True
            self.__windowChangedKeeperFuture.cancel()
            self.__windowChangedKeeperFuture = self.__windowChangedKeeperExecutor.submit(self.__window_changed_keeper)

    def updateAPI(self, api_data: api.MouseInfo):
        """
        (still in test)
        Updates the current state of the mouse and the window to api.
        :return: none
        """
        api_data.pos = self.curPos
        api_data.color = self.curColor
        api_data.speed = self.curSpeed
        api_data.isStopped = self.isMoved
        api_data.currentWindow = self.curWindow
        api_data.currentWindowTitle = self.curWindowTitle

    def __window_changed_keeper(self):
        """
        Keeps track of the window changes.
        :return:
        """
        self.__isKeepWindowChanged = True
        time.sleep(self.WINDOW_SWITCH_DELAY)
        self.__isKeepWindowChanged = False

    def print_debug_info(self, print_tool: printer.printer):
        """
        Prints debug info to the console.
        :return: none
        """
        print_tool.join(Style.BRIGHT + Fore.CYAN + f'WA Modern Console Debug Information' + Style.RESET_ALL)
        print_tool.join(f'Mouse Position:')
        print_tool.join(f'    X: {Fore.YELLOW}------> {self.curPos[0]}{Style.RESET_ALL}       ')
        print_tool.join(f'    Y: {Fore.YELLOW}------> {self.curPos[1]}{Style.RESET_ALL}       ')
        print_tool.join(
            f'Mouse Color: {api.color_to_ansi(self.curColor)}'
            f'RGB({self.curColor[0]}, {self.curColor[1]}, {self.curColor[2]}){Style.RESET_ALL}       ')
        print_tool.join(f'Mouse Speed: {self.curSpeed:.2f} pixels per second                                    ')

        if self.isMoved:
            print_tool.join(f'Is Mouse Stopped: {Fore.GREEN}✅ False{Style.RESET_ALL}')
        else:
            print_tool.join(f'Is Mouse Stopped: {Fore.RED}🛑 True{Style.RESET_ALL}  ')

        print_tool.join(f'Mouse Sensitivity: {Fore.MAGENTA}Medium{Style.RESET_ALL}')

        print_tool.join('\nColor Intensity:')
        print_tool.join(f'    Red Intensity: {Fore.RED}🔴 {self.curColor[0]}{Style.RESET_ALL}     ')
        print_tool.join(f'    Green Intensity: {Fore.GREEN}🟢 {self.curColor[1]}{Style.RESET_ALL}     ')
        print_tool.join(f'    Blue Intensity: {Fore.BLUE}🔵 {self.curColor[2]}{Style.RESET_ALL}     ')

        print_tool.join('\nWindow Information:')
        print_tool.join(f'    Window Title: {self.curWindowTitle}                                                     ')

        if self.isWindowChanged or self.__isKeepWindowChanged:
            print_tool.join(f'    {Fore.YELLOW}🔄 Window Changed!{Style.RESET_ALL}')
        else:
            print_tool.join(f'    {Fore.YELLOW}                   {Style.RESET_ALL}')

    def _stop(self):
        self.__windowChangedKeeperExecutor.shutdown()
        self.__LazyComputeColor.stop()

    def __exit__(self):
        self._stop()

    def __del__(self):
        self._stop()
