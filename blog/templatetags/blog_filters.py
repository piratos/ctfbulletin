__author__ = 'piratos'
from django import template, templatetags
register = template.Library()

@register.filter(name='url_it')
def url_it(value):
    return value.replace(' ', '_')