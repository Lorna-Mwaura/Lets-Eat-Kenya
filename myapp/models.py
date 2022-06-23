from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField( blank=False, null=False, max_length=50)
    description = models.CharField( blank=False, null=False, max_length=250)
    quantity = models.IntegerField( blank=False, null=False,)
    price = models.IntegerField(blank=False, null=False,)
    info = models.CharField(blank=True, null=True, max_length=500)
    image =CloudinaryField('image', null=True)

    def create_product(self):
        self.save()
    
    def delete_product(self):
        self.delete()

    def __str__(self) -> str:
        return self.product_name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    )
    order_amount = models.IntegerField(null=True, blank=True, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    time_ordered = models.TimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=200, null=True, default='Pending')

    def __str__(self) -> str:
        return self.product.product_name

    @property
    def total(self):
        return self.order_amount * self.product.price

