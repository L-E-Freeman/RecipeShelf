from django import template

# To be a valid tag library, module must contain a module-level variable named
# register that is a template.Library instance, in which all the tags and 
# filters are registered.
register = template.Library()


@register.filter
def duration(td):

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return '{} hr. {} min.'.format(hours, minutes)
    else:
        return '{} min.'.format(minutes)
