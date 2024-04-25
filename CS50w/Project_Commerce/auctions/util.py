from django.core.files.storage import default_storage

def save_images(images, item_number):
    saved_image_paths = []
    for image in images:
        upload_path = f'items/{item_number}/{image.name}'
        saved_path = default_storage.save(upload_path, image)
        saved_image_paths.append(saved_path)
    return saved_image_paths