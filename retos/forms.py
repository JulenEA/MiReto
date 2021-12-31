from django import forms
from .models import Reto

class CrearRetoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre del Reto")
    objetivo = forms.IntegerField()
    unidad = forms.CharField(label="Unidades", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Flexiones, Dominadas, KM...'}))
    fecha_inicio = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))
    fecha_fin = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ))


    

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        fecha_fin = self.cleaned_data['fecha_fin']


        if fecha_inicio > fecha_fin:
            raise forms.ValidationError("Las fechas son incorrectas")
    
        return fecha_fin



class AddProgresoForm(forms.Form):
    cantidad = forms.FloatField()
    reto = forms.ModelChoiceField(queryset=None)
    
    # def __init__(self, *args, **kwargs):
        
    #     super(AddProgresoForm, self).__init__(args, kwargs)
    #     retos = Reto.objects.all()
    #     self.fields["retos"] = forms.ModelChoiceField(queryset=retos)

