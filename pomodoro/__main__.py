"""
This is a file to demo tui.py
"""
import time
import argparse
from pomodoro.session import PomodoroSession
from pomodoro.tui import render_full, finish_session

parser = argparse.ArgumentParser(description="Run a Pomodoro timer in terminal.")
parser.add_argument("--work", type=int, default=25, help="Work duration in minutes", dest="work_duration")
parser.add_argument("--break", type=int, default=5, help="Break duration in minutes", dest="break_duration")
parser.add_argument("--cycles", type=int, default=4, help="Number of Pomodoro cycles")
parser.add_argument("--version", "-v", action="version", version="Pomodoro 1.0.0", help="Show the version and exit")
args = parser.parse_args()

work_duration = args.work_duration
break_duration = args.break_duration
total_cycles = args.cycles

session = PomodoroSession(work_duration, break_duration)
session.total_cycles = total_cycles

print("\n====================================================\n")
session.start()
while session.current_phase is not None:
    session.tick(total_cycles)
    status = session.get_status()

    current_sub_num = min(session.completed_cycles + 1, total_cycles)
    total_sub_num = total_cycles
    current_mins = status['remaining']
    total_mins = status.get('total', current_mins)
    is_resting = (status['phase'] == "break")

    render_full(current_sub_num, total_sub_num, current_mins, total_mins, is_resting)
    time.sleep(1) # Set it to 1 or less for debugging.

finish_session()
print("====================================================\n")
print("** Pomodoro session completed! **\n")
