from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import IncomeForm, ExpenseForm, CategoryForm, RegistationForm, UpdateForm
from .models import Income, Expense, Category
from itertools import chain
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'message': 'Registration successful','success': True})
    return redirect('index')

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful','success': True})
        return JsonResponse({'message': 'Invalid credentials','success': False})
    return redirect('index')


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    registeration_form = RegistationForm()
    login_form = AuthenticationForm()

    context = {
        'registeration_form': registeration_form,
        'login_form': login_form,
    }
    return render(request=request, template_name='app/general/index.html', context=context)


@login_required
def dashboard(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    income_form = IncomeForm()
    expense_form = ExpenseForm()
    category_form = CategoryForm()
    update_form = UpdateForm()

    income_monthly_data = {}
    expense_monthly_data = {}

    for month in months:
        income_monthly_data[month] = Income.objects.filter(user=request.user, date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0
        expense_monthly_data[month] = Expense.objects.filter(user=request.user, date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0

    incomes = Income.objects.filter(user=request.user)

    for income in incomes:
        month = income.date_received.strftime('%b')

        income_monthly_data[month] += income.amount

    income_data =  [float(x) for x in income_monthly_data.values()]

    expenses = Expense.objects.filter(user=request.user)

    for expense in expenses:
        month = expense.date_received.strftime('%b')

        expense_monthly_data[month] += expense.amount

    expense_data =  [-float(x) if x > 0 else float(x) for x in expense_monthly_data.values()]

    combined_records = list(chain(income_data, expense_data))

    sorted_records = sorted(combined_records, key=lambda x: x.created_at)

    Categories = Category.objects.filter(user=request.user)

    context = {
        'income_data': income_data,
        'expense_data': expense_data,
        'total_income': sum(income_data),
        'total_expense': sum(expense_data),
        'current_balance': sum(sum(income_data) , sum(expense_data)),
        'months': months,
        'income_form': income_form,
        'expense_form': expense_form,
        'category_form': category_form,
        'update_form': update_form,
        'incomes': incomes,
        'expenses': expenses,
        'categories': Categories,
        'sorted_records': sorted_records,
    }

    return render(request=request, template_name='app/general/dashboard.html', context=context)
