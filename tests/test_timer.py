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

