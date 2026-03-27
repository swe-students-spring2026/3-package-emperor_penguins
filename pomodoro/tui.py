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


def render_ith_sub(current_sub_num: int, total_sub_num: int) -> str:
    """
    Display which sub-session the user is currently at.
    """
    return f"current sub-session: [{current_sub_num}/{total_sub_num}]"

def render_sub_progress(current_mins: int, total_mins, is_resting = False) -> str:
    """
    Display the progress of the current sub-session, either studying or resting.
    """
    if is_resting:
        progress_icon = emoji.emojize(":sleepy_face:")
        label = "resting"
    else:
        progress_icon = emoji.emojize(":tomato:")
        label = "studying"
    empty_icon = emoji.emojize(":white_medium_square: ") # the trailing space is on purpose

    length = 10
    filled_length = int(length * (current_mins / total_mins)) if total_mins > 0 else 0
    progress_bar = progress_icon * filled_length + empty_icon * (length - filled_length)
    specifics = f"{current_mins}min/{total_mins}min"
    output = f"current sub-session progress ({label}): {progress_bar} [{specifics}]"
    return output

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

def finish_session():
    """Call this when the timer hits 100% so the next print starts on a new line."""
    print()
    sys.stdout.flush()
