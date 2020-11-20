from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/index.html')

# for showing signup/login button for student


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/studentclick.html')

# for showing signup/login button for teacher


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/adminclick.html')


def adminsignup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request, 'library/adminsignup.html', {'form': form})


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'library/studentsignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    else:
        return render(request, 'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    # now it is empty book form for sending to html
    form = forms.BookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.BookForm(request.POST)
        if form.is_valid():
            present = models.Book.objects.filter(name=form.cleaned_data.get(
                "name"), author=form.cleaned_data.get("author"), isbn=form.cleaned_data.get("isbn"))
            print(present)
            if present:
                present[0].quantity += 1
                present[0].save()
            else:
                user = form.save()
            return render(request, 'library/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.filter()
    return render(request, 'library/viewbook.html', {'books': books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.isbn = request.POST.get('isbn2')

            present = models.Book.objects.filter(
                isbn=request.POST.get('isbn2'))

            print(present)
            present[0].quantity -= 1
            present[0].save()
            obj.save()

            return render(request, 'library/bookissued.html')

    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    for ib in issuedbooks:
        issdate = str(ib.issuedate.day)+'-' + \
            str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate = str(ib.expirydate.day)+'-' + \
            str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        # fine calculation
        days = (date.today()-ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10

        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(
            enrollment=ib.enrollment))
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].enrollment,
                 books[i].name, books[i].author, issdate, expdate, fine)
            i = i+1
            li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user=request.user.id)
    if len(student):
        issuedbook = models.IssuedBook.objects.filter(
            enrollment=student[0].enrollment)
    else:
        issuedbook = []
    li1 = []

    li2 = []
    for ib in issuedbook:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t = (request.user, student[0].enrollment,
                 student[0].branch, book.name, book.author)
            li1.append(t)
        issdate = str(ib.issuedate.day)+'-' + \
            str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate = str(ib.expirydate.day)+'-' + \
            str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        # fine calculation
        days = (date.today()-ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10
        t = (issdate, expdate, fine)
        li2.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})


@login_required(login_url='studentlogin')
def returnbook_view(request):
    if request.method == 'POST':
        isbn = request.POST["book"]
        present = models.Book.objects.filter(isbn=isbn)
        print(present)
        present[0].quantity += 1
        present[0].save()
        student = models.StudentExtra.objects.filter(user=request.user.id)
        issuedbook = models.IssuedBook.objects.filter(
            enrollment=student[0].enrollment, isbn=isbn)
        issuedbook[0].delete()
        return render(request, "library/bookreturned.html")

    else:
        student = models.StudentExtra.objects.filter(user=request.user.id)
        if len(student):
            issuedbook = models.IssuedBook.objects.filter(
                enrollment=student[0].enrollment)
        else:
            issuedbook = []
        allissued = []
        for ib in issuedbook:
            books = models.Book.objects.filter(isbn=ib.isbn)
            for book in books:
                t = (book.name, ib.isbn)
                allissued.append(t)
        return render(request, 'library/returnbook.html', {'issuedbook': allissued})

    # form = forms.IssuedBookForm()
    # if request.method == 'POST':
    #     # now this form have data from html
    #     form = forms.IssuedBookForm(request.POST)
    #     if form.is_valid():
    #         obj = models.IssuedBook()
    #         obj.enrollment = request.POST.get('enrollment2')
    #         obj.isbn = request.POST.get('isbn2')

    #         present = models.Book.objects.filter(
    #             isbn=request.POST.get('isbn2'))
    #         print(present)
    #         if present:
    #             print(present)
    #             present[0].quantity -= 1
    #             present[0].save()
    #         else:
    #             obj.save()
    #         return render(request, 'library/bookissued.html')

    # return render(request, 'library/issuebook.html', {'form': form})
