import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')
PRIORITIES = ['low', 'medium', 'high']


def load_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def add_task(
    description: str,
    due_date: str | None = None,
    priority: str = 'medium'
) -> None:
    if priority not in PRIORITIES:
        raise ValueError(f"Priority must be one of: {', '.join(PRIORITIES)}")

    if due_date:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Due date must be in YYYY-MM-DD format')

    tasks = load_tasks()
    task = {
        'description': description,
        'completed': False,
        'priority': priority,
        'due_date': due_date,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: {description}")


def list_tasks(show_completed: bool = True) -> None:
    tasks = load_tasks()
    if not tasks:
        print('No tasks found.')
        return

    visible_tasks = [
        t for t in tasks if show_completed or not t.get('completed')
    ]
    if not visible_tasks:
        print('No tasks to display.')
        return

    visible_tasks.sort(
        key=lambda x: (
            PRIORITIES.index(x.get('priority', 'medium')),
            x.get('due_date', '9999-99-99')
        )
    )

    for i, task in enumerate(visible_tasks, 1):
        status = '✓' if task.get('completed') else ' '
        priority = f"[{task.get('priority', 'medium')}]"
        due_date = (
            f"Due: {task.get('due_date')}" if task.get('due_date') else ''
        )
        print(
            f"{i}. [{status}] {priority} {task.get('description')} {due_date}"
        )


def complete_task(task_id: int) -> None:
    tasks = load_tasks()
    index = task_id - 1
    if index < 0 or index >= len(tasks):
        print('Invalid task ID')
        return
    tasks[index]['completed'] = True
    tasks[index]['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_tasks(tasks)
    print(f"Completed task {task_id}")


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    index = task_id - 1
    if index < 0 or index >= len(tasks):
        print('Invalid task ID')
        return
    deleted_task = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted task: {deleted_task['description']}")


def main() -> int:
    parser = argparse.ArgumentParser(description='Enhanced CLI task manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('--due-date', help='Due date (YYYY-MM-DD)')
    add_parser.add_argument(
        '--priority',
        choices=PRIORITIES,
        default='medium',
        help='Task priority (default: medium)'
    )

    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument(
        '--hide-completed',
        action='store_true',
        help='Hide completed tasks'
    )

    complete_parser = subparsers.add_parser(
        'complete',
        help='Mark a task as completed'
    )
    complete_parser.add_argument('id', type=int, help='ID of task to complete')

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='ID of task to delete')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            add_task(args.description, args.due_date, args.priority)
        elif args.command == 'list':
            list_tasks(not args.hide_completed)
        elif args.command == 'complete':
            complete_task(args.id)
        elif args.command == 'delete':
            delete_task(args.id)
    except ValueError as e:
        print(f'Error: {e}')
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
