from django.shortcuts import render
from django.views.generic import CreateView,TemplateView, UpdateView, FormView,ListView,DetailView, DeleteView,View
from .models import Personal,Administradores,Minutas,Eventos
from django.core.urlresolvers import reverse_lazy
from Pacientes.forms import HistorialMedico_Form
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import auth
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime, time, date, timedelta

class Index_view(TemplateView):
	template_name = 'index.html'

# Create your views here.
class Registro_Minutas(CreateView):
	template_name='registro_minutas.html'
	model=Minutas
	fields='__all__'
	success_url=reverse_lazy('reporte_minutas')

class Detalle_minuta(DetailView):
	template_name='detalle_minuta.html'
	model=Minutas

class Reporte_Minutas(ListView):
	template_name='reporte_minutas.html'
	model=Minutas

class Registro_Eventos(CreateView):
	template_name='registro_eventos.html'
	model=Eventos
	fields='__all__'
	success_url=reverse_lazy('reporte_eventos')

class Eliminar_Eventos(DeleteView):
    model = Eventos
    success_url = reverse_lazy('reporte_eventos')
 
class Editar_Evento(UpdateView):
  	model=Eventos
  	fields='__all__'
  	template_name='editar_evento.html'
  	success_url=reverse_lazy('reporte_eventos')

class Reporte_Eventos(ListView):
	template_name='reporte_eventos.html'
	model=Eventos

class Detalle_eventos(DetailView):
	template_name='detalle_evento.html'
	model=Eventos

class Registro_Personal(CreateView):
	template_name='registro_personal.html'
	model=Personal
	fields='__all__'
	success_url=reverse_lazy('reporte_personal')

#class Eliminar_Personal(DeleteView):
#   model = Personal
#    success_url = reverse_lazy('reporte_personal')

class Editar_Personal(UpdateView):
  	model=Personal
  	fields='__all__'
  	template_name='editar_personal.html'
  	success_url=reverse_lazy('reporte_personal')

class Reporte_Personal(ListView):
	template_name='reporte_personal.html'
	model=Personal


class CrearUsAdmon(PermissionRequiredMixin,CreateView):
	permission_required='crear_admin'
	template_name='crear_admon.html'
	model=Administradores
	fields='__all__'
	success_url=reverse_lazy('login')

class EliminarAdmon(PermissionRequiredMixin,DeleteView):
	permission_required='crear_admin'
	model=Administradores
	success_url = reverse_lazy('report_admon')

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

class ReporteAdmindores(PermissionRequiredMixin,ListView):
	permission_required='crear_admin'
	template_name='reporte_admones.html'
	model=Administradores

def AsignarPermiso(request,pk):
	
	return HttpResponseRedirect('/reporte_personal')



class Donar(TemplateView):
	template_name='donaciones.html'

class Galeria(TemplateView):
	template_name='galeria2.html'

class Personal_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(120, 740, u"Reporte Personal")
		pdf.setFont("Helvetica", 14)
		fr=date.today()
		pdf.drawString(240, 720, fr.strftime('%m/%d/%Y'))

	def tabla1(self,pdf,y):
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Nombre', 'Funcion', 'Telefono','Correo')
		#Creamos una lista de tuplas que van a contener a las persona

		detalles = [(p.Personal_nombre+" "+p.Personal_apellidos, p.Personal_funcion, p.Personal_tel, p.Personal_correo) for p in Personal.objects.all()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[150 , 100, 100 , 150 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 650
		self.tabla1(pdf, y)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

class Minuta_pdf(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que esta guardado en la carpeta media/imagenes
		archivo_imagen = 'static/img/logosepher.png'
		#Definimos el tamano de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 20, 740, 160, 120,preserveAspectRatio=True)
		pdf.setFont("Helvetica-Bold", 20)
		#Dibujamos una cadena en la ubicacion X,Y especificada
		pdf.drawString(120, 740, u"Reporte Minuta")
		pdf.setFont("Helvetica", 14)


	def tabla1(self,pdf,y):
	Fecha_reunion=models.DateField()
    Asistentes=models.ManyToManyField(Administradores)
    Total_donacionesmon=models.DecimalField(max_digits=10,decimal_places=4)
    Valor_donacionesesp=models.DecimalField(max_digits=10,decimal_places=4)
    Duracion_reunion=models.CharField(max_length=15)
    Pacientes_beneficiados=models.IntegerField()
    Observaciones=models
    p=Minutas.objects.get(pk=pk).select_related("Asistentes")
    	detalles=(['Fecha reunion'],
    				[p.Fecha_reunion],
    				['Asistentes'],)
		detalles = [(p.Personal_nombre+" "+p.Personal_apellidos, p.Personal_funcion, p.Personal_tel, p.Personal_correo) for p in Personal.objects.all()]

		#Establecemos el tamano de cada una de las columnas de la tabla
		detalle_orden = Table([('Fecha')] + detalles, colWidths=[150 , 100, 100 , 150 ])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
			#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				('TEXTCOLOR',(0,0),(3,0),colors.black),
				#Los bordes de todas las celdas seran de color negro y con un grosor de 1
				('BACKGROUND',(0,0),(3,0),colors.gainsboro),
				
				('GRID', (0, 0), (-1, -1), 1, colors.gray), 
				#El tamano de las letras de cada una de las celdas sera de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamano de la hoja que ocupara la tabla 
		detalle_orden.wrapOn(pdf, 800, 500)
		#Definimos la coordenada donde se dibujara la tabla
		detalle_orden.drawOn(pdf, 35,y)    

	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al metodo cabecera donde estan definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 650
		self.tabla1(pdf, y)
		#Con show page hacemos un corte de pagina para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response
