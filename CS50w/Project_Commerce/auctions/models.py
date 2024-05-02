from django.db import models
from core.models import CustomUser



class AuctionList(models.Model):
    class Meta:
        managed = True
        
    title = models.CharField(max_length=64)
    short_description = models.CharField(max_length=64)
    details = models.TextField()
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
    image_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='auction_user')



class Bidding(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='biddings')
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='bidding_user')



class Comments(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='comment_user')



