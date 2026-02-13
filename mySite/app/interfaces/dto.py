from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class CategoryDTO:
    id: Optional[int]
    user_id: int
    name: str
    type: str

@dataclass
class IncomeDTO:
    id: Optional[int]
    user_id: int
    amount: Decimal
    source: str
    date_received: date
    category_id: Optional[int]
    description: Optional[str]
    date_created: Optional[date]
    date_updated: Optional[date]

@dataclass
class ExpenseDTO:
    id: Optional[int]
    user_id: int
    amount: Decimal
    category_id: Optional[int]
    date_incurred: date
    description: Optional[str]
    receipt_image: Optional[str]
    date_created: Optional[date]
    date_updated: Optional[date]

@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str