"""
Since our Pomodoro has a terminal-based user interface (TUI), 
this library has utility functions to display data in console/terminal.
Users should see the timer and session info (the progress bars, the ticking clock, the tables) 
appearing in the command line.

demo:
current sub-session: [2/4] # meaning the user is at the second sub-session of this study session
if it is studying time:
    current sub-session progress: [tomato...⬜️⬜️⬜️⬜️⬜️⬜️⬜️] (12min/25min)
else if it is rest time:
    curent sub-session rest progress: [sleepy.....⬜⬜⬜⬜] (3min/5min)
"""
import sys
import emoji
from pomodoro.storage import Storage



def render_ith_sub(current_sub_num: int, total_sub_num: int) -> str:
    """
    Display which sub-session the user is currently at.
    """
    if total_sub_num <= 0:
        raise ValueError("Total_sub_num must be greater than zero when rendering ith sub-session!")
    return f"current sub-session: [{current_sub_num}/{total_sub_num}]"

# def render_sub_progress(current_mins: int, total_mins, is_resting = False) -> str:
#     """
#     Display the progress of the current sub-session, either studying or resting.
#     """
#     if is_resting:
#         progress_icon = emoji.emojize(":sleepy_face:")
#         label = "resting"
#     else:
#         progress_icon = emoji.emojize(":tomato:")
#         label = "studying"
#     empty_icon = emoji.emojize(":white_medium_square: ") # the trailing space is on purpose
#     length = 10
#     # Raise ZeroDivisionError.
#     if total_mins == 0:
#         raise ZeroDivisionError("Total minutes cannot be zero when rendering sub-session progress!")
#     filled_length = int(length * (current_mins / total_mins)) if total_mins > 0 else 0
#     progress_bar = progress_icon * filled_length + empty_icon * (length - filled_length)
#     specifics = f"{current_mins}min/{total_mins}min"
#     output = f"current sub-session progress ({label}): {progress_bar} [{specifics}]"
#     return output
import emoji

def render_sub_progress(current: int, total: int, is_resting: bool = False) -> str:
    """
    Render a sub-session progress bar with emojis.

    Args:
        current: Minutes completed
        total: Total minutes for the sub-session
        is_resting: Whether the session is a rest period

    Returns:
        str: Progress bar string with label and filled/empty icons
    """
    if total <= 0:
        raise ZeroDivisionError("Total duration must be greater than 0")

    # Bar settings
    bar_length = 10
    label = "resting" if is_resting else "studying"

    # Choose emoji
    filled_emoji = emoji.emojize(":sleepy_face:") if is_resting else emoji.emojize(":tomato:")
    empty_emoji = emoji.emojize(":white_medium_square:") + " "  # append space for spacing test

    # Clamp current to [0, total]
    current = max(0, min(current, total))

    # Calculate number of filled icons
    filled_count = int(bar_length * (current / total))
    empty_count = bar_length - filled_count

    # Build progress bar string
    bar = filled_emoji * filled_count + empty_emoji * empty_count

    return f"{label}: {bar} {current}min/{total}min"

def render_full(current_sub_num: int, total_sub_num: int,
                current_mins: int, total_mins: int,
                is_resting = False):
    """
    Render the full TUI, including the timer, the session info, and the progress bars.
    """
    ith_sub = render_ith_sub(current_sub_num, total_sub_num)
    sub_progress = render_sub_progress(current_mins, total_mins, is_resting)
    full_output = f"\r\033[K\033[F{ith_sub}\n{sub_progress}"
    sys.stdout.write(full_output)
    sys.stdout.flush()

#Lan's edits
def show_timer_history(storage: Storage):
    """
    Print all timers in storage with their IDs and durations
    """
    timers = storage.list_timers()
    
    if not timers:
        print("No timers found.")
        return
    print("Timer History:")
    for timer_id, timer in timers.items():
        print(f"ID: {timer_id}, Duration: {timer.duration} minutes")

def finish_session():
    """Call this when the timer hits 100% so the next print starts on a new line."""
    print()
    sys.stdout.flush()


