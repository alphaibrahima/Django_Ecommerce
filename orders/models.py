from django.db import models
from accounts.models import Account
from django.utils import timezone

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=150)
    payment_method = models.CharField(max_length=150)
    amount_paid = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.payment_id}'



class Order(models.Model):
    STATUS ={
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    }        

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True ,null=True)
    order_number = models.CharField(max_length=100, default="", null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100,blank=True)
    order_total = models.CharField(max_length=30, default="", null=True)
    ip_address = models.CharField(blank=True ,max_length=10,  default="", null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    tax = models.CharField(max_length=49,default="", null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=timezone.now)
    


    def __str__(self) -> str:
        return self.first_name