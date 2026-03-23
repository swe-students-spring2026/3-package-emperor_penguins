"""
This is the terminal-based user interface (TUI) for a Pomodoro timer, 
displaying data in console/terminal.
Users should see the timer and session info (the progress bars, the ticking clock, the tables) 
appearing in the command line.
"""
import emoji
tomato_icon = emoji.emojize(":tomato:") # this is a str
empty_icon = emoji.emojize(":white_medium_square: ") # the trailing space is on purpose
print(tomato_icon * 5 + empty_icon * 5)
