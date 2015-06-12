from django import template

register = template.Library()


@register.filter(name='get_object_index')
def get_object_index(objects, index):
    return objects[index].library_owner
