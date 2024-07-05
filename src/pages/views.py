from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from urllib.parse import urlencode
from django.db import connection
import logging

logger = logging.getLogger(__name__)

@login_required
def createView(request):

    '''  Fix to flaw 3: 
    # if request.method == 'POST':
        # newpassword = request.POST.get('password')
        # newpassword2 = request.POST.get('password2')
        # iban = request.POST.get('iban')
    '''

    if request.method == 'GET':
        newpassword = request.GET.get('password')
        newpassword2 = request.GET.get('password2')
        iban = request.GET.get('iban')

        """  Fix to flaw 1 & 4 combined:
        if len(newpassword) < 12 or not any(char.isdigit() for char in newpassword) or not any(char.isupper() for char in newpassword) or not any(char.islower() for char in newpassword):
            messages.error(request, "Password must be at least 12 characters long and contain at least one uppercase letter, one lowercase letter and one digit.")
            
            # Fix to flaw 4:
            # logger.warning('Password must be at least 12 characters long and contain at least one uppercase letter, one lowercase letter and one digit')

            return redirect('/')

        if newpassword != request.user.username:
            messages.error(request, "Password must be the same as your username.")

            # Fix to flaw 4:
            # logger.warning('Password must be the same as your username')

            return redirect('/')
        """

        if newpassword != newpassword2:
            messages.error(request, "Passwords do not match.")

            # Fix to flaw 4:
            # logger.warning('Passwords do not match')

            return redirect('/')
        

        if len(iban) < 10 or len(iban) > 30:
            messages.error(request, "IBAN must be between 10 and 30 characters long.")

            # Fix to flaw 4:
            # logger.warning('IBAN must be between 10 and 30 characters long')

            return redirect('/')

        if Account.objects.filter(iban=iban).exists():

            # Fix to flaw 4:
            # logger.warning('IBAN already exists')

            messages.error(request, "IBAN already exists.")
            return redirect('/')

        if Account.objects.filter(owner=request.user).count() >= 3:
            messages.error(request, "You can't have more than 3 accounts.")

            # Fix to flaw 4:
            # logger.warning('You can't have more than 3 accounts')

            return redirect('/')

        Account.objects.create(owner=request.user, iban=iban, password=newpassword)
        messages.success(request, "Account created successfully!")  

        # Fix to flaw 4:
        # logger.info('Account created successfully!')
        
        # Vulnerable because of Flaw 3, Sensitive Data Exposure if GET method is used
        params = urlencode({'password': newpassword, 'iban': iban})
        return redirect(f'/?{params}')

        """Fix to flaw 3:
        return redirect('/')"""
        

@login_required
def addView(request):
    # if request.method == 'POST':
    if request.method == 'GET':
        iban = request.GET.get('to')
        amount = int(request.GET.get('amount', 0))  # Default to 0 if 'amount' is not provided or invalid
        
		# iban = request.POST.get('to')
        # amount = int(request.POST.get('amount', 0))
        # Vulnerable to SQL injection
 
        query = f"UPDATE Account SET balance = balance + {amount} WHERE iban = '{iban}'"
        with connection.cursor() as cursor:
            cursor.execute(query)

        messages.success(request, "Money added successfully!")

        '''Fix to flaw 2, 4 and 5 combined
        try:
            # Vulnerable to Flaw 5: Broken Access Control
            # account = Account.objects.get(iban=iban)
            
            # Fix to flaw 5: Broken Access Control
            # # try:
            #     account = Account.objects.get(iban=iban, owner=request.user)
            # except Account.DoesNotExist:
            #     messages.error(request, "Account with the provided IBAN does not exist or does not belong to you.")

            # Fix to flaw 4:
            # logger.warning('Account with the provided IBAN does not exist or does not belong to the user')

            #     return redirect('/')  

        except Account.DoesNotExist:
            messages.error(request, "Account with the provided IBAN does not exist.")
            return redirect('/')

        # Fix to flaw 2: SQL Injection, using Django ORM instead of raw SQL for updating the balance
        if amount > 0:
            account.balance += amount
            account.save()
            messages.success(request, "Money added successfully!")
        else:
            messages.error(request, "Amount must be a positive number.")
        '''

    return redirect('/')

@login_required
def deleteView(request):
    # if request.method == 'POST':
    if request.method == 'GET':
        iban = request.GET.get('iban')

        account = Account.objects.get(iban=iban)

        # Vulnerable to Flaw 5: Broken Access Control
        # account = Account.objects.get(iban=iban, owner=request.user)   

        if account.owner != request.user:
            messages.error(request, "You can only delete your own accounts.")
            # Fix to flaw 4:
            # logger.warning('You can only delete your own accounts')
            return redirect('/')

        if account.balance != 0:
            user = Account.objects.filter(owner=request.user)
            if user.count() == 1:
                messages.error(request, "You can't delete your last account if it has a balance.")
                # Fix to flaw 4:
                # logger.warning('You can't delete your last account if it has a balance')
                return redirect('/')
            elif user.count() == 2:
                other_account = user.exclude(iban=iban).first()
                other_account.balance += account.balance
                other_account.save()
                messages.success(request, "Balance transferred successfully!")
                # Fix to flaw 4:
                # logger.info('Balance transferred successfully')
            else:
                other_accounts = user.exclude(iban=iban)
                amount = account.balance // other_accounts.count()
                for other_account in other_accounts:
                    other_account.balance += amount
                    other_account.save()
                messages.success(request, "Balance split successfully!")
                # Fix to flaw 4:
                # logger.info('Balance split successfully')

         
        account.delete()
        messages.success(request, "Account deleted successfully!")
        return redirect('/')

    return redirect('/')

@login_required
def homePageView(request):
    logger.debug('Debug message: Inside homePageView')
    
    accounts = Account.objects.filter(owner=request.user)
    logger.debug(f'Accounts retrieved: {accounts}')

    x = {'accounts': accounts}
    return render(request, 'pages/index.html', x)
