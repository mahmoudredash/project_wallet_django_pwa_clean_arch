# Repository Pattern

Repositories are defined in Domain.
Implementation exists in Infrastructure.

Domain:

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task): pass

Infrastructure:

class DjangoTaskRepository(TaskRepository):
    def save(self, task):
        # convert entity to Django model
        pass
