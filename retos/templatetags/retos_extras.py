from django import template
from retos.utiles import normalizar_float, formatear_fecha

register = template.Library()

@register.filter
def normalizar_float_tag(value):
  return normalizar_float(value)

@register.filter
def formatear_fecha_tag(value):
  return formatear_fecha(value)


@register.filter
def jsdate(fecha):
    """formats a python date into a js Date() constructor.
    """
    try:
        return "new Date({0},{1},{2},0,0,0)".format(fecha.year, fecha.month - 1, fecha.day + 1)
    except AttributeError:
        return 'undefined'