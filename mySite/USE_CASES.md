# Application Layer - Use Case Rules

Each use case:

- One class per use case
- Must have execute() method
- Receives dependencies via constructor
- No direct ORM usage
- Returns DTO or entity

Example:

class CreateTaskUseCase:
    def __init__(self, task_repository):
        self.repo = task_repository

    def execute(self, data):
        task = Task(**data)
        self.repo.save(task)
        return task
