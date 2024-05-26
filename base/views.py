from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as mg
from django.contrib.auth.models import auth
from .models import Plan, Transaction, PaymentMethod, Investment, User, Recommendation
from .forms import TransactionForm, InvestmentForm, UserForm, UserForm2
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ObjectDoesNotExist
import math


# Create your views here.
def home(request):
    plans = Plan.objects.all()
    return render(request, 'index.html', {'plans': plans})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            mg.error(request, 'Invalid Username or Password')
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
    transaction = Transaction.objects.filter(user=request.user)
    invests = Investment.objects.filter(user=request.user, is_active=True)
    all_invests = Investment.objects.filter(user=request.user)
    days = timedelta(seconds=120)
    tpercent = 0
    tprofit = 0
    profits = 0

    for trans in transaction:
        if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
            total += trans.amount
        elif trans.status == 'Pending' and trans.transaction_type == 'Deposit':
            pendingDeposit += trans.amount
        else:
            withdrawal += trans.amount

    for value in invests:
        if value.counter >= 7:
            value.profit = ((value.amount) * int(value.plan.percentage) / 100)
            value.is_active = False
            value.save()

        profit += value.profit

        period = (datetime.now(timezone.utc) - value.created)
        period = period.total_seconds()

        ranges = math.floor(period/120)
        # print(ranges, period)

        if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

            tinvest += value.amount

            if ranges > 7:
                value.profit = round(
                    ((value.amount) * int(value.plan.percentage) / 100), 2)
            else:
                if ranges >= 1:
                    value.created = datetime.now(timezone.utc)
                    tpercent += int(value.plan.percentage)

                    profits += round(((value.amount) *
                                     (int(tpercent) / int(value.plan.hours)) / 100), 1)
                value.profit += profits * int(ranges)
            value.counter += ranges

            value.save()

    for x in all_invests:
        allprofit += round(x.profit, 1)

    print(allprofit)

    profit = profits + profit
    tbalance = round(total + allprofit, 2)
    total = total - tinvest
    norm = round(profit, 2)
    context = {'transaction': transaction, 'total': total, 'withdrawal': withdrawal, 'profit': norm,
               'tinvest': tinvest, 'tbalance': tbalance, 'pendingDeposit': pendingDeposit}
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def payment(request):
    methods = PaymentMethod.objects.all()
    context = {'methods': methods}
    return render(request, 'payment.html', context)


@login_required(login_url='login')
def plan(request, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
    transaction = Transaction.objects.filter(user=request.user)
    invests = Investment.objects.filter(user=request.user, is_active=True)
    all_invests = Investment.objects.filter(user=request.user)
    plans = Plan.objects.all()
    days = timedelta(seconds=120)
    tpercent = 0
    tprofit = 0
    profits = 0

    for trans in transaction:
        if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
            total += trans.amount
        elif trans.status == 'Pending' and trans.transaction_type == 'Deposit':
            pendingDeposit += trans.amount
        else:
            withdrawal += trans.amount

    for value in invests:
        if value.counter >= 7:
            value.profit = ((value.amount) * int(value.plan.percentage) / 100)
            value.is_active = False
            value.save()

        profit += value.profit

        period = (datetime.now(timezone.utc) - value.created)
        period = period.total_seconds()

        ranges = math.floor(period/120)
        # print(ranges, period)

        if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

            tinvest += value.amount

            if ranges > 7:
                value.profit = round(
                    ((value.amount) * int(value.plan.percentage) / 100), 2)
            else:
                if ranges >= 1:
                    value.created = datetime.now(timezone.utc)
                    tpercent += int(value.plan.percentage)

                    profits += round(((value.amount) *
                                     (int(tpercent) / int(value.plan.hours)) / 100), 1)
                value.profit += profits * int(ranges)
            value.counter += ranges

            value.save()

    for x in all_invests:
        allprofit += round(x.profit, 1)

    print(allprofit)

    profit = profits + profit
    tbalance = round(total + allprofit, 2)
    total = total - tinvest
    norm = round(profit, 2)
    context = {'transaction': transaction, 'total': total, 'withdrawal': withdrawal, 'profit': norm,
               'tinvest': tinvest, 'tbalance': tbalance, 'pendingDeposit': pendingDeposit, 'plans': plans}
    return render(request, 'plan.html', context)


@login_required(login_url='login')
def invest(request, pk, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
    transaction = Transaction.objects.filter(user=request.user)
    form = InvestmentForm()
    plan = Plan.objects.get(id=pk)
    invests = Investment.objects.filter(user=request.user, is_active=True)
    all_invests = Investment.objects.filter(user=request.user)
    days = timedelta(seconds=120)
    tpercent = 0
    tprofit = 0
    profits = 0

    for trans in transaction:
        if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
            total += trans.amount
        elif trans.status == 'Pending' and trans.transaction_type == 'Deposit':
            pendingDeposit += trans.amount
        else:
            withdrawal += trans.amount

    for value in invests:
        if value.counter >= 7:
            value.profit = ((value.amount) * int(value.plan.percentage) / 100)
            value.is_active = False
            value.save()

        profit += value.profit

        period = (datetime.now(timezone.utc) - value.created)
        period = period.total_seconds()

        ranges = math.floor(period/120)
        # print(ranges, period)

        if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

            tinvest += value.amount

            if ranges > 7:
                value.profit = round(
                    ((value.amount) * int(value.plan.percentage) / 100), 2)
            else:
                if ranges >= 1:
                    value.created = datetime.now(timezone.utc)
                    tpercent += int(value.plan.percentage)

                    profits += round(((value.amount) *
                                     (int(tpercent) / int(value.plan.hours)) / 100), 1)
                value.profit += profits * int(ranges)
            value.counter += ranges

            value.save()

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if int(amount) < plan.minimum_amount:
            mg.error(request, "The Amount is Less than Minimum Amount")

        elif int(amount) > plan.maximum_amount:
            mg.error(request, "The Amount is Greater than Maximum Amount")

        elif int(amount) > total:
            mg.error(request, "Insufficient Fund")

        else:
            Investment.objects.create(
                user=request.user,
                plan=plan,
                amount=amount,
                profit=0,
            )
            return redirect('history')

    for x in all_invests:
        allprofit += round(x.profit, 1)

    print(allprofit)

    profit = profits + profit
    tbalance = round(total + allprofit, 2)
    total = total - tinvest
    norm = round(profit, 2)
    context = {'transaction': transaction, 'total': total, 'withdrawal': withdrawal, 'profit': norm,
               'tinvest': tinvest, 'tbalance': tbalance, 'pendingDeposit': pendingDeposit, 'plan': plan}
    return render(request, 'db-investment.html', context)


@login_required(login_url='login')
def deposit(request, pk):
    form = TransactionForm()
    method = PaymentMethod.objects.get(id=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.payment_method = method
            deposit.transaction_type = 'Deposit'
            deposit.save()

            return redirect('dashboard')
    context = {'method': method, 'form': form}
    return render(request, 'deposit.html', context)


@login_required(login_url='login')
def withdrawal(request, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
    transaction = Transaction.objects.filter(user=request.user)
    invests = Investment.objects.filter(user=request.user, is_active=True)
    all_invests = Investment.objects.filter(user=request.user)
    days = timedelta(seconds=120)
    withdrawal = False
    tpercent = 0
    tprofit = 0
    profits = 0

    for trans in transaction:
        if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
            total += trans.amount
        elif trans.status == 'Pending' and trans.transaction_type == 'Deposit':
            pendingDeposit += trans.amount
        else:
            withdrawal += trans.amount

    for value in invests:
        if value.counter >= 7:
            value.profit = ((value.amount) * int(value.plan.percentage) / 100)
            value.is_active = False
            value.save()

        profit += value.profit

        period = (datetime.now(timezone.utc) - value.created)
        period = period.total_seconds()

        ranges = math.floor(period/120)
        # print(ranges, period)

        if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

            tinvest += value.amount

            if ranges > 7:
                value.profit = round(
                    ((value.amount) * int(value.plan.percentage) / 100), 2)
            else:
                if ranges >= 1:
                    value.created = datetime.now(timezone.utc)
                    tpercent += int(value.plan.percentage)

                    profits += round(((value.amount) *
                                     (int(tpercent) / int(value.plan.hours)) / 100), 1)
                value.profit += profits * int(ranges)
            value.counter += ranges

            value.save()

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if int(amount) > tbalance:
            mg.error(request, 'Insufficient Funds')

        else:
            Transaction.objects.create(
                user=request.user,
                amount=amount,
            )

            return redirect('dashboard')

    for x in all_invests:
        allprofit += round(x.profit, 1)

    print(allprofit)

    totals = total
    profit = profits + profit
    tbalance = round(total + allprofit, 2)
    total = total - tinvest
    norm = round(profit, 2)

    if totals > 1000:
        withdrawal = True

    context = {'transaction': transaction, 'total': total, 'withdrawal': withdrawal, 'profit': norm,
               'tinvest': tinvest, 'withdrawal': withdrawal, 'tbalance': tbalance, 'pendingDeposit': pendingDeposit}
    return render(request, 'db-withdraw.html', context)


@login_required(login_url='login')
def investments(request, total=0, profit=0, tinvest=0, tbalance=0):
    investments = Investment.objects.filter(user=request.user)
    form = InvestmentForm()
    transaction = Transaction.objects.filter(user=request.user)
    invests = Investment.objects.filter(user=request.user)
    # tdelta = datetime.timedelta(minutes=20)

    for trans in transaction:
        if trans.status == 'Confirmed':
            total += trans.amount

    for value in invests:
        tinvest += value.amount
        profit += value.amount * (int(value.plan.percentage) / 100)

    tbalance = total + profit
    total = total - tinvest

    context = {'investments': investments, 'plan': plan, 'form': form,
               'total': total, 'profit': profit, 'tinvest': tinvest, 'tbalance': tbalance}
    return render(request, 'db-history.html', context)


def register(request):
    form = UserForm()
    if request.method == 'POST':
        code = request.POST.get('referer')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            mg.error(request, 'The Passwords are not The same')
        else:
            if code:
                try:
                    recomend = User.objects.get(code=code)

                    form = UserForm(request.POST)
                    if form.is_valid():
                        user = form.save()

                        auth.login(request, user)

                        Recommendation.objects.create(
                            user=request.user,
                            recommended_by=recomend
                        )

                        with get_connection(
                            host=settings.EMAIL_HOST,
                            port=settings.EMAIL_PORT,
                            username=settings.EMAIL_HOST_USER,
                            password=settings.EMAIL_HOST_PASSWORD,
                            use_ssl=settings.EMAIL_USE_SSL
                        ) as connection:

                            subject = "REGISTRATION"
                            message = f"""
                            Welcome to 
                        STEPUP INVESTMENT
                    Email: info@stepedup.com 


                        Delivery Details:


                First Name: {request.user.first_name} 
                Last Name: {request.user.last_name}
                Email: {request.user.email}
                Your Referer Code: {request.user.code}
                

                        Thanks for using our Service


                """
                            email_from = "info@stepedup.com"
                            receiver = [request.user.email]
                            EmailMessage(subject, message, email_from,
                                         receiver, connection=connection).send()

                        return redirect('dashboard')

                    else:
                        mg.error(
                            request, "You need a stronger Password or Email has been used")
                except ObjectDoesNotExist:
                    mg.error(request, "Invalid code")

            else:
                form = UserForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    auth.login(request, user)

                    with get_connection(
                        host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                        use_ssl=settings.EMAIL_USE_SSL
                    ) as connection:

                        subject = "REGISTRATION"
                        message = f"""
                            Welcome to 
                        STEPUP INVESTMENT
                    Email: info@stepedup.com 


                        Delivery Details:


                First Name: {request.user.first_name} 
                Last Name: {request.user.last_name}
                Email: {request.user.email}
                Your Referer Code: {request.user.code}
                

                        Thanks for using our Service


                """
                        email_from = "info@stepedup.com"
                        receiver = [request.user.email]
                        EmailMessage(subject, message, email_from,
                                     receiver, connection=connection).send()

                    return redirect('dashboard')
                else:
                    mg.error(
                        request, "You need a stronger Password or Email has been used")

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
def profile(request, pk, total=0, profit=0, tinvest=0, tbalance=0):
    transaction = Transaction.objects.filter(user=request.user)
    invests = Investment.objects.filter(user=request.user)
    tdelta = datetime.timedelta(minutes=20)

    for trans in transaction:
        if trans.status == 'Confirmed':
            total += trans.amount

    for value in invests:
        tinvest += value.amount
        profit += value.amount * (int(value.plan.percentage) / 100)

    tbalance = total + profit
    total = total - tinvest

    context = {'investments': investments, 'plan': plan, 'total': total,
               'profit': profit, 'tinvest': tinvest, 'tbalance': tbalance}
    return render(request, 'db-settings.html', context)


@login_required(login_url='login')
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    edit = True
    form = UserForm2(instance=user)

    if request.method == 'POST':
        form = UserForm2(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

            return redirect('profile', request.user.id)

    return render(request, 'register.html', {'form': form, 'edit': edit})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('home')


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages as mg
# from django.contrib.auth.models import auth
# from .models import Plan, Transaction, PaymentMethod, Investment, User, Recommendation
# from .forms import TransactionForm, InvestmentForm, UserForm, UserForm2
# from datetime import datetime, timedelta, timezone
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.mail import EmailMessage, get_connection
# from django.conf import settings
# import math


# # Create your views here.
# def home(request):
#     plans = Plan.objects.all()
#     return render(request, 'index.html', {'plans': plans})

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return redirect('dashboard')
#         else:
#             mg.error(request, 'Invalid Username or Password')
#     return render(request, 'login.html')


# @login_required(login_url='login')
# def dashboard(request, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
#     transaction = Transaction.objects.filter(user=request.user)
#     invests = Investment.objects.filter(user=request.user, is_active=True)
#     all_invests = Investment.objects.filter(user=request.user)
#     days = timedelta(seconds=86400)
#     tpercent = 0
#     tprofit = 0
#     profits = 0

#     for trans in transaction:
#         if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
#             total += trans.amount
#         elif trans.status == 'Pending' and trans.transaction_type=='Deposit':
#             pendingDeposit += trans.amount
#         else: withdrawal += trans.amount

#     for value in invests:
#         if value.counter >= 7:
#             value.profit = ((value.amount) * int(value.plan.percentage) / 100)
#             value.is_active = False
#             value.save()

#         profit += value.profit

#         period = (datetime.now(timezone.utc) - value.created)
#         period =  period.total_seconds()

#         ranges = math.floor(period/86400)
#         # print(ranges, period)

#         if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

#             tinvest += value.amount

#             if ranges > 7:
#                 value.profit = round(((value.amount) * int(value.plan.percentage) / 100), 2)
#             else:
#                 if ranges >=1:
#                     value.created = datetime.now(timezone.utc)
#                     tpercent += int(value.plan.percentage)

#                     profits += round(((value.amount) * (int(tpercent) / int(value.plan.hours)) / 100), 1)
#                 value.profit += profits * int(ranges)
#             value.counter += ranges

#             value.save()


#     for x in all_invests:
#         allprofit += round(x.profit, 1)

#     print(allprofit)


#     profit = profits + profit
#     tbalance = round(total + allprofit, 2)
#     total = total - tinvest
#     norm = round(profit, 2)
#     context = {'transaction': transaction, 'total': total, 'withdrawal':withdrawal, 'profit': norm,
#     'tinvest':tinvest, 'tbalance': tbalance, 'pendingDeposit':pendingDeposit}
#     return render(request, 'dashboard.html', context)


# @login_required(login_url='login')
# def payment(request):
#     methods = PaymentMethod.objects.all()
#     context = {'methods': methods}
#     return render(request, 'payment.html', context)


# @login_required(login_url='login')
# def plan(request, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
#     transaction = Transaction.objects.filter(user=request.user)
#     invests = Investment.objects.filter(user=request.user, is_active=True)
#     all_invests = Investment.objects.filter(user=request.user)
#     plans = Plan.objects.all()
#     days = timedelta(seconds=86400)
#     tpercent = 0
#     tprofit = 0
#     profits = 0

#     for trans in transaction:
#         if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
#             total += trans.amount
#         elif trans.status == 'Pending' and trans.transaction_type=='Deposit':
#             pendingDeposit += trans.amount
#         else: withdrawal += trans.amount

#     for value in invests:
#         if value.counter >= 7:
#             value.profit = ((value.amount) * int(value.plan.percentage) / 100)
#             value.is_active = False
#             value.save()

#         profit += value.profit

#         period = (datetime.now(timezone.utc) - value.created)
#         period =  period.total_seconds()

#         ranges = math.floor(period/86400)
#         # print(ranges, period)

#         if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

#             tinvest += value.amount

#             if ranges > 7:
#                 value.profit = round(((value.amount) * int(value.plan.percentage) / 100), 2)
#             else:
#                 if ranges >=1:
#                     value.created = datetime.now(timezone.utc)
#                     tpercent += int(value.plan.percentage)

#                     profits += round(((value.amount) * (int(tpercent) / int(value.plan.hours)) / 100), 1)
#                 value.profit += profits * int(ranges)
#             value.counter += ranges

#             value.save()


#     for x in all_invests:
#         allprofit += round(x.profit, 1)

#     print(allprofit)


#     profit = profits + profit
#     tbalance = round(total + allprofit, 2)
#     total = total - tinvest
#     norm = round(profit, 2)
#     context = {'transaction': transaction, 'total': total, 'withdrawal':withdrawal, 'profit': norm,
#     'tinvest':tinvest, 'tbalance': tbalance, 'pendingDeposit':pendingDeposit, 'plans':plans}
#     return render(request, 'plan.html', context)


# @login_required(login_url='login')
# def invest(request, pk, pendingDeposit=0, withdrawal=0, allprofit=0, total=0, profit=0, tinvest=0, tbalance=0):
#     transaction = Transaction.objects.filter(user=request.user)
#     form = InvestmentForm()
#     plan = Plan.objects.get(id=pk)
#     invests = Investment.objects.filter(user=request.user, is_active=True)
#     all_invests = Investment.objects.filter(user=request.user)
#     days = timedelta(seconds=86400)
#     tpercent = 0
#     tprofit = 0
#     profits = 0

#     for trans in transaction:
#         if trans.status == 'Confirmed' and trans.transaction_type == 'Deposit':
#             total += trans.amount
#         elif trans.status == 'Pending' and trans.transaction_type=='Deposit':
#             pendingDeposit += trans.amount
#         else: withdrawal += trans.amount

#     for value in invests:
#         if value.counter >= 7:
#             value.profit = ((value.amount) * int(value.plan.percentage) / 100)
#             value.is_active = False
#             value.save()

#         profit += value.profit

#         period = (datetime.now(timezone.utc) - value.created)
#         period =  period.total_seconds()

#         ranges = math.floor(period/86400)
#         # print(ranges, period)

#         if int(value.counter) <= int(value.plan.hours) and value.is_active == True:

#             tinvest += value.amount

#             if ranges > 7:
#                 value.profit = round(((value.amount) * int(value.plan.percentage) / 100), 2)
#             else:
#                 if ranges >=1:
#                     value.created = datetime.now(timezone.utc)
#                     tpercent += int(value.plan.percentage)

#                     profits += round(((value.amount) * (int(tpercent) / int(value.plan.hours)) / 100), 1)
#                 value.profit += profits * int(ranges)
#             value.counter += ranges

#             value.save()


#     if request.method == 'POST':
#         amount = request.POST.get('amount')

#         if int(amount) < plan.minimum_amount:
#             mg.error(request, "The Amount is Less than Minimum Amount")

#         elif int(amount) > plan.maximum_amount:
#             mg.error(request, "The Amount is Greater than Maximum Amount")

#         elif int(amount) > total:
#             mg.error(request, "Insufficient Fund")

#         else:
#             Investment.objects.create(
#                 user=request.user,
#                 plan=plan,
#                 amount=amount,
#                 profit=0,
#             )

#             # Email Setup
#             with get_connection(
#             host=settings.EMAIL_HOST,
#             port=settings.EMAIL_PORT,
#             username=settings.EMAIL_HOST_USER,
#             password=settings.EMAIL_HOST_PASSWORD,
#             use_ssl=settings.EMAIL_USE_SSL
#             ) as connection:

#                 subject = "STEPEDUP PLAN SUCCESSFUL"
#                 message = f"""
# YOUR STEPEDUP PLAN DETAILS:

# Amount: {amount}
# Plan: {plan}

# Thanks for using our Service


#     """
#                 email_from = "info@stepedup.com"
#                 receiver = [request.user.email]
#                 EmailMessage(subject, message, email_from, receiver, connection=connection).send()
#                 return redirect('history')


#     for x in all_invests:
#         allprofit += round(x.profit, 1)

#     print(allprofit)


#     profit = profits + profit
#     tbalance = round(total + allprofit, 2)
#     total = total - tinvest
#     norm = round(profit, 2)
#     context = {'transaction': transaction, 'total': total, 'withdrawal':withdrawal, 'profit': norm,
#     'tinvest':tinvest, 'tbalance': tbalance, 'pendingDeposit':pendingDeposit, 'plan':plan}
#     return render(request, 'db-investment.html', context)


# @login_required(login_url='login')
# def deposit(request, pk):
#     form = TransactionForm()
#     method = PaymentMethod.objects.get(id=pk)

#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         form = TransactionForm(request.POST, request.FILES)

#         if form.is_valid():
#             deposit = form.save(commit=False)
#             deposit.user = request.user
#             deposit.payment_method = method
#             deposit.transaction_type = 'Deposit'
#             deposit.save()


#             #Email Setup

#             with get_connection(
#             host=settings.EMAIL_HOST,
#             port=settings.EMAIL_PORT,
#             username=settings.EMAIL_HOST_USER,
#             password=settings.EMAIL_HOST_PASSWORD,
#             use_ssl=settings.EMAIL_USE_SSL
#             ) as connection:

#                 subject = "DEPOSIT SUCCESSFUL"
#                 message = f"""

#             Your Deposit Details:


#     Deposited Amount: {amount}
#     Deposit Method: {method}


#             Thanks for using our Service


#     """
#                 email_from = "info@stepedup.com"
#                 receiver = [request.user.email]
#                 EmailMessage(subject, message, email_from, receiver, connection=connection).send()


#             return redirect('dashboard')
#     context = {'method': method, 'form': form}
#     return render(request, 'deposit.html', context)


# @login_required(login_url='login')
# def withdrawal(request, total=0, profit=0, tinvest=0, tbalance=0, withdrwable=0):
#     transaction = Transaction.objects.filter(user=request.user)
#     invests = Investment.objects.filter(user=request.user)
#     # tdelta = datetime.timedelta(minutes=20)

#     for trans in transaction:
#         if trans.status == 'Confirmed':
#             total += trans.amount

#     for value in invests:
#         tinvest += value.amount
#         profit += value.amount * (int(value.plan.percentage) / 100)

#     tbalance = total + profit
#     total = total - tinvest
#     withdrwable = tbalance - tinvest

#     if request.method == 'POST':
#         amount = request.POST.get('amount')

#         if int(amount) > tbalance:
#             mg.error(request, 'Insufficient Funds')

#         else:
#             Transaction.objects.create(
#             user=request.user,
#             amount=amount,
#             )

#             return redirect('dashboard')

#     context = {'transaction': transaction, 'total': total, 'profit': profit, 'tinvest':tinvest, 'tbalance': tbalance}

#     return render(request, 'db-withdraw.html', context)


# @login_required(login_url='login')
# def investments(request, total=0, profit=0, tinvest=0, tbalance=0):
#     investments = Investment.objects.filter(user=request.user)
#     form = InvestmentForm()
#     transaction = Transaction.objects.filter(user=request.user)
#     invests = Investment.objects.filter(user=request.user)
#     # tdelta = datetime.timedelta(minutes=20)


#     for trans in transaction:
#         if trans.status == 'Confirmed':
#             total += trans.amount

#     for value in invests:
#         tinvest += value.amount
#         profit += value.amount * (int(value.plan.percentage) / 100)

#     tbalance = total + profit
#     total = total - tinvest


#     context = {'investments': investments, 'plan': plan, 'form': form, 'total': total, 'profit': profit, 'tinvest':tinvest, 'tbalance': tbalance}
#     return render(request, 'db-history.html', context)


# def register(request):
#     form = UserForm()
#     if request.method == 'POST':
#         code = request.POST.get('referer')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 != password2:
#             mg.error(request, 'The Passwords are not The same')
#         else:
#             if code:
#                 try:
#                     recomend = User.objects.get(code=code)


#                     form = UserForm(request.POST)
#                     if form.is_valid():
#                         user = form.save()

#                         auth.login(request, user)

#                         Recommendation.objects.create(
#                             user=request.user,
#                             recommended_by=recomend
#                         )

#                     #Email Setup

#                         with get_connection(
#                         host=settings.EMAIL_HOST,
#                         port=settings.EMAIL_PORT,
#                         username=settings.EMAIL_HOST_USER,
#                         password=settings.EMAIL_HOST_PASSWORD,
#                         use_ssl=settings.EMAIL_USE_SSL
#                         ) as connection:

#                             subject = "REGISTRATION SUCCESSFUL"
#                             message = f"""
#                             Welcome to STEPUP
#                     Email: info@stepedup.com


#                         Your Registration Details:


#                 First Name: {request.user.first_name}
#                 Last Name: {request.user.last_name}
#                 Email: {request.user.email}
#                 Your Referer Code: {request.user.code}


#                         Thanks for using our Service


#                 """
#                             email_from = "info@stepedup.com"
#                             receiver = [request.user.email]
#                             EmailMessage(subject, message, email_from, receiver, connection=connection).send()


#                         return redirect('dashboard')

#                     else:
#                         mg.error(request, "You need a stronger Password")
#                 except ObjectDoesNotExist:
#                     mg.error(request, "Invalid code")

#             else:
#                 form = UserForm(request.POST)
#                 if form.is_valid():
#                     user = form.save()
#                     auth.login(request, user)

#                     #Email Setup
#                     with get_connection(
#                         host=settings.EMAIL_HOST,
#                         port=settings.EMAIL_PORT,
#                         username=settings.EMAIL_HOST_USER,
#                         password=settings.EMAIL_HOST_PASSWORD,
#                         use_ssl=settings.EMAIL_USE_SSL
#                         ) as connection:

#                             subject = "REGISTRATION SUCCESSFUL"
#                             message = f"""
#                             Welcome to STEPUP
#                     Email: info@stepedup.com


#                         Your Registration Details:


#                 First Name: {request.user.first_name}
#                 Last Name: {request.user.last_name}
#                 Email: {request.user.email}
#                 Your Referer Code: {request.user.code}


#                         Thanks for using our Service


#                 """
#                             email_from = "info@stepedup.com"
#                             receiver = [request.user.email]
#                             EmailMessage(subject, message, email_from, receiver, connection=connection).send()

#                     return redirect('dashboard')
#                 else:
#                     mg.error(request, "You need a stronger Password")


#     context = {'form': form}
#     return render(request, 'register.html', context)


# @login_required(login_url='login')
# def profile(request, pk, total=0, profit=0, tinvest=0, tbalance=0):
#     transaction = Transaction.objects.filter(user=request.user)
#     invests = Investment.objects.filter(user=request.user)
#     # tdelta = datetime.timedelta(minutes=20)

#     for trans in transaction:
#         if trans.status == 'Confirmed':
#             total += trans.amount

#     for value in invests:
#         tinvest += value.amount
#         profit += value.amount * (int(value.plan.percentage) / 100)


#     tbalance = total + profit
#     total = total - tinvest


#     context = {'investments': investments, 'plan': plan, 'total': total, 'profit': profit, 'tinvest':tinvest, 'tbalance': tbalance}
#     return render(request, 'db-settings.html', context)


# @login_required(login_url='login')
# def editProfile(request, pk):
#     user = User.objects.get(id=pk)
#     edit = True
#     form = UserForm2(instance=user)

#     if request.method == 'POST':
#         form = UserForm2(request.POST, request.FILES, instance=user)

#         if form.is_valid():
#             form.save()

#             return redirect('profile', request.user.id )

#     return render(request, 'register.html', {'form': form, 'edit': edit})


# def about(request):
#     return render(request, 'about.html')


# def contact(request):
#     return render(request, 'contact.html')


# def logout(request):
#     if request.user.is_authenticated:
#         auth.logout(request)
#         return redirect('home')
