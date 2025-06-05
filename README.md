# CLI Task Manager

A powerful command-line task manager built with Python that helps you keep track of your daily tasks with priorities, due dates, categories, and tags.

## Features

- Add new tasks with descriptions
- Set task priorities (low, medium, high)
- Add due dates to tasks
- Organize tasks with categories and tags
- Search tasks by description
- Filter tasks by category or tag
- List all tasks with their completion status
- Hide completed tasks
- Mark tasks as complete
- Delete tasks
- Export/import tasks to/from JSON
- Sort tasks by priority and due date
- Persistent storage using JSON
- Simple and intuitive command-line interface

## Requirements

- Python 3.8 or higher
- No external dependencies required

## Installation

### From Source

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Using pip

```bash
pip install cli-task-manager
```

## Usage

The task manager provides several commands:

```bash
# Add a new task
task-manager add "Buy milk"

# Add a task with priority, due date, category, and tags
task-manager add "Submit report" --due-date 2024-05-01 --priority high --category "Work" --tags "urgent,important"

# List all tasks
task-manager list

# List tasks with filters
task-manager list --hide-completed --category "Work" --tag "urgent" --search "report"

# Complete a task by its ID
task-manager complete 1

# Delete a task by its ID
task-manager delete 1

# Export tasks to a JSON file
task-manager export tasks.json

# Import tasks from a JSON file
task-manager import tasks.json
```

Tasks are stored in a local `tasks.json` file in the same directory as the script.

## Example Output

```
Work:
1. [ ] [high] Submit report Due: 2024-05-01 Tags: urgent, important
2. [ ] [medium] Review code Due: 2024-04-15 Tags: review

Personal:
3. [ ] [low] Buy milk
4. [✓] [medium] Call mom
```

## Task Properties

- **Description**: Required text describing the task
- **Priority**: Optional (low, medium, high) - defaults to medium
- **Due Date**: Optional date in YYYY-MM-DD format
- **Category**: Optional category for grouping tasks
- **Tags**: Optional list of tags for filtering
- **Status**: Automatically tracked (completed or not)
- **Created At**: Automatically set when task is created
- **Completed At**: Automatically set when task is completed

## Development

### Setup

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Testing

Run the test suite:
```bash
pytest
```

### Linting

Check code style:
```bash
ruff check .
ruff format .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.