import os
import sys


class printer:
    buffer: list[str]
    oldBuffer: list[str]
    emptyBuffer: list[str]

    def __init__(self, empty_buffer: list[str] = None):
        """
        initialize the printer.
        :param empty_buffer: the basic buffer when reset/clear.
        :return: none
        """
        if empty_buffer is None:
            empty_buffer = list()
        self.emptyBuffer = empty_buffer
        self.reset()

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
        sys.stdout.writelines([f"\033[{len(self.buffer) + 3}A\033[2K"] + self.buffer)
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
