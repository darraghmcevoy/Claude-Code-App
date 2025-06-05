import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

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
    priority: str = 'medium',
    category: str | None = None,
    tags: List[str] | None = None
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
        'category': category,
        'tags': tags or [],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: {description}")


def list_tasks(
    show_completed: bool = True,
    category: str | None = None,
    tag: str | None = None,
    search: str | None = None
) -> None:
    tasks = load_tasks()
    if not tasks:
        print('No tasks found.')
        return

    # Filter tasks
    visible_tasks = [
        t for t in tasks
        if (show_completed or not t.get('completed'))
        and (not category or t.get('category') == category)
        and (not tag or tag in (t.get('tags') or []))
        and (not search or search.lower() in t.get('description', '').lower())
    ]

    if not visible_tasks:
        print('No tasks to display.')
        return

    # Sort tasks by priority and due date
    visible_tasks.sort(
        key=lambda x: (
            PRIORITIES.index(x.get('priority', 'medium')),
            x.get('due_date', '9999-99-99')
        )
    )

    # Group tasks by category if any tasks have categories
    if any(t.get('category') for t in visible_tasks):
        tasks_by_category: Dict[str, List[Dict[str, Any]]] = {}
        for task in visible_tasks:
            cat = task.get('category', 'Uncategorized')
            tasks_by_category.setdefault(cat, []).append(task)

        for category, cat_tasks in tasks_by_category.items():
            print(f"\n{category}:")
            for i, task in enumerate(cat_tasks, 1):
                _print_task(i, task)
    else:
        for i, task in enumerate(visible_tasks, 1):
            _print_task(i, task)


def _print_task(index: int, task: Dict[str, Any]) -> None:
    status = '✓' if task.get('completed') else ' '
    priority = f"[{task.get('priority', 'medium')}]"
    due_date = f"Due: {task.get('due_date')}" if task.get('due_date') else ''
    tags = f"Tags: {', '.join(task.get('tags', []))}" if task.get('tags') else ''
    print(
        f"{index}. [{status}] {priority} {task.get('description')} {due_date} {tags}"
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


def export_tasks(filename: str) -> None:
    tasks = load_tasks()
    with open(filename, 'w') as f:
        json.dump(tasks, f, indent=2)
    print(f"Exported {len(tasks)} tasks to {filename}")


def import_tasks(filename: str) -> None:
    try:
        with open(filename, 'r') as f:
            tasks = json.load(f)
        save_tasks(tasks)
        print(f"Imported {len(tasks)} tasks from {filename}")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error importing tasks: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description='Enhanced CLI task manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('--due-date', help='Due date (YYYY-MM-DD)')
    add_parser.add_argument(
        '--priority',
        choices=PRIORITIES,
        default='medium',
        help='Task priority (default: medium)'
    )
    add_parser.add_argument('--category', help='Task category')
    add_parser.add_argument('--tags', help='Comma-separated list of tags')

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument(
        '--hide-completed',
        action='store_true',
        help='Hide completed tasks'
    )
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.add_argument('--search', help='Search in task descriptions')

    # Complete task command
    complete_parser = subparsers.add_parser(
        'complete',
        help='Mark a task as completed'
    )
    complete_parser.add_argument('id', type=int, help='ID of task to complete')

    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='ID of task to delete')

    # Export tasks command
    export_parser = subparsers.add_parser('export', help='Export tasks to JSON')
    export_parser.add_argument('filename', help='Output filename')

    # Import tasks command
    import_parser = subparsers.add_parser('import', help='Import tasks from JSON')
    import_parser.add_argument('filename', help='Input filename')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            tags = args.tags.split(',') if args.tags else None
            add_task(
                args.description,
                args.due_date,
                args.priority,
                args.category,
                tags
            )
        elif args.command == 'list':
            list_tasks(
                not args.hide_completed,
                args.category,
                args.tag,
                args.search
            )
        elif args.command == 'complete':
            complete_task(args.id)
        elif args.command == 'delete':
            delete_task(args.id)
        elif args.command == 'export':
            export_tasks(args.filename)
        elif args.command == 'import':
            import_tasks(args.filename)
    except ValueError as e:
        print(f'Error: {e}')
        return 1
    return 0


if __name__ == '__main__':
    exit(main()) 