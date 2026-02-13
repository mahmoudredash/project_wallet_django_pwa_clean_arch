from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime, date

from app.application.use_cases import (
    CreateCategoryUseCase, GetCategoryUseCase, GetAllCategoriesByUserUseCase,
    UpdateCategoryUseCase, DeleteCategoryUseCase,
    CreateIncomeUseCase, GetIncomeUseCase, GetAllIncomesByUserUseCase,
    UpdateIncomeUseCase, DeleteIncomeUseCase,
    CreateExpenseUseCase, GetExpenseUseCase, GetAllExpensesByUserUseCase,
    UpdateExpenseUseCase, DeleteExpenseUseCase
)
from app.infrastructure.repositories import (
    DjangoCategoryRepository, DjangoIncomeRepository, DjangoExpenseRepository
)
from app.interfaces.dto import CategoryDTO, IncomeDTO, ExpenseDTO

# Initialize repositories
category_repo = DjangoCategoryRepository()
income_repo = DjangoIncomeRepository()
expense_repo = DjangoExpenseRepository()

# Initialize use cases
create_category_uc = CreateCategoryUseCase(category_repo)
get_category_uc = GetCategoryUseCase(category_repo)
get_all_categories_uc = GetAllCategoriesByUserUseCase(category_repo)
update_category_uc = UpdateCategoryUseCase(category_repo)
delete_category_uc = DeleteCategoryUseCase(category_repo)

create_income_uc = CreateIncomeUseCase(income_repo, category_repo)
get_income_uc = GetIncomeUseCase(income_repo)
get_all_incomes_uc = GetAllIncomesByUserUseCase(income_repo)
update_income_uc = UpdateIncomeUseCase(income_repo, category_repo)
delete_income_uc = DeleteIncomeUseCase(income_repo)

create_expense_uc = CreateExpenseUseCase(expense_repo, category_repo)
get_expense_uc = GetExpenseUseCase(expense_repo)
get_all_expenses_uc = GetAllExpensesByUserUseCase(expense_repo)
update_expense_uc = UpdateExpenseUseCase(expense_repo, category_repo)
delete_expense_uc = DeleteExpenseUseCase(expense_repo)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if username and email and password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return JsonResponse({'message': 'Registration successful', 'success': True})
        return JsonResponse({'message': 'All fields are required', 'success': False})
    return redirect('index')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'success': True})
        return JsonResponse({'message': 'Invalid credentials', 'success': False})
    return redirect('index')


@login_required
def log_out(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful', 'success': True})


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
    }
    return render(request=request, template_name='app/general/index.html', context=context)


@login_required
def dashboard(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    income_monthly_data = {}
    expense_monthly_data = {}

    for month in months:
        income_monthly_data[month] = 0
        expense_monthly_data[month] = 0

    incomes = get_all_incomes_uc.execute(request.user.id)
    for income in incomes:
        month = income.date_received.strftime('%b')
        income_monthly_data[month] += float(income.amount)

    expenses = get_all_expenses_uc.execute(request.user.id)
    for expense in expenses:
        month = expense.date_incurred.strftime('%b')
        expense_monthly_data[month] += float(expense.amount)

    income_data = [float(x) for x in income_monthly_data.values()]
    expense_data = [-float(x) if x > 0 else float(x) for x in expense_monthly_data.values()]

    total_income = sum(income_data)
    total_expense = sum(expense_data)
    current_balance = total_income + total_expense

    categories = get_all_categories_uc.execute(request.user.id)

    context = {
        'income_data': income_data,
        'expense_data': expense_data,
        'total_income': total_income,
        'total_expense': total_expense,
        'current_balance': current_balance,
        'months': months,
        'categories': categories,
    }
    return render(request=request, template_name='app/dashboard/dashboard.html', context=context)


@csrf_exempt
@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')

        if name and type:
            try:
                category = create_category_uc.execute(request.user.id, name, type)
                return JsonResponse({
                    'message': 'Category created successfully',
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name,
                        'type': category.type
                    }
                })
            except Exception as e:
                return JsonResponse({'message': str(e), 'success': False})
        return JsonResponse({'message': 'Name and type are required', 'success': False})


@csrf_exempt
@login_required
def create_income(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        source = request.POST.get('source')
        date_received = request.POST.get('date_received')
        category_id = request.POST.get('category_id')
        description = request.POST.get('description')

        if amount and source and date_received:
            try:
                income = create_income_uc.execute(
                    request.user.id,
                    Decimal(amount),
                    source,
                    datetime.strptime(date_received, '%Y-%m-%d').date(),
                    int(category_id) if category_id else None,
                    description
                )
                return JsonResponse({
                    'message': 'Income created successfully',
                    'success': True,
                    'income': {
                        'id': income.id,
                        'amount': float(income.amount),
                        'source': income.source,
                        'date_received': income.date_received.isoformat(),
                        'category_id': income.category.id if income.category else None,
                        'description': income.description
                    }
                })
            except Exception as e:
                return JsonResponse({'message': str(e), 'success': False})
        return JsonResponse({'message': 'Amount, source and date are required', 'success': False})


@csrf_exempt
@login_required
def create_expense(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category_id = request.POST.get('category_id')
        date_incurred = request.POST.get('date_incurred')
        description = request.POST.get('description')
        receipt_image = request.POST.get('receipt_image')

        if amount and date_incurred:
            try:
                expense = create_expense_uc.execute(
                    request.user.id,
                    Decimal(amount),
                    int(category_id) if category_id else None,
                    datetime.strptime(date_incurred, '%Y-%m-%d').date(),
                    description,
                    receipt_image
                )
                return JsonResponse({
                    'message': 'Expense created successfully',
                    'success': True,
                    'expense': {
                        'id': expense.id,
                        'amount': float(expense.amount),
                        'category_id': expense.category.id if expense.category else None,
                        'date_incurred': expense.date_incurred.isoformat(),
                        'description': expense.description,
                        'receipt_image': expense.receipt_image
                    }
                })
            except Exception as e:
                return JsonResponse({'message': str(e), 'success': False})
        return JsonResponse({'message': 'Amount and date are required', 'success': False})


@csrf_exempt
@login_required
def get_categories(request):
    if request.method == 'GET':
        try:
            categories = get_all_categories_uc.execute(request.user.id)
            categories_data = [{
                'id': cat.id,
                'name': cat.name,
                'type': cat.type
            } for cat in categories]
            return JsonResponse({
                'message': 'Categories retrieved successfully',
                'success': True,
                'categories': categories_data
            })
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False})


@csrf_exempt
@login_required
def get_incomes(request):
    if request.method == 'GET':
        try:
            incomes = get_all_incomes_uc.execute(request.user.id)
            incomes_data = [{
                'id': inc.id,
                'amount': float(inc.amount),
                'source': inc.source,
                'date_received': inc.date_received.isoformat(),
                'category_id': inc.category.id if inc.category else None,
                'description': inc.description,
                'date_created': inc.date_created.isoformat() if inc.date_created else None,
                'date_updated': inc.date_updated.isoformat() if inc.date_updated else None
            } for inc in incomes]
            return JsonResponse({
                'message': 'Incomes retrieved successfully',
                'success': True,
                'incomes': incomes_data
            })
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False})


@csrf_exempt
@login_required
def get_expenses(request):
    if request.method == 'GET':
        try:
            expenses = get_all_expenses_uc.execute(request.user.id)
            expenses_data = [{
                'id': exp.id,
                'amount': float(exp.amount),
                'category_id': exp.category.id if exp.category else None,
                'date_incurred': exp.date_incurred.isoformat(),
                'description': exp.description,
                'receipt_image': exp.receipt_image,
                'date_created': exp.date_created.isoformat() if exp.date_created else None,
                'date_updated': exp.date_updated.isoformat() if exp.date_updated else None
            } for exp in expenses]
            return JsonResponse({
                'message': 'Expenses retrieved successfully',
                'success': True,
                'expenses': expenses_data
            })
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False})


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
