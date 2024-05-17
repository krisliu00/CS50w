from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os


def save_images(images, user, post):
    saved_image_paths = []

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
