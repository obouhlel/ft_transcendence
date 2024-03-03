from django import template
import datetime

register = template.Library()

@register.filter
def to_date_string(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    return ''