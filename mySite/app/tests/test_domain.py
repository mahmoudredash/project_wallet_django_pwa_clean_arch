import unittest
from datetime import date
from decimal import Decimal
from app.domain.entities import Category, Income, Expense, CategoryType

class TestDomainEntities(unittest.TestCase):
    
    def test_category_creation(self):
        category = Category(id=1, user_id=1, name="Test Category", type=CategoryType.INCOME)
        self.assertEqual(category.id, 1)
        self.assertEqual(category.user_id, 1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.type, CategoryType.INCOME)
    
    def test_income_creation(self):
        category = Category(id=1, user_id=1, name="Test Category", type=CategoryType.INCOME)
        income = Income(id=1, user_id=1, amount=Decimal("100.00"), source="Test Source", 
                       date_received=date.today(), category=category, description="Test Income")
        self.assertEqual(income.id, 1)
        self.assertEqual(income.user_id, 1)
        self.assertEqual(income.amount, Decimal("100.00"))
        self.assertEqual(income.source, "Test Source")
        self.assertEqual(income.category, category)
    
    def test_expense_creation(self):
        category = Category(id=1, user_id=1, name="Test Category", type=CategoryType.EXPENSE)
        expense = Expense(id=1, user_id=1, amount=Decimal("50.00"), category=category, 
                         date_incurred=date.today(), description="Test Expense")
        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.user_id, 1)
        self.assertEqual(expense.amount, Decimal("50.00"))
        self.assertEqual(expense.category, category)

if __name__ == '__main__':
    unittest.main()