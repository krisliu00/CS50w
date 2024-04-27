from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bidding, AuctionList

def save_images(images, item_number):
    saved_image_paths = []
    for image in images:
        upload_path = f'items/{item_number}/{image.name}'
        saved_path = default_storage.save(upload_path, image)
        saved_image_paths.append(saved_path)
    return saved_image_paths


@receiver(post_save, sender=Bidding)
def current_price(sender, instance, **kwargs):
    try:
        auction_item = AuctionList.objects.get(item_number=instance.auction.item_number)
        if instance.bid is not None:
            current_price = instance.bid + auction_item.price
            auction_item.price = current_price
            auction_item.save()

    except AuctionList.DoesNotExist:
        pass
