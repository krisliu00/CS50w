from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


def save_images(images, user, post):
    saved_image_paths = []

    if not images:
        return None

    for image in images:
        img = Image.open(image)
        target_width = 300
        aspect_ratio = img.height / img.width
        target_height = int(target_width * aspect_ratio)
        img.thumbnail((target_width, target_height), Image.LANCZOS)
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG') 
        img_file = ContentFile(img_bytes.getvalue())
        upload_path = os.path.join(settings.MEDIA_ROOT, 'Post_Image', user.username, f'{post.id}', image.name)

        saved_path = default_storage.save(upload_path, img_file)

        saved_image_paths.append(saved_path)

    return saved_image_paths

def post_images(username, post):
    id = post.id

    img_folder_path = f"{settings.MEDIA_ROOT}/Post_Image/{username}/{id}/"

    if not os.path.exists(img_folder_path):
        return None

    return img_folder_path

def time_setting(createtime):
    now = make_aware(datetime.now())
    time_diff = now - createtime
    
    if time_diff < timedelta(hours=24):
        hours_ago = int(time_diff.total_seconds() // 3600)
        return f"{hours_ago}h"
    else:
        return createtime.strftime("%m/%d")

def save_profile_photo(image, user):
    if not image:
        return None
    else:
        img = Image.open(image)
        target_width = 300
        target_height = 300
        img.thumbnail((target_width, target_height), Image.LANCZOS)
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG') 
        img_file = ContentFile(img_bytes.getvalue())
        upload_path = os.path.join(settings.MEDIA_ROOT, 'Profile_Photo', user.username, 'head.png')

        saved_path = default_storage.save(upload_path, img_file)

    return saved_path
