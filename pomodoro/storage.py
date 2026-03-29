import uuid
from typing import Dict, Any
import json
import os
from pomodoro.timer import Timer

class Storage:
    def __init__(self, filename = "timers.json"):
        self._filename = filename
        self._timers : Dict[str, Timer] = {} # Store as a dictionary: {timer_id: Timer} 
        self._load()

    def _load(self):
        """
        Load timers from a JSON file into memory.
        """
        if not os.path.exists(self._filename):
                return
            
        with open(self._filename, "r") as f:
            data = json.load(f)
            for tid, duration in data.items():
                self._timers[tid] = Timer(duration)

    def _save(self):
        """
        Save timers from memory to a JSON file.
        """
        data = {tid: timer.duration for tid, timer in self._timers.items()}
        with open(self._filename, "w") as f:
            json.dump(data, f)

    def save(self): #helps with coverage
        self._save()

    def create_timer(self, duration: int) -> str:
        """
        Create a new timer and store it in memory.
        """

        timer_id = str(uuid.uuid4())
        self._timers[timer_id] = Timer(duration)
        self._save()  # Save to file after creating a new timer
        return timer_id

    def get_timer(self, timer_id: str) -> Timer:
        """
        Retrieve a timer from storage by its unique ID.
        """

        if timer_id not in self._timers:
            raise ValueError(f"Timer {timer_id} does not exist.")

        return self._timers[timer_id]

    def list_timers(self) -> Dict[str, Timer]: #important for get_timer_presets
        """
        Retrieve all timers currently stored in memory.
        """

        return self._timers

    def get_timer_presets(self) -> Dict[str, int]:
        """
        Return a dictionary of preset timer names and their durations.
        """

        return {
            tid: timer.duration for tid, timer in self._timers.items()
        }

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
        self._save()  # Save changes to file after deleting a timer
