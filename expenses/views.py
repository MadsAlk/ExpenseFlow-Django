from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages 
# Create your views here.

@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner = request.user)
    context = {
        'expenses': expenses
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):  
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'filled': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    

    
    amount = request.POST['amount']
    description = request.POST['description']
    category = request.POST['category']
    date = request.POST['date']
    owner = request.user
    

    if not amount:
        messages.error(request, 'Amount is required')
    elif not category:
        messages.error(request, 'Category is required')
    else:
        if not date:
            Expense.objects.create(amount=amount, description=description, category=category, owner=owner )
        else:
            Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=owner )
        messages.success(request, 'Expense added successfully')
        return redirect('expenses')

    return render(request, 'expenses/add_expense.html', context)



def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)

    categories = Category.objects.all()
    context = {
        'filled': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    amount = request.POST['amount']
    description = request.POST['description']
    category = request.POST['category']
    date = request.POST['date']
    
    if not amount:
        messages.error(request, 'Amount is required')
    elif not category:
        messages.error(request, 'Category is required')
    else:
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, 'Expense updated successfully')

    return render(request, 'expenses/edit_expense.html', context)


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    return redirect('expenses')
