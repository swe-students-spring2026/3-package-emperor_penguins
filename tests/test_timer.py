import pytest

from pomodoro.timer import Timer

# we use FakeTime + monkeypatch so that the Timer doesn't use real time
# for reproducibility of tests and time efficiency while running tests

class FakeTime:
    def __init__(self, start=1000):
        self.current = start

    def time(self):
        return self.current

    def advance(self, seconds):
        self.current += seconds

def test_init_sets_duration_remaining_and_status():
    timer = Timer(150)

    assert timer.duration == 150
    assert timer.remaining == 150
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_init_with_non_int_duration_raises_type_error():
    with pytest.raises(TypeError):
        Timer("25")

    with pytest.raises(TypeError):
        Timer(25.5)

    with pytest.raises(TypeError):
        Timer(None)

def test_init_with_zero_or_negative_duration_raises_value_error():
    with pytest.raises(ValueError):
        Timer(0)

    with pytest.raises(ValueError):
        Timer(-1)

    with pytest.raises(ValueError):
        Timer(-100)

def test_start_from_stopped_sets_running_and_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(60)
    timer.start()

    assert timer.status == "running"
    assert timer._last_tick_time == 1000
    assert timer.remaining == 60

def test_start_when_already_running_does_not_reset_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(60)
    timer.start()
    first_tick_time = timer._last_tick_time

    fake.advance(5)
    timer.start()

    assert timer.status == "running"
    assert timer._last_tick_time == first_tick_time
    assert timer._last_tick_time != fake.time()

def test_start_from_paused_sets_running_and_updates_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(60)
    timer.start()
    fake.advance(3)
    timer.pause()

    assert timer.status == "paused"
    assert timer._last_tick_time is None

    fake.advance(7)
    timer.start()

    assert timer.status == "running"
    assert timer._last_tick_time == fake.time()
    assert timer.remaining == 60

def test_start_when_remaining_zero_resets_before_running(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(10)
    timer.remaining = 0
    timer.status = "stopped"

    timer.start()

    assert timer.remaining == 10
    assert timer.status == "running"
    assert timer._last_tick_time == fake.time()

def test_pause_from_running_sets_paused_and_clears_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(30)
    timer.start()
    assert timer._last_tick_time == 1000

    timer.pause()

    assert timer.status == "paused"
    assert timer._last_tick_time is None
    assert timer.remaining == 30

def test_pause_from_stopped_does_nothing():
    timer = Timer(30)
    timer.pause()

    assert timer.status == "stopped"
    assert timer.remaining == 30
    assert timer._last_tick_time is None

def test_pause_from_paused_does_nothing(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(30)
    timer.start()
    timer.pause()
    timer.pause()

    assert timer.status == "paused"
    assert timer.remaining == 30
    assert timer._last_tick_time is None

def test_reset_restores_remaining_status_and_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(45)
    timer.start()
    fake.advance(10)
    timer.tick()
    assert timer.remaining == 35

    timer.reset()

    assert timer.remaining == 45
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_tick_when_stopped_returns_remaining_without_change():
    timer = Timer(20)
    result = timer.tick()

    assert result == 20
    assert timer.remaining == 20
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_tick_when_paused_returns_remaining_without_change(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    timer.pause()

    result = timer.tick()

    assert result == 20
    assert timer.remaining == 20
    assert timer.status == "paused"
    assert timer._last_tick_time is None

def test_tick_when_running_and_last_tick_time_none_sets_it_and_does_not_decrement(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.status = "running"
    timer._last_tick_time = None

    result = timer.tick()

    assert result == 20
    assert timer.remaining == 20
    assert timer.status == "running"
    assert timer._last_tick_time == fake.time()

def test_tick_with_less_than_one_second_elapsed_does_not_decrement(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    fake.advance(0)

    result = timer.tick()

    assert result == 20
    assert timer.remaining == 20
    assert timer.status == "running"
    assert timer._last_tick_time == 1000

def test_tick_with_fractional_elapsed_under_one_second_does_not_decrement(monkeypatch):
    fake = FakeTime(start=1000.0)
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    fake.advance(0.8)

    result = timer.tick()

    assert result == 20
    assert timer.remaining == 20
    assert timer.status == "running"
    assert timer._last_tick_time == 1000.0

def test_tick_with_one_second_elapsed_decrements_by_one(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    fake.advance(1)

    result = timer.tick()

    assert result == 19
    assert timer.remaining == 19
    assert timer.status == "running"
    assert timer._last_tick_time == 1001

def test_tick_with_multiple_seconds_elapsed_decrements_by_elapsed_amount(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    fake.advance(7)

    result = timer.tick()

    assert result == 13
    assert timer.remaining == 13
    assert timer.status == "running"
    assert timer._last_tick_time == 1007

def test_tick_multiple_times_accumulates_correctly(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(15)
    timer.start()

    fake.advance(3)
    assert timer.tick() == 12
    assert timer.remaining == 12
    assert timer._last_tick_time == 1003

    fake.advance(2)
    assert timer.tick() == 10
    assert timer.remaining == 10
    assert timer._last_tick_time == 1005

    fake.advance(5)
    assert timer.tick() == 5
    assert timer.remaining == 5
    assert timer._last_tick_time == 1010

def test_tick_never_makes_remaining_negative(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(5)
    timer.start()
    fake.advance(100)

    result = timer.tick()

    assert result == 0
    assert timer.remaining == 0
    assert timer.remaining >= 0

def test_tick_reaching_zero_stops_timer_and_clears_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(5)
    timer.start()
    fake.advance(5)

    result = timer.tick()

    assert result == 0
    assert timer.remaining == 0
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_tick_past_zero_stops_timer_and_clears_last_tick_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(5)
    timer.start()
    fake.advance(8)

    result = timer.tick()

    assert result == 0
    assert timer.remaining == 0
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_tick_after_finished_and_stopped_does_nothing(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(3)
    timer.start()
    fake.advance(3)
    timer.tick()

    assert timer.remaining == 0
    assert timer.status == "stopped"

    fake.advance(5)
    result = timer.tick()

    assert result == 0
    assert timer.remaining == 0
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_start_after_finishing_resets_and_runs_again(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(3)
    timer.start()
    fake.advance(3)
    timer.tick()

    assert timer.remaining == 0
    assert timer.status == "stopped"

    fake.advance(10)
    timer.start()

    assert timer.remaining == 3
    assert timer.status == "running"
    assert timer._last_tick_time == fake.time()

def test_is_finished_false_initially():
    timer = Timer(25)

    assert timer.is_finished() is False

def test_is_finished_true_when_remaining_zero():
    timer = Timer(25)
    timer.remaining = 0

    assert timer.is_finished() is True

def test_get_progress_initially_zero():
    timer = Timer(50)

    assert timer.get_progress() == 0

def test_get_progress_after_time_passes(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(50)
    timer.start()
    fake.advance(12)
    timer.tick()

    assert timer.remaining == 38
    assert timer.get_progress() == 12

def test_get_progress_when_finished_equals_duration():
    timer = Timer(50)
    timer.remaining = 0

    assert timer.get_progress() == 50

def test_get_display_time_formats_exact_minutes():
    timer = Timer(300)

    assert timer.get_display_time() == "05:00"

def test_get_display_time_formats_minutes_and_seconds():
    timer = Timer(300)
    timer.remaining = 125

    assert timer.get_display_time() == "02:05"

def test_get_display_time_formats_under_one_minute():
    timer = Timer(30)

    assert timer.get_display_time() == "00:30"

def test_get_display_time_formats_zero():
    timer = Timer(30)
    timer.remaining = 0

    assert timer.get_display_time() == "00:00"

def test_get_status_returns_complete_dictionary_initial_state():
    timer = Timer(90)

    status = timer.get_status()

    assert isinstance(status, dict)
    assert status["duration"] == 90
    assert status["remaining"] == 90
    assert status["status"] == "stopped"
    assert status["display_time"] == "01:30"

def test_get_status_returns_updated_values_after_tick(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(90)
    timer.start()
    fake.advance(15)
    timer.tick()

    status = timer.get_status()

    assert status["duration"] == 90
    assert status["remaining"] == 75
    assert status["status"] == "running"
    assert status["display_time"] == "01:15"

def test_get_status_after_pause(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(40)
    timer.start()
    timer.pause()

    status = timer.get_status()

    assert status["duration"] == 40
    assert status["remaining"] == 40
    assert status["status"] == "paused"
    assert status["display_time"] == "00:40"

def test_get_status_after_finish(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(4)
    timer.start()
    fake.advance(4)
    timer.tick()

    status = timer.get_status()

    assert status["duration"] == 4
    assert status["remaining"] == 0
    assert status["status"] == "stopped"
    assert status["display_time"] == "00:00"

def test_pause_then_tick_does_not_decrement(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    fake.advance(5)
    timer.pause()
    remaining_before = timer.remaining

    fake.advance(10)
    result = timer.tick()

    assert result == remaining_before
    assert timer.remaining == remaining_before
    assert timer.status == "paused"

def test_reset_after_pause_restores_initial_state(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()
    timer.pause()
    timer.reset()

    assert timer.remaining == 20
    assert timer.status == "stopped"
    assert timer._last_tick_time is None

def test_reset_after_finish_restores_initial_state(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(2)
    timer.start()
    fake.advance(2)
    timer.tick()
    assert timer.remaining == 0

    timer.reset()

    assert timer.remaining == 2
    assert timer.status == "stopped"
    assert timer._last_tick_time is None
    assert timer.is_finished() is False

def test_start_after_pause_does_not_count_paused_time(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(20)
    timer.start()

    fake.advance(5)
    timer.tick()
    assert timer.remaining == 15

    timer.pause()
    fake.advance(100)

    timer.start()
    assert timer.remaining == 15
    assert timer.status == "running"
    assert timer._last_tick_time == fake.time()

    fake.advance(3)
    timer.tick()
    assert timer.remaining == 12

def test_tick_exactly_to_zero_from_partial_progress(monkeypatch):
    fake = FakeTime()
    monkeypatch.setattr("pomodoro.timer.time.time", fake.time)

    timer = Timer(10)
    timer.start()

    fake.advance(4)
    timer.tick()
    assert timer.remaining == 6

    fake.advance(6)
    result = timer.tick()

    assert result == 0
    assert timer.remaining == 0
    assert timer.status == "stopped"
    assert timer.is_finished() is True