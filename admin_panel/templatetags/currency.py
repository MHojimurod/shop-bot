from django import template

register = template.Library()


import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


@register.simple_tag
def money(number:int, grouping:bool=True):
    print(locale.currency(number, grouping=grouping)[1:],"bbb")
    return f"{locale.currency(number, grouping=grouping)[1:]}"