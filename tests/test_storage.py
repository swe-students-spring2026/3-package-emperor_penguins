import pytest
from pomodoro.timer import Timer
from pomodoro.storage import Storage


@pytest.fixture
def storage(tmp_path):
    file = tmp_path / "timers.json"
    return Storage(filename=file)


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


'''test for memory pesistence of timers in storage, which is used by the TUI to allow users to reuse previous timers.'''
def test_persistence(tmp_path):
    file = tmp_path / "timers.json"
    storage = Storage(filename=file)

    timer_id = storage.create_timer(25)
    storage.save()

    # Create a new storage instance to load from the file
    new_storage = Storage(filename=file)
    timers = new_storage.list_timers()

    assert timer_id in timers
    assert timers[timer_id].duration == 25

def test_file_created(tmp_path):
    file = tmp_path / "timers.json"
    storage = Storage(filename=file)
    storage.create_timer(10)
    assert file.exists()

def test_multiple_timers_persist(tmp_path):
    file = tmp_path / "timers.json"

    storage1 = Storage(filename=file)
    id1 = storage1.create_timer(10)
    id2 = storage1.create_timer(20)

    storage2 = Storage(filename=file)

    timers = storage2.list_timers()
    assert len(timers) == 2
    assert id1 in timers
    assert id2 in timers

def test_load_empty_file(tmp_path):
    file = tmp_path / "timers.json"
    file.write_text("{}")

    storage = Storage(filename=file)

    assert storage.list_timers() == {}