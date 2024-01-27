from threading import Thread
import time


class fpsCounter:
    fps: int
    frames: int
    Counter: Thread
    doCount: bool

    def __init__(self):
        self.doCount = True
        self.fps = 0
        self.frames = 0
        self.Counter = Thread(target=self.count, name="FPS Counter")
        self.Counter.start()

    def count(self):
        while self.doCount:
            self.frames = 0
            time.sleep(1)
            self.fps = self.frames

    def update(self):
        self.frames += 1

    def getFPS(self):
        return self.fps

    def _stop(self):
        self.doCount = False
        self.Counter.join(1)

    def __exit__(self):
        self._stop()

    def __del__(self):
        self._stop()
