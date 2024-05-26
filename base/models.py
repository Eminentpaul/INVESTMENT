from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.urls import reverse
from .utility import generate_ref_code
from django.contrib.auth.models import User


STATUS = (
    ("Pending", "Pending"),
    ("Cancelled", 'Cancelled'),
    ('Successful', 'Successful'),
    ('Approved', 'Approved'), 
    ('Confirmed', 'Comfirmed')
)



# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=12, blank=True)
    image = models.ImageField(blank=True, default="static/profile.jpg", null=True, upload_to='user/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_recommendation(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


class Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='refer_by')
    created = models.DateTimeField(auto_now_add=True, null=True)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to='payment method/')
    address_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=100)
    minimum_amount = models.IntegerField()
    maximum_amount = models.IntegerField()
    percentage = models.CharField(max_length=5)
    hours = models.CharField(max_length=100)
    

    def __str__(self):
        return f'{self.name} - {self.percentage}% Return after {self.hours} Days'


    def get_url(self):
        return reverse('invest', args=[self.id])


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='Transactions', null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    transaction_type = models.CharField(max_length=50, default='Withdrawal')
    created = models.DateTimeField(auto_now_add=True)

    
class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    amount = models.IntegerField()
    profit = models.FloatField()
    counter = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']

        
        