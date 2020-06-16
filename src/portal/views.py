from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .forms import RegModelForm , ContactForm, InvitacionAdminForm
from .models import Registrado, Contacto, InvitacionAdmin

# Create your views here.
def inicio(request):
	titulo = "Suscribete"
	# if request.user.is_authenticated:
	# 	titulo = "Bienvenid@ %s" %(request.user) #saludo 
	form = RegModelForm(request.POST or None)

	context = {
				"titulo": titulo,
				"form_register": form,
			}

	if form.is_valid():
		# comentario = form.cleaned_data.get("comentario")
		instance = form.save(commit = False)
		form_email = form.cleaned_data.get("email")
		form_nombre = form.cleaned_data.get("nombre")
		asunto = 'Solicitud Registro Observatorio Egresados'
		email_from = settings.EMAIL_HOST_USER
		email_to = [email_from]
		email_mensaje = "%s: Solicitud Registro Cuenta Enviado por %s Enviado a %s" %(form_nombre , form_email, email_to)
		send_mail(asunto, 
			email_mensaje,
			email_from,
			email_to,
			fail_silently=False
			)

		asunto2 = 'Invitacion Egresado Observatorio Egresados'
		link ='http://EgresadosTecnologica.pythonanywhere.com/accounts/register/'
		email_to2 = [form_email]
		email_mensaje2 = "Cordial saludo %s: Dando respuesta a su solicitud lo invitamos a formar parte de la plataforma Observatorio de Egresados. Para crear su cuenta ingreser al link %s de lo contrario haga caso omiso a este correo, la habilitacion de su cuenta esta sujeta a criterio de nuestro grupo de administradores. Enviado por %s." %(form_nombre,link,email_from)
		send_mail(asunto2, 
			email_mensaje2,
			email_from,
			email_to2,
			fail_silently=False
			)

		instance.user = request.user
		instance.save()	
		return HttpResponseRedirect(instance.get_absolute_url())
	return render(request, "inicio.html", context)

def solicitud_registro(request):
	titulo = "Solicitud Registro"
	# if request.user.is_authenticated:
	# 	titulo = "Bienvenid@ %s" %(request.user) #saludo 
	form = RegModelForm(request.POST or None)

	context = {
				"titulo": titulo,
				"form_register": form,
			}

	if form.is_valid():		
		# comentario = form.cleaned_data.get("comentario")
		instance = form.save(commit = False)
		form_email = form.cleaned_data.get("email")
		form_nombre = form.cleaned_data.get("nombre")
		asunto = 'Solicitud Registro Observatorio Egresados'
		email_from = settings.EMAIL_HOST_USER
		email_to = [email_from]
		email_mensaje = "%s: Solicitud Registro Cuenta Enviado por %s Enviado a %s" %(form_nombre , form_email, email_to)
		send_mail(asunto, 
			email_mensaje,
			email_from,
			email_to,
			fail_silently=False
			)
		
		asunto2 = 'Invitacion Egresado Observatorio Egresados'
		link ='http://EgresadosTecnologica.pythonanywhere.com/accounts/register/'
		email_to2 = [form_email]
		email_mensaje2 = "Cordial saludo %s: Dando respuesta a su solicitud lo invitamos a formar parte de la plataforma Observatorio de Egresados. Para crear su cuenta ingreser al link %s de lo contrario haga caso omiso a este correo, la habilitacion de su cuenta esta sujeta a criterio de nuestro grupo de administradores. Enviado por %s." %(form_nombre,link,email_from)
		send_mail(asunto2, 
			email_mensaje2,
			email_from,
			email_to2,
			fail_silently=False
			)
		
		
		instance.user = request.user
		instance.save()	
		return HttpResponseRedirect(instance.get_absolute_url())

	if not request.user.is_authenticated:
		return render(request, "solicitud_register.html", context)
	else:
		raise PermissionDenied
	
#Invitar administrador
def invitacionAdmin(request):
	titulo = "Invitar Administrador"
	form = InvitacionAdminForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		form_email = form.cleaned_data.get("email")
		form_nombre = form.cleaned_data.get("nombre")
		asunto = 'Invitacion Administrador Observatorio Egresados'
		link ='http://EgresadosTecnologica.pythonanywhere.com/accounts/register/'
		email_from = settings.EMAIL_HOST_USER
		email_to = [form_email]
		email_mensaje = "Cordial saludo %s: El presente correo es para invitarlo a formar parte del grupo de administradores de Observatorio de Egresados. Para crear su cuenta ingreser al link %s de lo contrario haga caso omiso a este correo. Enviado por %s.  " %(form_nombre,link,email_from)
		send_mail(asunto, 
			email_mensaje,
			email_from,
			email_to,
			fail_silently=False
			)
		instance.user = request.user
		instance.save()	
		messages.success(request, "Tu mensaje ha sido enviado con Exito")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form_contacto": form,
		"titulo": titulo,
	}
	if request.user.is_superuser:
		return render(request, "inviteadmin.html", context)
	else:
		raise PermissionDenied
	
#Enviar Comentario acerca de la plataforma
def contacto(request):
	titulo = "Comentario"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		form_email = request.user.email
		form_mensaje = form.cleaned_data.get("comentario")
		form_nombre = form.cleaned_data.get("nombre")
		asunto = 'Contacto Observatorio Egresados'
		email_from = settings.EMAIL_HOST_USER
		email_to = [email_from]
		email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
		send_mail(asunto, 
			email_mensaje,
			email_from,
			email_to,
			fail_silently=False
			)
		instance.user = request.user
		instance.save()	
		messages.success(request, "Tu mensaje ha sido enviado con Exito")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form_contacto": form,
		"titulo": titulo,
	}
	if request.user.Administrador or request.user.Egresado:
		return render(request, "contacto.html", context)
	else:
		raise PermissionDenied







