import os
import sys


class printer:
    buffer: list[str]
    oldBuffer: list[str]

    def __init__(self):
        self.buffer = []
        self.oldBuffer = []

    def join(self, string: str):
        """
        one line each
        :param string: add in buffer
        :return: none
        """
        self.buffer.append(string + '\n')

    def update(self):
        """
        print buffer
        :return: none
        """
        if self.buffer == self.oldBuffer:
            return

        # os.system("cls")
        sys.stdout.writelines([f"\033[{len(self.buffer) + 3}A\033[2K"] + self.buffer)
        sys.stdout.flush()

    def clear(self):
        """
        clear buffer
        :return: none
        """
        self.oldBuffer = self.buffer
        self.buffer = []
