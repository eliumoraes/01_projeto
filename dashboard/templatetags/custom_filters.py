from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  return value.split(key)


@register.filter(name='telefone')
def telefone(value):
  return '(' + value[0:3] + ') ' + value[3:7] + '-' + value[7:12]
  