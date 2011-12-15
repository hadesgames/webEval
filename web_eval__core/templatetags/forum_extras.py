import postmarkup

from django import template

register = template.Library()

# translates bbcode syntax to html
def bbcode(value):
    markup = postmarkup.PostMarkup()
    markup.default_tags()
    return markup.render_to_html(value)
register.filter('bbcode', bbcode)