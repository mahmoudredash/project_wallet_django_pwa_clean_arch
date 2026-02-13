from typing import List, Optional
from django.contrib.auth.models import User

from app.domain.entities import Category, Income, Expense, CategoryType
from app.domain.repositories import CategoryRepository, IncomeRepository, ExpenseRepository
from app.infrastructure.models import Category as DjangoCategory, Income as DjangoIncome, Expense as DjangoExpense


class DjangoCategoryRepository(CategoryRepository):
    def get_by_id(self, category_id: int) -> Optional[Category]:
        try:
            django_category = DjangoCategory.objects.get(id=category_id)
            return self._to_domain_entity(django_category)
        except DjangoCategory.DoesNotExist:
            return None

    def get_all_by_user(self, user_id: int) -> List[Category]:
        django_categories = DjangoCategory.objects.filter(user_id=user_id)
        return [self._to_domain_entity(dc) for dc in django_categories]

    def save(self, category: Category) -> Category:
        if category.id:
            django_category = DjangoCategory.objects.get(id=category.id)
            django_category.name = category.name
            django_category.type = category.type
            django_category.save()
        else:
            user = User.objects.get(id=category.user_id)
            django_category = DjangoCategory.objects.create(
                user=user,
                name=category.name,
                type=category.type
            )
            category.id = django_category.id
        return category

    def delete(self, category_id: int):
        DjangoCategory.objects.filter(id=category_id).delete()

    def _to_domain_entity(self, django_category: DjangoCategory) -> Category:
        return Category(
            id=django_category.id,
            user_id=django_category.user.id,
            name=django_category.name,
            type=django_category.type
        )


class DjangoIncomeRepository(IncomeRepository):
    def get_by_id(self, income_id: int) -> Optional[Income]:
        try:
            django_income = DjangoIncome.objects.get(id=income_id)
            return self._to_domain_entity(django_income)
        except DjangoIncome.DoesNotExist:
            return None

    def get_all_by_user(self, user_id: int) -> List[Income]:
        django_incomes = DjangoIncome.objects.filter(user_id=user_id)
        return [self._to_domain_entity(di) for di in django_incomes]

    def save(self, income: Income) -> Income:
        if income.id:
            django_income = DjangoIncome.objects.get(id=income.id)
            django_income.amount = income.amount
            django_income.source = income.source
            django_income.date_received = income.date_received
            django_income.category = DjangoCategory.objects.get(id=income.category.id) if income.category else None
            django_income.description = income.description
            django_income.save()
        else:
            user = User.objects.get(id=income.user_id)
            django_income = DjangoIncome.objects.create(
                user=user,
                amount=income.amount,
                source=income.source,
                date_received=income.date_received,
                category=DjangoCategory.objects.get(id=income.category.id) if income.category else None,
                description=income.description
            )
            income.id = django_income.id
        return income

    def delete(self, income_id: int):
        DjangoIncome.objects.filter(id=income_id).delete()

    def _to_domain_entity(self, django_income: DjangoIncome) -> Income:
        category = DjangoCategoryRepository().get_by_id(django_income.category.id) if django_income.category else None
        return Income(
            id=django_income.id,
            user_id=django_income.user.id,
            amount=django_income.amount,
            source=django_income.source,
            date_received=django_income.date_received,
            category=category,
            description=django_income.description,
            date_created=django_income.date_created,
            date_updated=django_income.date_updated
        )


class DjangoExpenseRepository(ExpenseRepository):
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        try:
            django_expense = DjangoExpense.objects.get(id=expense_id)
            return self._to_domain_entity(django_expense)
        except DjangoExpense.DoesNotExist:
            return None

    def get_all_by_user(self, user_id: int) -> List[Expense]:
        django_expenses = DjangoExpense.objects.filter(user_id=user_id)
        return [self._to_domain_entity(de) for de in django_expenses]

    def save(self, expense: Expense) -> Expense:
        if expense.id:
            django_expense = DjangoExpense.objects.get(id=expense.id)
            django_expense.amount = expense.amount
            django_expense.category = DjangoCategory.objects.get(id=expense.category.id) if expense.category else None
            django_expense.date_incurred = expense.date_incurred
            django_expense.description = expense.description
            django_expense.receipt_image = expense.receipt_image
            django_expense.save()
        else:
            user = User.objects.get(id=expense.user_id)
            django_expense = DjangoExpense.objects.create(
                user=user,
                amount=expense.amount,
                category=DjangoCategory.objects.get(id=expense.category.id) if expense.category else None,
                date_incurred=expense.date_incurred,
                description=expense.description,
                receipt_image=expense.receipt_image
            )
            expense.id = django_expense.id
        return expense

    def delete(self, expense_id: int):
        DjangoExpense.objects.filter(id=expense_id).delete()

    def _to_domain_entity(self, django_expense: DjangoExpense) -> Expense:
        category = DjangoCategoryRepository().get_by_id(django_expense.category.id) if django_expense.category else None
        return Expense(
            id=django_expense.id,
            user_id=django_expense.user.id,
            amount=django_expense.amount,
            category=category,
            date_incurred=django_expense.date_incurred,
            description=django_expense.description,
            receipt_image=django_expense.receipt_image,
            date_created=django_expense.date_created,
            date_updated=django_expense.date_updated
        )
