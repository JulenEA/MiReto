from django.contrib.humanize.templatetags import humanize

def normalizar_float(numero):
    result = None
    if numero - int(numero) > 0:
        result = round(numero, 2)
    else: 
        result = int(numero)

    result = str(result).replace(".", "C")
    return humanize.intcomma(result).replace(",", ".").replace("C", ",")


    

def formatear_fecha(fecha):
    return fecha.strftime("%d/%m/%Y")