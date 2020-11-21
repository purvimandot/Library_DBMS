from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=10, primary_key=True)
    branch = models.CharField(max_length=20)
    # used in issue book

    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
    ]
    name = models.CharField(max_length=20)
    isbn = models.PositiveIntegerField(primary_key=True)
    author = models.CharField(max_length=20)
    category = models.CharField(
        max_length=20, choices=catchoice, default='education')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):

    enrollment = models.CharField(max_length=10)
    isbn = models.PositiveIntegerField(primary_key=True)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return self.enrollment
