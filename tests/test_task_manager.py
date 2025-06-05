import os
import tempfile
import json
from contextlib import redirect_stdout
from io import StringIO

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


if __name__ == '__main__':
    unittest.main()
