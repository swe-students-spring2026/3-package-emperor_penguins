# Timer 
import time

class Timer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining = duration
        self.status = "stopped" # stopped / running / paused

    def start(self):
        self.status = "running"

    def pause(self):
        self.status = "paused"

    def reset(self):
        self.remaining = self.duration
        self.status = "stopped"

    def tick(self):
        if self.status == "running" and self.remaining > 0:
            self.remaining -= 1