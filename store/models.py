from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    email = models.CharField(max_length = 200, null = True)
    name = models.CharField(max_length = 200, )
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200,  null = True, blank = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    digital = models.BooleanField(default = False, null = True, blank = True)
    description = models.CharField(max_length = 500, null = True , blank= True)
    image = models.ImageField( null = True, blank = True)
    category = models.ForeignKey(Category , null = True, blank = True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            url = ''
            return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length= 100, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        Total = sum ([item.get_total for item in orderitems])
        return Total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum ([item.quantity for item in orderitems])
        return  total_items

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class shippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length= 200, null = True)
    city = models.CharField(max_length= 200, null = True)
    state = models.CharField(max_length= 200, null = True)
    zipcode = models.CharField(max_length= 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return str(self.address)