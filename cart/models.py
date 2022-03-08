from pyexpat import model
from django.db import models
from store.models import Product
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantite = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def sub_total(self):
        return self.product.price * self.quantite


    def __str__(self):
        return self.product

