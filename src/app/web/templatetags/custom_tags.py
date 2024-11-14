from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def get_url(name):
    return reverse(name)
