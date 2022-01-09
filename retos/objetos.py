from django.db.models import Sum
from datetime import date
from django.contrib.humanize.templatetags import humanize
from dateutil.relativedelta import *
import json

from retos.utiles import normalizar_float, formatear_fecha



class RetoObject():
    id = -1
    nombre = ""
    fecha_inicio = None
    fecha_fin = None
    unidad = ""
    objetivo = 0

    progreso = 0
    promedio = 0
    promedio_necesario = 0
    porcentaje = 0

    ultimo_progreso = None

    maxima_diaria = None

    #Si está fuera del plazo del reto no se puede añadir progreso
    can_add = False

    datos_grafico = []

    def __init__(self, reto_qs, *args, **kwargs):
        self.id = reto_qs.id
        self.nombre = reto_qs.nombre
        self.fecha_inicio = reto_qs.fecha_inicio
        self.fecha_fin = reto_qs.fecha_fin
        self.unidad = reto_qs.unidad
        self.objetivo = reto_qs.objetivo

        #Calcular progreso
        self.progreso = reto_qs.progreso_set.aggregate(Sum("cantidad"))["cantidad__sum"]
        if self.progreso is None:
            self.progreso = 0
        
        #Calcular Promedio
        hoy = date.today()
        if self.fecha_inicio > hoy:
            self.promedio = 0
        else:
            fecha_referencia = hoy
            if hoy > self.fecha_fin:
                fecha_referencia = self.fecha_fin

            dias_pasados = (fecha_referencia - self.fecha_inicio).days + 1
            self.promedio = round(self.progreso / (dias_pasados), 2)


        #Promedio Necesario
        self.promedio_necesario = round(self.objetivo / ((self.fecha_fin - self.fecha_inicio).days + 1), 2)
        
        #Calcular Porcentaje
        self.porcentaje = self.progreso/self.objetivo

        #Calcular Último Progreso
        ultimo_progreso = reto_qs.progreso_set.order_by("-fecha").first()
        if ultimo_progreso is not None:
            self.ultimo_progreso_cantidad = ultimo_progreso.cantidad
            self.ultimo_progreso_tiempo = humanize.naturaltime(ultimo_progreso.fecha).split(",")[0]
        else:
            self.ultimo_progreso_cantidad = None

        #Calcular Progreso Hoy
        self.progreso_hoy = reto_qs.progreso_set.filter(fecha_dia=hoy).aggregate(Sum("cantidad"))["cantidad__sum"]
        if self.progreso_hoy is None:
            self.progreso_hoy = 0

        
        #Calcular Máxima Diaria
        max = reto_qs.progreso_set.order_by("-cantidad")
        max = reto_qs.progreso_set.values("fecha_dia").annotate(cant=Sum("cantidad")).order_by("-cant")
        self.maxima_diaria = None
        if len(max) > 0:
            self.maxima_diaria = max[0]

        
        #Calcular Datos Gráfico
        #delta = datetime.timedelta(months=+1)
        delta = relativedelta(months=1)
        fecha_aux = self.fecha_inicio
        self.labels = []
        self.data = []
        
        reto_por_mes = reto_qs.progreso_set.values("fecha_mes").annotate(cant=Sum("cantidad")).order_by() 
        reto_dict = dict()
        for retopm in reto_por_mes:
            mes = str(retopm["fecha_mes"].month) + "-" + str(retopm["fecha_mes"].year)
            reto_dict[mes] = retopm["cant"]


        while(fecha_aux <= self.fecha_fin):
            mes = str(fecha_aux.month) + "-" + str(fecha_aux.year)
            cantidad = 0
            if mes in reto_dict:
                cantidad = reto_dict[mes]

            self.labels.append(fecha_aux.strftime("%b") + " " + str(fecha_aux.year)[2:])
            self.data.append(cantidad)
            fecha_aux += delta

        self.labels = json.dumps(self.labels)
        self.data = json.dumps(self.data)


        


    def get_objetivo(self):
        return normalizar_float(self.objetivo)

    def get_progreso(self):
        return normalizar_float(self.progreso)
    
    def get_promedio(self):
        return normalizar_float(self.promedio)
    
    def get_promedio_necesario(self):
        return normalizar_float(self.promedio_necesario)

    def get_ultimo_progreso(self):
        pass

    def get_progreso_hoy(self):
        return normalizar_float(self.progreso_hoy)

    def get_maxima_diaria(self):
        pass

    def get_fecha_inicio(self):
        return formatear_fecha(self.fecha_inicio)

    def get_fecha_fin(self):
        return formatear_fecha(self.fecha_fin)


    def ha_empezado(self):
        if self.fecha_inicio > date.today():
            return False
        return True

    def ha_acabado(self):
        if self.fecha_fin >= date.today():
            return False
        return True

    def esta_activo(self):
        return self.ha_empezado() and not self.ha_acabado()
