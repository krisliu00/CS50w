from django.db import models


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
      
    
class ItemPictures(models.Model):
    auction_list = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='item_pictures')
    item_picture = models.ImageField(upload_to='static/auctions/item_pictures')



