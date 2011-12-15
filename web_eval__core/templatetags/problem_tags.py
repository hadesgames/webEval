from django import template

register = template.Library()

# checks if problem is visible by user
def visible(problem, user):
    return problem.can_view(user)
register.filter('visible', visible)
