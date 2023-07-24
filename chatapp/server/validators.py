import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimensions for the image 70x70 - size of uploaded image {img.size}"
                )


# Bu fonksiyon, bir tuple (demet) döndürür,
# ve bu demetin ilk öğesi dosya adını, ikinci öğesi ise uzantıyı içerir.
def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension")
