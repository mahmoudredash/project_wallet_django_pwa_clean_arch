from datetime import date, datetime
from decimal import Decimal
from typing import List, Literal, Optional

from app.domain.entities import Category, Income, Expense, CategoryType
from app.domain.repositories import CategoryRepository, IncomeRepository, ExpenseRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repo = category_repository

    def execute(self, user_id: int, name: str, type: Literal[CategoryType.INCOME, CategoryType.EXPENSE]) -> Category:
        category = Category(id=None, user_id=user_id, name=name, type=type)
        return self.category_repo.save(category)


class GetCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repo = category_repository

    def execute(self, category_id: int) -> Optional[Category]:
        return self.category_repo.get_by_id(category_id)


class GetAllCategoriesByUserUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repo = category_repository

    def execute(self, user_id: int) -> List[Category]:
        return self.category_repo.get_all_by_user(user_id)


class UpdateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repo = category_repository

    def execute(self, category_id: int, user_id: int, name: str, type: Literal[CategoryType.INCOME, CategoryType.EXPENSE]) -> Category:
        category = Category(id=category_id, user_id=user_id, name=name, type=type)
        return self.category_repo.save(category)


class DeleteCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repo = category_repository

    def execute(self, category_id: int):
        self.category_repo.delete(category_id)


class CreateIncomeUseCase:
    def __init__(self, income_repository: IncomeRepository, category_repository: CategoryRepository):
        self.income_repo = income_repository
        self.category_repo = category_repository

    def execute(self, user_id: int, amount: Decimal, source: str, date_received: date, category_id: Optional[int], description: Optional[str]) -> Income:
        category = self.category_repo.get_by_id(category_id) if category_id else None
        income = Income(id=None, user_id=user_id, amount=amount, source=source, date_received=date_received, category=category, description=description)
        return self.income_repo.save(income)


class GetIncomeUseCase:
    def __init__(self, income_repository: IncomeRepository):
        self.income_repo = income_repository

    def execute(self, income_id: int) -> Optional[Income]:
        return self.income_repo.get_by_id(income_id)


class GetAllIncomesByUserUseCase:
    def __init__(self, income_repository: IncomeRepository):
        self.income_repo = income_repository

    def execute(self, user_id: int) -> List[Income]:
        return self.income_repo.get_all_by_user(user_id)


class UpdateIncomeUseCase:
    def __init__(self, income_repository: IncomeRepository, category_repository: CategoryRepository):
        self.income_repo = income_repository
        self.category_repo = category_repository

    def execute(self, income_id: int, user_id: int, amount: Decimal, source: str, date_received: date, category_id: Optional[int], description: Optional[str]) -> Income:
        category = self.category_repo.get_by_id(category_id) if category_id else None
        income = Income(id=income_id, user_id=user_id, amount=amount, source=source, date_received=date_received, category=category, description=description)
        return self.income_repo.save(income)


class DeleteIncomeUseCase:
    def __init__(self, income_repository: IncomeRepository):
        self.income_repo = income_repository

    def execute(self, income_id: int):
        self.income_repo.delete(income_id)


class CreateExpenseUseCase:
    def __init__(self, expense_repository: ExpenseRepository, category_repository: CategoryRepository):
        self.expense_repo = expense_repository
        self.category_repo = category_repository

    def execute(self, user_id: int, amount: Decimal, category_id: Optional[int], date_incurred: date, description: Optional[str], receipt_image: Optional[str]) -> Expense:
        category = self.category_repo.get_by_id(category_id) if category_id else None
        expense = Expense(id=None, user_id=user_id, amount=amount, category=category, date_incurred=date_incurred, description=description, receipt_image=receipt_image)
        return self.expense_repo.save(expense)


class GetExpenseUseCase:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repo = expense_repository

    def execute(self, expense_id: int) -> Optional[Expense]:
        return self.expense_repo.get_by_id(expense_id)


class GetAllExpensesByUserUseCase:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repo = expense_repository

    def execute(self, user_id: int) -> List[Expense]:
        return self.expense_repo.get_all_by_user(user_id)


class UpdateExpenseUseCase:
    def __init__(self, expense_repository: ExpenseRepository, category_repository: CategoryRepository):
        self.expense_repo = expense_repository
        self.category_repo = category_repository

    def execute(self, expense_id: int, user_id: int, amount: Decimal, category_id: Optional[int], date_incurred: date, description: Optional[str], receipt_image: Optional[str]) -> Expense:
        category = self.category_repo.get_by_id(category_id) if category_id else None
        expense = Expense(id=expense_id, user_id=user_id, amount=amount, category=category, date_incurred=date_incurred, description=description, receipt_image=receipt_image)
        return self.expense_repo.save(expense)


class DeleteExpenseUseCase:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repo = expense_repository

    def execute(self, expense_id: int):
        self.expense_repo.delete(expense_id)
