from django import template

register = template.Library()


def is_has(value, arg):
    return value.index(arg)>=0