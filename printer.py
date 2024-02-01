import queue
import sys
import threading


class printer:
    buffer: list[str]
    oldBuffer: list[str]
    emptyBuffer: list[str]
    _printThread: threading.Thread
    _printQueue: queue.Queue
    isRunning: bool

    def __init__(self, empty_buffer: list[str] = None):
        """
        initialize the printer.
        :param empty_buffer: the basic buffer when reset/clear.
        :return: none
        """
        if empty_buffer is None:
            empty_buffer = list()
        self.emptyBuffer = empty_buffer
        self._printThread = threading.Thread(target=self._update)
        self._printQueue = queue.Queue(2)
        self.isRunning = True
        self.reset()
        self._printThread.start()

    def join(self, string: str):
        """
        add in buffer.
        :param string: one line each
        :return: none
        """
        self.buffer.append(string + '\n')

    def update(self):
        """
        update buffer on screen.
        :return: none
        """
        if self.buffer == self.oldBuffer:
            return
        if self._printQueue.full():
            self._printQueue.get()
        self._printQueue.put(self.buffer)

    def _update(self):
        while self.isRunning:
            buffer = self._printQueue.get()
            sys.stdout.writelines([f"\033[{len(buffer) + 3}A\033[2K"] + buffer)
            sys.stdout.flush()

    def clear(self):
        """
        clear buffer.
        :return: none
        """
        self.oldBuffer = self.buffer
        self.buffer = self.emptyBuffer.copy()

    def reset(self):
        """
        reset buffer.
        :return: none
        """
        self.buffer = self.emptyBuffer.copy()
        self.oldBuffer = self.emptyBuffer.copy()

    def stop(self):
        self.isRunning = False
        self._printThread.join()

    def __exit__(self):
        self.stop()

    def __del__(self):
        self.stop()
