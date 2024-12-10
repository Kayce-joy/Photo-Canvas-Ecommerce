#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



#class Photo(models.Model):
    #title = models.CharField(max_length=255)
    #description = models.TextField()
    #image = models.ImageField(upload_to='photos/')
    #price = models.DecimalField(max_digits=10, decimal_places=2)

    #def __str__(self):
        #return self.title

class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Make it nullable

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.photo.price

    #class Transaction(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    #timestamp = models.DateTimeField(auto_now_add=True)
    #status = models.CharField(max_length=50, default='Pending')
    #transaction_id = models.CharField(max_length=255, blank=True, null=True)

    #def __str__(self):
        #return f"Transaction {self.transaction_id or 'N/A'} - {self.status}"

class Photoshoot(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title