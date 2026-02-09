from django.contrib import admin

# Register your models here.
from .models import  Expense, Income, Category

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount', 'category', 'description' ,'date_received' )
    list_filter = ('date_received', 'category')
    search_fields = ('user','amount','category')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'description' , 'date_incurred', 'receipt_image')
    list_filter = ('date_incurred', 'category')
    search_fields = ('user','amount','category','description','date_incurred')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','type')
    search_fields = ('name','type')
