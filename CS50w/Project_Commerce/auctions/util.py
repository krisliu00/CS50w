import glob
import textwrap
from django.core.files.storage import default_storage
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Bidding, AuctionList
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
from datetime import datetime
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models import Max

def save_images(images, item_number):
    saved_image_paths = []
    for image in images:

        img = Image.open(image)
        width, height = img.size
        target_size = (300, 350)
        width_ratio = target_size[0] / width
        height_ratio = target_size[1] / height
        scale = min(width_ratio, height_ratio)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_img = img.resize((new_width, new_height))
        adjusted_img = Image.new("RGB", target_size, color=(255, 255, 255))
        offset = ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2)
        adjusted_img.paste(resized_img, offset)
        img_bytes = BytesIO()
        adjusted_img.save(img_bytes, format='PNG') 
        img_file = ContentFile(img_bytes.getvalue())
        upload_path = f'items/{item_number}/{image.name}'
        saved_path = default_storage.save(upload_path, img_file)
        saved_image_paths.append(saved_path)
    return saved_image_paths


def delete_instance(item_number):
    try:
        instance = AuctionList.objects.get(item_number=item_number)
        instance.delete()
        return True
    except AuctionList.DoesNotExist:
        return False 
    
@receiver(post_delete, sender=AuctionList)
def delete_auction_images(sender, instance, **kwargs):
    item_number = instance.item_number
    media_items_folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    if os.path.exists(media_items_folder_path):
        for filename in os.listdir(media_items_folder_path):
            file_path = os.path.join(media_items_folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(media_items_folder_path)
    media_index_image_path = os.path.join(settings.MEDIA_ROOT, 'index_images', f"{item_number}.png")
    if os.path.exists(media_index_image_path):
        os.remove(media_index_image_path)

# @receiver(post_save, sender=Bidding)
# def current_price(sender, instance, **kwargs):
#     try:
#         auction_item = AuctionList.objects.get(item_number=instance.auction.item_number)
#         if instance.bid is not None:
#             current_price = instance.bid + auction_item.price
#             auction_item.price = current_price
#             auction_item.save()

#     except AuctionList.DoesNotExist:
#         pass

def format_timedelta(remaining_time):
    total_seconds = remaining_time.total_seconds()
    days_as_hours, remainder = divmod(total_seconds, 3600 * 24)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours += days_as_hours * 24
    if seconds >= 60:
        minutes += seconds // 60
        seconds %= 60
    
    return f"{int(hours):02d}h:{int(minutes):02d}m:{int(seconds):02d}s"


def index_image(item_number):
    try:
        auction_data = AuctionList.objects.get(item_number=item_number)
    except AuctionList.DoesNotExist:
        return None
    
    max_width = 280
    wrapped_short_description = textwrap.fill(auction_data.short_description, width=max_width).replace('\n', ' ')

    media_folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    image_files = glob.glob(os.path.join(media_folder_path, '*.*'))
    
    item_image = Image.open(image_files[0])
    
    item_width, item_height = item_image.size
    
    white_image = Image.new('RGBA', (item_width, item_height), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(white_image)
    font = ImageFont.truetype("arial.ttf", 15)

    end_time = auction_data.end_time.replace(tzinfo=None)
    current_time = datetime.now()
    remaining_time = end_time - current_time
    formattd_remaining_time = format_timedelta(remaining_time)
    texts = [f"{auction_data.title}", wrapped_short_description, f"Price: {auction_data.price}", f"Time Remaining: {formattd_remaining_time}"]

    y_position = 10
    x_position = 10  

    for text in texts:
        for c in text:
            # Get the bounding box for the current character
            draw.text((x_position, y_position), c, fill="black", font=font)
            x_position += draw.textlength(c, font=font)  
        
        
        y_position += draw.textbbox((x_position, y_position), text, font=font)[3] - draw.textbbox((x_position, y_position), text, font=font)[1] + 10
        x_position = 10

    background_image = Image.new('RGBA', (item_width, item_height + y_position), color=(255, 255, 255, 255))
    background_image.paste(item_image, (0, 0))
    background_image.paste(white_image, (0, item_height))
    

    upload_path = f'index_images/{item_number}.png'
    file_path = os.path.join(settings.MEDIA_ROOT, upload_path)
    with default_storage.open(file_path, 'wb') as image_file:
        background_image.save(image_file, format='PNG')

    return upload_path

def highest_bidding(item_number):
    user_ids = AuctionList.objects.filter(item_number=item_number).values_list('user_id', flat=True)
    highest_bid = None
    print(item_number)

    for user_id in user_ids:
        aggregation_result = Bidding.objects.filter(user_id=user_id).aggregate(max_bid=Max('bid'))
        max_bid = aggregation_result.get('max_bid')  # Access max_bid from aggregation_result

        if max_bid is not None:
            if highest_bid is None or max_bid > highest_bid:
                highest_bid = max_bid

    return highest_bid



def watchlist_image(item_number):
    file_name = None
    
    if item_number:
        file_name = f"{settings.MEDIA_URL}index_images/{item_number}.png"

    return file_name