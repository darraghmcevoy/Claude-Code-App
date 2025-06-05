import os
import tempfile
import json
from contextlib import redirect_stdout
from io import StringIO
from datetime import datetime

import unittest

import task_manager


class TaskManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tasks_file = os.path.join(self.tmpdir.name, 'tasks.json')
        # patch TASKS_FILE
        self._orig_tasks_file = task_manager.TASKS_FILE
        task_manager.TASKS_FILE = self.tasks_file

    def tearDown(self):
        task_manager.TASKS_FILE = self._orig_tasks_file
        self.tmpdir.cleanup()

    def read_tasks(self):
        if not os.path.exists(self.tasks_file):
            return []
        with open(self.tasks_file) as f:
            return json.load(f)

    def test_add_and_list(self):
        task_manager.add_task('Test task', priority='high')
        tasks = self.read_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], 'Test task')
        self.assertEqual(tasks[0]['priority'], 'high')

        buf = StringIO()
        with redirect_stdout(buf):
            task_manager.list_tasks()
        output = buf.getvalue()
        self.assertIn('Test task', output)

    def test_complete_and_delete(self):
        task_manager.add_task('Another task')
        task_manager.complete_task(1)
        tasks = self.read_tasks()
        self.assertTrue(tasks[0]['completed'])

        task_manager.delete_task(1)
        tasks = self.read_tasks()
        self.assertEqual(tasks, [])

    def test_invalid_priority(self):
        with self.assertRaises(ValueError) as cm:
            task_manager.add_task('Test task', priority='invalid')
        self.assertIn('Priority must be one of', str(cm.exception))

    def test_invalid_due_date(self):
        with self.assertRaises(ValueError) as cm:
            task_manager.add_task('Test task', due_date='invalid-date')
        self.assertIn('Due date must be in YYYY-MM-DD format', str(cm.exception))

    def test_valid_due_date(self):
        task_manager.add_task('Test task', due_date='2024-12-31')
        tasks = self.read_tasks()
        self.assertEqual(tasks[0]['due_date'], '2024-12-31')

    def test_hide_completed(self):
        task_manager.add_task('Task 1')
        task_manager.add_task('Task 2')
        task_manager.complete_task(1)

        buf = StringIO()
        with redirect_stdout(buf):
            task_manager.list_tasks(show_completed=False)
        output = buf.getvalue()
        self.assertNotIn('Task 1', output)
        self.assertIn('Task 2', output)

    def test_sort_by_priority_and_due_date(self):
        task_manager.add_task('Low priority', priority='low', due_date='2024-12-31')
        task_manager.add_task('High priority', priority='high', due_date='2024-01-01')
        task_manager.add_task('Medium priority', priority='medium')

        buf = StringIO()
        with redirect_stdout(buf):
            task_manager.list_tasks()
        output = buf.getvalue()
        
        # Check order: high -> medium -> low
        high_idx = output.find('High priority')
        medium_idx = output.find('Medium priority')
        low_idx = output.find('Low priority')
        
        self.assertLess(high_idx, medium_idx)
        self.assertLess(medium_idx, low_idx)

    def test_invalid_task_id(self):
        task_manager.add_task('Test task')
        
        # Test invalid ID for complete
        buf = StringIO()
        with redirect_stdout(buf):
            task_manager.complete_task(999)
        self.assertIn('Invalid task ID', buf.getvalue())

        # Test invalid ID for delete
        buf = StringIO()
        with redirect_stdout(buf):
            task_manager.delete_task(999)
        self.assertIn('Invalid task ID', buf.getvalue())


if __name__ == '__main__':
    unittest.main() 