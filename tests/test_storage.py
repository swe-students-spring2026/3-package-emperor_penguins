import unittest
from pomodoro.timer import Timer
from pomodoro.storage import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()

    def test_create_and_get_timer(self):
        timer_id = self.storage.create_timer(25)
        timer = self.storage.get_timer(timer_id)
        self.assertIsInstance(timer, Timer)
        self.assertEqual(timer.duration, 25)

    def test_list_timers(self):
        timer_id1 = self.storage.create_timer(15)
        timer_id2 = self.storage.create_timer(30)
        timers = self.storage.list_timers()
        self.assertIn(timer_id1, timers)
        self.assertIn(timer_id2, timers)
        self.assertEqual(len(timers), 2)

    def test_update_timer(self):
        timer_id = self.storage.create_timer(20)
        self.storage.update_timer(timer_id, duration=40)
        timer = self.storage.get_timer(timer_id)
        self.assertEqual(timer.duration, 40)

    def test_update_invalid_attribute(self):
        timer_id = self.storage.create_timer(10)
        with self.assertRaises(ValueError):
            self.storage.update_timer(timer_id, invalid_attr=123)

    def test_update_nonexistent_timer(self):
        with self.assertRaises(ValueError) as context:
            self.storage.update_timer("nonexistent_id", duration=30)
        self.assertIn("Timer nonexistent_id does not exist.", str(context.exception))

    def test_delete_timer(self):
        timer_id = self.storage.create_timer(10)
        self.storage.delete_timer(timer_id)
        with self.assertRaises(ValueError):
            self.storage.get_timer(timer_id)

    def test_get_nonexistent_timer(self):
        with self.assertRaises(ValueError):
            self.storage.get_timer("nonexistent_id")

    def test_delete_nonexistent_timer(self):
        with self.assertRaises(ValueError):
            self.storage.delete_timer("nonexistent_id")

if __name__ == "__main__":
    unittest.main()