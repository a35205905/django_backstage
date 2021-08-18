from django.core.exceptions import ValidationError

def validate_image(image):
    file_size = image.file.size
    limit_mb = 2

    if file_size > limit_mb * 1024 * 1024:
       raise ValidationError("大小不超過：{} MB".format(limit_mb))

def validate_pdf(pdf):
    file_size = pdf.file.size
    limit_mb = 10

    if file_size > limit_mb * 1024 * 1024:
       raise ValidationError("大小不超過：{} MB".format(limit_mb))