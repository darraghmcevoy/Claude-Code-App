# Claude Code App

This is a new Git repository created with Claude Code.

## Getting Started

This repository is set up and ready for development.

## Requirements

* Python 3.8+

No external dependencies are required.

## Features

- Git repository with GitHub integration
- Ready for VS Code development
- Claude Code compatible

## CLI Task Manager

The repository includes an enhanced CLI tool for managing tasks. Tasks are saved
in a `tasks.json` file located next to the script.

### Usage

```bash
# Add a task
python task_manager.py add "Buy milk"

# Add a task with a due date and priority
python task_manager.py add "Submit report" --due-date 2024-05-01 --priority high

# List tasks
python task_manager.py list

# Complete a task by its ID
python task_manager.py complete 1

# Delete a task
python task_manager.py delete 1
```

See `LICENSE` for licensing information.
