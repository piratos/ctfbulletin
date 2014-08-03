__author__ = 'piratos'
from django import template
register = template.Library()


@register.filter(name='larger')
def larger(value, than):
    if len(value) > than:
        return True
    return False