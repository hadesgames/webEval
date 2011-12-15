import creoleparser
from datetime import datetime

from django import template
from django.utils.timesince import timesince

register = template.Library()

# returns sorted dict
def sorted_dict (value):
    return sorted(value.iteritems())
register.filter('sorted_dict', sorted_dict)


def timedelta (value, arg=None):
    if not value:
        return ''
    if arg:
        cmp = arg
    else:
        cmp = datetime.now()
    if value > cmp:
        return "%s" % timesince(cmp,value)
    else:
        return "%s" % timesince(value,cmp)
register.filter('timedelta',timedelta)

def timeanddate_template (value):
    return value.strftime("day=%d&month=%m&year=%Y&hour=%H&min=%M&sec=%S")
register.filter('timeanddate_template', timeanddate_template)

def even (value):
    return value % 2 == 0
register.filter('even', even)

def xrange1 (value):
    return xrange(1, value + 1)
register.filter('xrange1', xrange1)

def status_urllize (value, page):
    value.append('page=%d' % page)
    return "?" + '&'.join(value)
register.filter('status_urllize', status_urllize)

def registered (value, arg):
    return len(value.registered_users.filter(username=arg.username)) != 0
register.filter('registered', registered)

