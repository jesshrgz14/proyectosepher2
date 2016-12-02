from __future__ import unicode_literals
from datetime import datetime, time, date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Personal(models.Model):
    Personal_nombre=models.CharField(max_length=40,validators=[RegexValidator(regex='^[a-zA-Z\s]*$',message="Valor invalido")])
    Personal_apellidos=models.CharField(max_length=50,validators=[RegexValidator(regex='^[a-zA-Z\s]*$',message="Valor invalido")])
    Personal_funcion=models.CharField(max_length=60)
    Personal_tel=models.CharField(max_length=15)
    Personal_correo=models.EmailField()

    def __unicode__(self):
        return "Nombre: %s - Apellido: %s"%(self.Personal_nombre,self.Personal_apellidos) 

class Administradores(models.Model):
    perfil=models.OneToOneField(User,on_delete=models.CASCADE,)
    Admon_nombre=models.CharField(max_length=40,validators=[RegexValidator(regex='^[a-zA-Z]\s*$',message="Valor invalido")])
    Admon_tel=models.CharField(max_length=15,validators=[RegexValidator(regex='^[0-9|\\-]*$',message="Ingrese un numero de telefono valido")])
    Admon_correo=models.EmailField()
    class Meta:
        permissions = (
            ("editar", "Edicion de registros"),
            ("crear_admin","Crear administradores"),
            ("asig_permisos","Asignar permisos"),
            )

    def __unicode__(self):
        return "Nombre: %s "%(self.Admon_nombre) 

class Minutas(models.Model):
    Fecha_reunion=models.DateField()
    Asistentes=models.ManyToManyField(Administradores)
    Total_donacionesmon=models.DecimalField(max_digits=10,decimal_places=4)
    Valor_donacionesesp=models.DecimalField(max_digits=10,decimal_places=4)
    Duracion_reunion=models.CharField(max_length=15)
    Pacientes_beneficiados=models.IntegerField()
    Observaciones=models.TextField()

    def __unicode__(self):
        return "Fecha_reunion: %s "%(self.Fecha_reunion) 

class Eventos(models.Model):
    Nombre_evento=models.CharField(max_length=30)
    Fecha_evento=models.DateField()
    Lugar_evento=models.CharField(max_length=100)
    Personal_evento=models.ManyToManyField(Personal)
    Hora_evento=models.TimeField()

    def __unicode__(self):
        return "Nombre: %s - Apellido: %s"%(self.Nombre_evento,self.Fecha_evento) 




