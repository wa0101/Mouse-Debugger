from concurrent.futures import ThreadPoolExecutor, Future
import time


class fpsCounter:
    fps: int
    frames: int
    CounterPool: ThreadPoolExecutor
    Counter: Future
    doCount: bool

    def __init__(self):
        self.doCount = True
        self.fps = 0
        self.frames = 0
        self.CounterPool = ThreadPoolExecutor(max_workers=1)
        self.Counter = self.CounterPool.submit(self.count)

    def count(self):
        while self.doCount:
            self.frames = 0
            time.sleep(1)
            self.fps = self.frames

    def update(self):
        self.frames += 1

    def getFPS(self):
        return self.fps

    def stop(self):
        self.doCount = False
        self.CounterPool.shutdown()

    def __exit__(self):
        self.stop()

    def __del__(self):
        self.stop()
