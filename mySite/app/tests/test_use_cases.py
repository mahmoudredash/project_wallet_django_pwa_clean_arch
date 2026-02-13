import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import Mock
from app.domain.entities import Category, Income, Expense, CategoryType
from app.domain.repositories import CategoryRepository, IncomeRepository, ExpenseRepository
from app.application.use_cases import (
    CreateCategoryUseCase, CreateIncomeUseCase, CreateExpenseUseCase
)

class MockCategoryRepository(CategoryRepository):
    def __init__(self):
        self.categories = []
    
    def get_by_id(self, category_id):
        return next((c for c in self.categories if c.id == category_id), None)
    
    def get_all_by_user(self, user_id):
        return [c for c in self.categories if c.user_id == user_id]
    
    def save(self, category):
        if category.id is None:
            category.id = len(self.categories) + 1
        self.categories.append(category)
        return category
    
    def delete(self, category_id):
        self.categories = [c for c in self.categories if c.id != category_id]

class MockIncomeRepository(IncomeRepository):
    def __init__(self):
        self.incomes = []
    
    def get_by_id(self, income_id):
        return next((i for i in self.incomes if i.id == income_id), None)
    
    def get_all_by_user(self, user_id):
        return [i for i in self.incomes if i.user_id == user_id]
    
    def save(self, income):
        if income.id is None:
            income.id = len(self.incomes) + 1
        self.incomes.append(income)
        return income
    
    def delete(self, income_id):
        self.incomes = [i for i in self.incomes if i.id != income_id]

class MockExpenseRepository(ExpenseRepository):
    def __init__(self):
        self.expenses = []
    
    def get_by_id(self, expense_id):
        return next((e for e in self.expenses if e.id == expense_id), None)
    
    def get_all_by_user(self, user_id):
        return [e for e in self.expenses if e.user_id == user_id]
    
    def save(self, expense):
        if expense.id is None:
            expense.id = len(self.expenses) + 1
        self.expenses.append(expense)
        return expense
    
    def delete(self, expense_id):
        self.expenses = [e for e in self.expenses if e.id != expense_id]

class TestUseCases(unittest.TestCase):
    
    def setUp(self):
        self.category_repo = MockCategoryRepository()
        self.income_repo = MockIncomeRepository()
        self.expense_repo = MockExpenseRepository()
    
    def test_create_category_use_case(self):
        use_case = CreateCategoryUseCase(self.category_repo)
        category = use_case.execute(user_id=1, name="Test Category", type=CategoryType.INCOME)
        
        self.assertEqual(category.user_id, 1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.type, CategoryType.INCOME)
        self.assertIsNotNone(category.id)
    
    def test_create_income_use_case(self):
        category_repo = MockCategoryRepository()
        category = Category(id=1, user_id=1, name="Test Category", type=CategoryType.INCOME)
        category_repo.save(category)
        
        use_case = CreateIncomeUseCase(self.income_repo, category_repo)
        income = use_case.execute(
            user_id=1,
            amount=Decimal("100.00"),
            source="Test Source",
            date_received=date.today(),
            category_id=1,
            description="Test Income"
        )
        
        self.assertEqual(income.user_id, 1)
        self.assertEqual(income.amount, Decimal("100.00"))
        self.assertEqual(income.source, "Test Source")
        self.assertEqual(income.category.id, 1)
    
    def test_create_expense_use_case(self):
        category_repo = MockCategoryRepository()
        category = Category(id=1, user_id=1, name="Test Category", type=CategoryType.EXPENSE)
        category_repo.save(category)
        
        use_case = CreateExpenseUseCase(self.expense_repo, category_repo)
        expense = use_case.execute(
            user_id=1,
            amount=Decimal("50.00"),
            category_id=1,
            date_incurred=date.today(),
            description="Test Expense"
        )
        
        self.assertEqual(expense.user_id, 1)
        self.assertEqual(expense.amount, Decimal("50.00"))
        self.assertEqual(expense.category.id, 1)

if __name__ == '__main__':
    unittest.main()