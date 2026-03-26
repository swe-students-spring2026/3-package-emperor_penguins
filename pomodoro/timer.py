# Timer 
import time

class Timer:
    def __init__(self, duration: int):
        # validate inputs
        if not isinstance(duration, int):
            raise TypeError("duration is not an integer.")
        if duration <= 0: 
            raise ValueError("duration must be greater than 0.")
        
        self.duration = duration
        self.remaining = duration
        self.status = "stopped" # stopped / running / paused
        self._last_tick_time = None

    def start(self):
        if self.remaining <= 0: 
            self.reset()
        if self.status != "running":
            self.status = "running"
            self._last_tick_time = time.time()

    def pause(self):
        if self.status == "running": 
            self.status = "paused"
            self._last_tick_time = None

    def reset(self):
        self.remaining = self.duration
        self.status = "stopped"
        self._last_tick_time = None

    def tick(self):
        if self.status != "running":
            return self.remaining
        
        now = time.time()

        if self._last_tick_time is None: 
            self._last_tick_time = now 
            return self.remaining
        
        elapsed = int(now - self._last_tick_time)

        if elapsed > 0: 
            self.remaining = max(0, self.remaining - elapsed)
            self._last_tick_time = now 

            if self.remaining == 0: 
                self.status = "stopped"
                self._last_tick_time = None
        
        return self.remaining