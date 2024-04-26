from django.db import models
from django.utils import timezone
from datetime import timedelta


class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_choices = [
        ('fashion', 'Fashion'),
        ('electronics', 'Electronics'),
        ('accessories', 'Accessories'),
        ('toy', 'Toy'),
        ('furniture', 'Furniture'),
        ('others', 'Others')]
    
    category = models.CharField(max_length=20, choices=category_choices)
    end_time = models.DateTimeField()
    item_number = models.CharField(max_length=64, primary_key=True)
    

class Bidding(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='biddings')
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



      



