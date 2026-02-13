# Domain Layer Rules

- No Django imports allowed.
- Entities must be plain Python classes.
- Value Objects must be immutable.
- Business rules live here only.
- No database logic here.
- No HTTP logic here.

Example:

✔ Good:
class Task:
    def complete(self):
        self.completed = True

✘ Bad:
from django.db import models
class Task(models.Model):
    