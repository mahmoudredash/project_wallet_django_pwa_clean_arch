from django.contrib import admin
from app.infrastructure.models import Category, Income, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'source', 'date_received', 'user', 'category')
    list_filter = ('date_received', 'category')
    search_fields = ('source', 'description')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date_incurred', 'user', 'category')
    list_filter = ('date_incurred', 'category')
    search_fields = ('description',)