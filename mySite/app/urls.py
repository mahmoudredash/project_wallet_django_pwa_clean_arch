from django.urls import path
from .views import (register,log_in,index,dashboard,create_income,create_expense,create_category,delete_income,delete_expense,delete_category,update_record)

urlpatterns = [
    path('sing-up/', register, name='register'),
    path('log-in/', log_in, name='log_in'),
    path('log-out/', log_out, name='log_out'),
    path('index/', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/update/<slug:record_type>/<int:record_id>/', dashboard, name='update_record'),
    path('create-income/', create_income, name='create_income'),
    path('create-expense/', create_expense, name='create_expense'),
    path('create-category/', create_category, name='create_category'),
    path('delete-income/<int:id>/', delete_income, name='delete_income'),
    path('delete-expense/<int:id>/', delete_expense, name='delete_expense'),
    path('delete-category/<int:id>/', delete_category, name='delete_category'),
    # path('update-record/<int:id>/', update_record, name='update_record'),
]
