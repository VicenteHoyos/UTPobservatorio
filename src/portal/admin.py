from django.contrib import admin

# Register your models here.
from .forms import RegModelForm, ContactForm , InvitacionAdminForm#formulario
from .models import Registrado, Contacto, InvitacionAdmin, DBEgresado


class AdminEgresados(admin.ModelAdmin):
	list_display = ["nombre", "email", "programa"]
	search_fields = ["email"]
	class Meta:
		model = DBEgresado

class AdminRegistrado(admin.ModelAdmin):
	list_display = ["email", "nombre", "timestamp"]
	form = RegModelForm
	# list_display_links = ["nombre"]
	list_filter = ["timestamp"]
	list_editable = ["nombre"]
	search_fields = ["email", "nombre"]
	# class Meta:
	# 	model = Registrado

class AdminInvitacionAdmin(admin.ModelAdmin):
	list_display = ["email", "nombre", "timestamp"]
	form = InvitacionAdminForm
	# list_display_links = ["nombre"]
	list_filter = ["timestamp"]
	list_editable = ["nombre"]
	search_fields = ["email", "nombre"]


class AdminContacto(admin.ModelAdmin):
	list_display = ["email", "nombre","comentario", "timestamp"]
	form = ContactForm 
    # list_display_links = ["nombre"]
	list_filter = ["timestamp"]
	list_editable = ["nombre"]
	search_fields = ["email", "nombre"]


admin.site.register(DBEgresado, AdminEgresados)
admin.site.register(Registrado, AdminRegistrado)
admin.site.register(Contacto, AdminContacto)
admin.site.register(InvitacionAdmin, AdminInvitacionAdmin)