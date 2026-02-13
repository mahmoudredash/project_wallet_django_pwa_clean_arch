from django.urls import path
from .views import (
    register, log_in, log_out, index, dashboard,
    create_income, create_expense, create_category,
    get_incomes, get_expenses, get_categories
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', log_in, name='log_in'),
    path('logout/', log_out, name='log_out'),
    path('index/', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/create-income/', create_income, name='create_income'),
    path('api/create-expense/', create_expense, name='create_expense'),
    path('api/create-category/', create_category, name='create_category'),
    path('api/get-incomes/', get_incomes, name='get_incomes'),
    path('api/get-expenses/', get_expenses, name='get_expenses'),
    path('api/get-categories/', get_categories, name='get_categories'),
]
