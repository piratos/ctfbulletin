__author__ = 'piratos'
from django import template
register = template.Library()

@register.filter(name='rank_it')
def rank_it(value, team_list=[]):
    return team_list.index(value)+1