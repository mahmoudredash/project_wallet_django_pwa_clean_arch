from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

class CategoryType:
    INCOME = "income"
    EXPENSE = "expense"

class Category:
    def __init__(self, id: Optional[int], user_id: int, name: str, type: Literal[CategoryType.INCOME, CategoryType.EXPENSE]):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.type = type

class Income:
    def __init__(self, id: Optional[int], user_id: int, amount: Decimal, source: str, date_received: date, category: Optional[Category], description: Optional[str], date_created: Optional[datetime] = None, date_updated: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.source = source
        self.date_received = date_received
        self.category = category
        self.description = description
        self.date_created = date_created if date_created else datetime.now()
        self.date_updated = date_updated if date_updated else datetime.now()

class Expense:
    def __init__(self, id: Optional[int], user_id: int, amount: Decimal, category: Optional[Category], date_incurred: date, description: Optional[str], receipt_image: Optional[str], date_created: Optional[datetime] = None, date_updated: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date_incurred = date_incurred
        self.description = description
        self.receipt_image = receipt_image
        self.date_created = date_created if date_created else datetime.now()
        self.date_updated = date_updated if date_updated else datetime.now()
