from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def image_tag(image_url, width, height):
    """
    Шаблонный тег для вывода изображения с изменением размера.
    Пример использования: {% image_tag "url/to/image.jpg" 300 300 %}
    """
    return format_html('<img src="{}" width="{}" height="{}"/>', image_url, width, height)
