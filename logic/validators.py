from django.core.exceptions import ValidationError

def validate_img_format(value):
    valid_formats = ['png', 'jpeg', 'jpg']
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')