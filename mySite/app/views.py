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

@login_required
def log_out(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful','success': True})

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


@login_required
def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return JsonResponse({'message': 'Income created successfully', 'success': True})
        else:
            return JsonResponse({'message': 'Invalid form data', 'success': False})

    return JsonResponse({'message': 'Invalid request method', 'success': False})




@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return JsonResponse({'message': 'Expense created successfully', 'success': True})
        else:
            return JsonResponse({'message': 'Invalid form data', 'success': False})

    return JsonResponse({'message': 'Invalid request method', 'success': False})


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return JsonResponse({'message': 'Category created successfully', 'success': True})
        else:
            return JsonResponse({'message': 'Invalid form data', 'success': False})

    return JsonResponse({'message': 'Invalid request method', 'success': False})


@login_required
def delete_income(request, income_id):
    if request.method == 'DELETE':
        try:
            income = Income.objects.get(id=income_id, user=request.user)
            income.delete()
            return JsonResponse({'message': 'Income deleted successfully', 'success': True})
        except Income.DoesNotExist:
            return JsonResponse({'message': 'Income not found', 'success': False})


@login_required
def delete_expense(request, expense_id):
    if request.method == 'DELETE':
        try:
            expense = Expense.objects.get(id=expense_id, user=request.user)
            expense.delete()
            return JsonResponse({'message': 'Expense deleted successfully', 'success': True})
        except Expense.DoesNotExist:
            return JsonResponse({'message': 'Expense not found', 'success': False})

@login_required
def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            category.delete()
            return JsonResponse({'message': 'Category deleted successfully', 'success': True})
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found', 'success': False})



@login_required
def update_record(request, record_type, record_id):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if record_type == 'income':
            got_income = Income.objects.filter(user=request.user, id=record_id).last()

            if form.is_valid() and got_income:
                got_income.amount = form.cleaned_data['amount']
                got_income.description = form.cleaned_data['description']
                got_income.category = form.cleaned_data['category']
                got_income.save()
                return JsonResponse({'message': 'Income updated successfully', 'success': True})
        elif record_type == 'expense':
            got_expense = Expense.objects.filter(user=request.user, id=record_id).last()

            if form.is_valid() and got_expense:
                got_expense.amount = form.cleaned_data['amount']
                got_expense.description = form.cleaned_data['description']
                got_expense.category = form.cleaned_data['category']
                got_expense.save()
                return JsonResponse({'message': 'Expense updated successfully', 'success': True})
        elif record_type == 'category':
            got_category = Category.objects.filter(user=request.user, id=record_id).last()

            if form.is_valid() and got_category:
                got_category.name = form.cleaned_data['name']
                got_category.save()
                return JsonResponse({'message': 'Category updated successfully', 'success': True})
        return JsonResponse({'message': 'Record not found', 'success': False})
    return redirect('dashboard')
