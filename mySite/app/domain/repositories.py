from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Category, Income, Expense


class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[Category]:
        pass

    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, category_id: int):
        pass


class IncomeRepository(ABC):
    @abstractmethod
    def get_by_id(self, income_id: int) -> Optional[Income]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[Income]:
        pass

    @abstractmethod
    def save(self, income: Income) -> Income:
        pass

    @abstractmethod
    def delete(self, income_id: int):
        pass


class ExpenseRepository(ABC):
    @abstractmethod
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[Expense]:
        pass

    @abstractmethod
    def save(self, expense: Expense) -> Expense:
        pass

    @abstractmethod
    def delete(self, expense_id: int):
        pass
