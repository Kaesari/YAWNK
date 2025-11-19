from django import template
from itertools import groupby
from operator import itemgetter

register = template.Library()

@register.filter
def groupby(value, key):
    """Group a list of dictionaries by a specific key."""
    try:
        sorted_value = sorted(value, key=itemgetter(key))
        grouped = groupby(sorted_value, key=itemgetter(key))
        return {k: list(v) for k, v in grouped}
    except Exception as e:
        print(f"Error in groupby filter: {e}")
        return value
