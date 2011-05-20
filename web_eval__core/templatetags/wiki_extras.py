import creoleparser

from django import template
from webEval.web_eval__core.wiki__helper import *
register = template.Library()

# translates creole syntax to html
def creole(value):
    return creoleparser.text2html(value)
register.filter('creole', creole)


# returns markup types
def markup_types(value):
    return ['Creole', 'Markdown', 'Textile']
register.filter('markup_types', markup_types)

# returns security types
def security_types(value):
    return ['Public', 'Protected', 'Private']
register.filter('security_types', security_types)

# chops string to first character
def first_characters(value, number):
    return value[:number]
register.filter('first_characters', first_characters)
    
# markup
def webEval_markup(value):
    return markup(value)
register.filter('webEval_markup', webEval_markup)
    