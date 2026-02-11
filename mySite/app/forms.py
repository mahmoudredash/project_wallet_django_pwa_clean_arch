 from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Expense, Income, Category


class RegistationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date_received', 'category', 'description']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date_incurred', 'category', 'receipt_image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']


class UpdateForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    description = forms.CharField(max_length=255, required=True, label='Description', widget=forms.Textarea(attrs={'rows': 4}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True,label='Category')
