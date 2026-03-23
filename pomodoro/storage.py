import uuid
from typing import Dict, Any
from pomodoro.timer import Timer

class Storage:
    def __init__(self):
        self._timers: Dict[str, Timer] = {} # Store as a dictionary: {timer_id: Timer}

    def create_timer(self, duration: int) -> str:
        """
        Create a new timer and store it in memory.
        """

        timer_id = str(uuid.uuid4())
        self._timers[timer_id] = Timer(duration)
        return timer_id

    def get_timer(self, timer_id: str) -> Timer:
        """
        Retrieve a timer from storage by its unique ID.
        """

        if timer_id not in self._timers:
            raise ValueError(f"Timer {timer_id} does not exist.")

        return self._timers[timer_id]

    def list_timers(self) -> Dict[str, Timer]:
        """
        Retrieve all timers currently stored in memory.
        """

        return self._timers

    def update_timer(self, timer_id: str, **updates) -> None:
        """
        Update timer fields.
        """

        if timer_id not in self._timers:
            raise ValueError(f"Timer {timer_id} does not exist.")

        timer = self._timers[timer_id]
        for key, value in updates.items():
            if not hasattr(timer, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(timer, key, value)

    def delete_timer(self, timer_id: str) -> None:
        """
        Delete a timer.
        """

        if timer_id not in self._timers:
            raise ValueError(f"Timer {timer_id} does not exist.")

        del self._timers[timer_id]