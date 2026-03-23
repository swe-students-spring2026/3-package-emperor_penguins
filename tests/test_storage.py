import pytest
from pomodoro.timer import Timer
from pomodoro.storage import Storage


@pytest.fixture
def storage():
    return Storage()


def test_create_and_get_timer(storage):
    timer_id = storage.create_timer(25)
    timer = storage.get_timer(timer_id)

    assert isinstance(timer, Timer)
    assert timer.duration == 25


def test_list_timers(storage):
    timer_id1 = storage.create_timer(15)
    timer_id2 = storage.create_timer(30)

    timers = storage.list_timers()

    assert timer_id1 in timers
    assert timer_id2 in timers
    assert len(timers) == 2


def test_update_timer(storage):
    timer_id = storage.create_timer(20)

    storage.update_timer(timer_id, duration=40)
    timer = storage.get_timer(timer_id)

    assert timer.duration == 40


def test_update_invalid_attribute(storage):
    timer_id = storage.create_timer(10)

    with pytest.raises(ValueError):
        storage.update_timer(timer_id, invalid_attr=123)


def test_update_nonexistent_timer(storage):
    with pytest.raises(ValueError) as exc_info:
        storage.update_timer("nonexistent_id", duration=30)

    assert "Timer nonexistent_id does not exist." in str(exc_info.value)


def test_delete_timer(storage):
    timer_id = storage.create_timer(10)

    storage.delete_timer(timer_id)

    with pytest.raises(ValueError):
        storage.get_timer(timer_id)


def test_get_nonexistent_timer(storage):
    with pytest.raises(ValueError):
        storage.get_timer("nonexistent_id")


def test_delete_nonexistent_timer(storage):
    with pytest.raises(ValueError):
        storage.delete_timer("nonexistent_id")