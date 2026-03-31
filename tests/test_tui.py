"""
Tests for pomodoro.tui module.
"""
import pytest
import emoji
from pomodoro import tui
from pomodoro.storage import Storage

def test_render_ith_sub():
    result = tui.render_ith_sub(1, 4)
    assert result == "current sub-session: [1/4]"


@pytest.mark.parametrize("current,total,is_resting,label,emoji_code", [
    (5, 10, False, "studying", ":tomato:"),
    (2, 5, True, "resting", ":sleepy_face:"),
])
def test_render_sub_progress_basic(current, total, is_resting, label, emoji_code):
    result = tui.render_sub_progress(current, total, is_resting)

    expected_emoji = emoji.emojize(emoji_code)

    assert label in result
    assert f"{current}min/{total}min" in result
    assert expected_emoji in result


@pytest.mark.parametrize("current,total,emoji_code", [
    (0, 10, ":tomato:"),
    (5, 10, ":tomato:"),
    (10, 10, ":tomato:"),
])
def test_render_sub_progress_filled_length(current, total, emoji_code):
    result = tui.render_sub_progress(current, total)

    expected_emoji = emoji.emojize(emoji_code)
    filled_count = result.count(expected_emoji)

    expected_filled = int(10 * (current / total))
    assert filled_count == expected_filled


def test_render_sub_progress_empty_icon_present():
    result = tui.render_sub_progress(3, 10)

    empty_icon = emoji.emojize(":white_medium_square:")
    assert empty_icon in result

def test_empty_icon_spacing():
    result = tui.render_sub_progress(0, 10)
    assert "◻️ " in result  # includes space

def test_render_sub_progress_full_bar_no_empty():
    result = tui.render_sub_progress(10, 10)

    empty_icon = emoji.emojize(":white_medium_square:")
    assert empty_icon not in result


def test_render_full_outputs_correctly(capsys):
    tui.render_full(2, 4, 6, 25, is_resting=False)

    captured = capsys.readouterr()
    output = captured.out

    assert "current sub-session: [2/4]" in output
    assert "6min/25min" in output


def test_render_full_resting_branch(capsys):
    tui.render_full(3, 4, 2, 5, is_resting=True)

    captured = capsys.readouterr()
    output = captured.out

    assert "resting" in output
    assert "2min/5min" in output


def test_finish_session_prints_newline(capsys):
    tui.finish_session()

    captured = capsys.readouterr()
    assert captured.out == "\n"


def test_render_sub_progress_zero_total_raises():
    with pytest.raises(ZeroDivisionError):
        tui.render_sub_progress(1, 0)


def test_render_ith_sub_invalid_total():
    with pytest.raises(ValueError):
        tui.render_ith_sub(1, 0)

def test_render_sub_progress_overflow():
    result = tui.render_sub_progress(15, 10)
    # Should not exceed bar length
    assert result.count(emoji.emojize(":tomato:")) <= 10

def test_render_sub_progress_negative():
    result = tui.render_sub_progress(-5, 10)
    # Should not produce negative filled icons
    assert result.count(emoji.emojize(":tomato:")) >= 0

def test_render_full_includes_control_chars(capsys):
    tui.render_full(1, 2, 5, 10)

    output = capsys.readouterr().out

    assert "\r" in output
    assert "\033[K" in output

def test_show_timer_history_with_data(capsys, tmp_path):
    storage = Storage(filename=tmp_path / "timers.json")
    storage.create_timer(25)

    tui.show_timer_history(storage)

    output = capsys.readouterr().out
    assert "Timer History:" in output
    assert "Duration: 25 minutes" in output