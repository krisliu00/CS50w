from django.db import models
from django.utils import timezone
from datetime import timedelta


class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    category_choices = [
        ('fashion', 'Fashion'),
        ('electronics', 'Electronics'),
        ('accessories', 'Accessories'),
        ('toy', 'Toy'),
        ('furniture', 'Furniture'),
        ('others', 'Others')]
    
    category = models.CharField(max_length=20, choices=category_choices)
    end_time = models.DateTimeField()
    item_number = models.CharField(max_length=64)
      



