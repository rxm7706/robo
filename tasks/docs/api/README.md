<!-- markdownlint-disable -->

# API Overview

## Modules

- [`robocorp.tasks`](./robocorp.tasks.md#module-robocorptasks): Robocorp tasks helps in creating entry points for your automation project.
- [`robocorp.tasks.cli`](./robocorp.tasks.cli.md#module-robocorptaskscli): Main entry point for running tasks from robocorp-tasks.

## Classes

- No classes

## Functions

- [`tasks.get_current_task`](./robocorp.tasks.md#function-get_current_task): Provides the task which is being currently run or None if not currently
- [`tasks.get_output_dir`](./robocorp.tasks.md#function-get_output_dir): Provide the output directory being used for the run or None if there's no
- [`tasks.session_cache`](./robocorp.tasks.md#function-session_cache): Provides decorator which caches return and clears automatically when all
- [`tasks.task`](./robocorp.tasks.md#function-task): Decorator for tasks (entry points) which can be executed by `robocorp.tasks`.
- [`tasks.task_cache`](./robocorp.tasks.md#function-task_cache): Provides decorator which caches return and clears it automatically when the
- [`cli.main`](./robocorp.tasks.cli.md#function-main): Entry point for running tasks from robocorp-tasks.
