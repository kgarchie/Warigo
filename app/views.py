import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import User, FundApplication, Department


# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required(login_url='app:login')
def apply(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    if request.method == 'POST':
        department = request.POST['department']
        applicant = request.user
        project_name = request.POST['project_name']
        project_description = request.POST['project_description']
        try:
            amount = int(request.POST['amount'])
        except ValueError:
            messages.error(request, 'Amount must be a number; Please input amount')
            return redirect('app:apply')
        campus = request.POST['campus']
        ps = request.POST['ps']
        pe = request.POST['pe']

        if ps != "":
            # convert ps iso date to datetime
            ps = datetime.datetime.strptime(ps, '%Y-%m-%d')
        else:
            ps = None

        if pe != "":
            # convert pe iso date to datetime
            pe = datetime.datetime.strptime(pe, '%Y-%m-%d')
        else:
            pe = None

        department = Department.objects.get(id=department)

        fund_application = FundApplication.objects.create(department=department, applicant=applicant,
                                                          project_name=project_name,
                                                          project_description=project_description,
                                                          amount_applied_for=amount,
                                                          campus=campus, ps=ps, pe=pe)
        try:
            fund_application.save()
            messages.success(request, 'Application submitted successfully')
            return redirect('app:index')
        except IntegrityError:
            messages.error(request, 'Application already exists')
            return redirect('app:apply')
    return render(request, 'application.html', context)


@login_required(login_url='app:login')
def history(request):
    user_applications = FundApplication.objects.filter(applicant=request.user)
    context = {
        'user_applications': user_applications
    }
    return render(request, 'history.html', context)


def search_history(request):
    if request.method == 'POST':
        search = request.POST['search']
        # search both project name and project description
        user_applications = FundApplication.objects.filter(applicant=request.user,
                                                           project_name__icontains=search) | FundApplication.objects.filter(
            applicant=request.user, project_description__icontains=search)
        # user_applications = FundApplication.objects.filter(applicant=request.user, project_name__icontains=search)
        # in case the above fails
        context = {
            'user_applications': user_applications
        }
        return render(request, 'history.html', context)
    return redirect('app:history')


def about(request):
    return render(request, 'about.html')


def login_function(request):
    if request.method == 'POST':
        reg_no = request.POST['reg_no']
        password = request.POST['password']
        user = authenticate(request, staff_id_or_reg_no=reg_no, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('app:login')
    return render(request, 'login.html')


def logout_function(request):
    logout(request)
    return render(request, 'index.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        reg_no = request.POST['reg_no']
        student_name = request.POST['student_name']
        student_email = request.POST['student_email']
        password = request.POST['password2']

        if User.objects.filter(staff_id_or_reg_no=reg_no).exists():
            messages.error(request, 'Student Already Exists')
            return redirect('app:register')
        else:
            user = User.objects.create_user(staff_id_or_reg_no=reg_no, name=student_name, email=student_email,
                                            password=password)
            user.save()
            messages.success(request, 'Student Registered Successfully')
            login(request, user)
            return redirect('app:index')
    return render(request, 'register.html')


def view_pending(request):
    if request.user.is_staff:
        pending_applications = FundApplication.objects.filter(approved=False, rejected=False)
        context = {
            'user_applications': pending_applications
        }
        return render(request, 'history.html', context)
    else:
        pending_applications = FundApplication.objects.filter(approved=False, rejected=False)
        context = {
            'user_applications': pending_applications
        }
        return render(request, 'history.html', context)


def view_approved(request):
    if request.user.is_staff:
        approved_applications = FundApplication.objects.filter(approved=True)
        context = {
            'user_applications': approved_applications
        }
        return render(request, 'history.html', context)
    else:
        approved_applications = FundApplication.objects.filter(applicant=request.user)
        context = {
            'user_applications': approved_applications
        }
        return render(request, 'history.html', context)


def application_detail(request, pk):
    department = Department.objects.all()
    application = FundApplication.objects.get(pk=pk)
    context = {
        'application': application,
        'departments': department
    }
    return render(request, 'application_details.html', context)


def application_update(request, pk):
    departments = Department.objects.all()
    fund_application = FundApplication.objects.get(pk=pk)
    context = {
        'departments': departments,
        'fund_application': fund_application
    }
    if request.method == 'POST':
        department = request.POST['department']
        applicant = request.user
        project_name = request.POST['project_name']
        project_description = request.POST['project_description']
        amount = request.POST['amount']
        campus = request.POST['campus']
        ps = request.POST['ps']
        pe = request.POST['pe']

        department = Department.objects.get(id=department)

        fund_application.applicant = applicant
        fund_application.department = department
        fund_application.project_name = project_name
        fund_application.project_description = project_description
        fund_application.amount_applied_for = amount
        fund_application.campus = campus
        fund_application.ps = ps
        fund_application.pe = pe
        fund_application.rejected = False
        fund_application.approved = False
        fund_application.status = 'Edited | Pending'

        fund_application.save()
        messages.success(request, 'Your application has been submitted successfully')
        return redirect('app:history')
    return render(request, 'application_update.html', context)


def application_delete(request, pk):
    application = FundApplication.objects.get(pk=pk)
    if application.approved == True or application.rejected == True:
        messages.error(request, 'You cannot delete an approved or rejected application')
        return redirect('app:history')
    messages.success(request, 'Application deleted successfully')
    return redirect('app:history')


def application_approve(request, id):
    application = FundApplication.objects.get(id=id)
    if request.method == 'POST':
        application.approved = True
        application.status = 'Approved'
        application.save()
        messages.success(request, 'Application approved successfully')
        return redirect('app:dashboard')
    return render(request, 'application_details.html', context={'application': application})


def application_reject(request, id):
    application = FundApplication.objects.get(id=id)
    if request.method == 'POST':
        application.rejected = True
        application.status = 'Rejected'
        application.save()
        messages.success(request, 'Application rejected successfully')
        return redirect('app:dashboard')
    return render(request, 'application_details.html', context={'application': application})


def application_appeal(request, id):
    application = FundApplication.objects.get(id=id)
    if request.method == 'POST':
        application.status = 'Rejected | Appealed'
        application.save()
        messages.success(request, 'Application appealed successfully')
        return redirect('app:dashboard')
    return render(request, 'application_details.html', context={'application': application})


def view_rejected(request):
    if request.user.is_staff:
        rejected_applications = FundApplication.objects.filter(status__icontains='Rejected', rejected=True)
        context = {
            'user_applications': rejected_applications
        }
        return render(request, 'history.html', context)
    else:
        rejected_applications = FundApplication.objects.filter(status='Rejected', applicant=request.user)
        context = {
            'user_applications': rejected_applications
        }
        return render(request, 'history.html', context)


def view_appealed(request):
    if request.user.is_staff:
        appealed_applications = FundApplication.objects.filter(status__icontains='Appealed', rejected=True)
        context = {
            'user_applications': appealed_applications
        }
        return render(request, 'history.html', context)
    else:
        appealed_applications = FundApplication.objects.filter(status='Appealed', applicant=request.user)
        context = {
            'user_applications': appealed_applications
        }
        return render(request, 'history.html', context)


def search(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        search_results = FundApplication.objects.filter(project_name__icontains=search_term)
        context = {
            'user_applications': search_results
        }
        return render(request, 'history.html', context)
    return render(request, 'history.html')


def search_pending(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        search_results = FundApplication.objects.filter(project_name__icontains=search_term,
                                                        status__icontains='Pending')
        context = {
            'user_applications': search_results
        }
        return render(request, 'history.html', context)
    return render(request, 'history.html')


def search_approved(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        search_results = FundApplication.objects.filter(project_name__icontains=search_term,
                                                        status__icontains='Approved')
        context = {
            'user_applications': search_results
        }
        return render(request, 'history.html', context)
    return render(request, 'history.html')


def search_rejected(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        search_results = FundApplication.objects.filter(project_name__icontains=search_term,
                                                        status__icontains='Rejected')
        context = {
            'user_applications': search_results
        }
        return render(request, 'history.html', context)
    return render(request, 'history.html')


def search_appealed(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        search_results = FundApplication.objects.filter(project_name__icontains=search_term,
                                                        status__icontains='Appealed')
        context = {
            'user_applications': search_results
        }
        return render(request, 'history.html', context)
    return render(request, 'history.html')
