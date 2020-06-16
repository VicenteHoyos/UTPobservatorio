from django import forms

from .models import Registrado,InvitacionAdmin, Contacto, DBEgresado #se importa el modelo

class RegModelForm(forms.ModelForm):
	Egresados = DBEgresado.objects.all()
	class Meta:
		model = Registrado
		fields = ["nombre", "email",]

	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_base, proveeder = email.split("@")
		if proveeder == "gmail.com":
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co")
		else:
			dominio, extension, pais = proveeder.split(".")
			if dominio =="utp":
				if extension == "edu":
					if pais == "co":
						Egresados = DBEgresado.objects.all()
						for user in Egresados:
							if user.email == email:
								return email
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co, o revisa si eres egresado")

	def clean_nombre(self):
		nombre = self.cleaned_data.get("nombre")
		#validaciones
		return nombre

class InvitacionAdminForm(forms.ModelForm):
	Egresados = DBEgresado.objects.all()
	class Meta:
		model = InvitacionAdmin
		fields = ["nombre", "email",]

	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_base, proveeder = email.split("@")
		if proveeder == "gmail.com":
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co")
		else:
			dominio, extension, pais = proveeder.split(".")
			if dominio =="utp":
				if extension == "edu":
					if pais == "co":
						Egresados = DBEgresado.objects.all()
						for user in Egresados:
							if user.email == email:
								return email
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co, o revisa si es egresado")
		

	def clean_nombre(self):
		nombre = self.cleaned_data.get("nombre")
		#validaciones
		return nombre
		
class ContactForm(forms.ModelForm):
	Egresados = DBEgresado.objects.all()
	class Meta:
		model = Contacto
		fields = ["nombre","comentario",]

	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_base, proveeder = email.split("@")
		if proveeder == "gmail.com":
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co")
		else:
			dominio, extension, pais = proveeder.split(".")
			if dominio =="utp":
				if extension == "edu":
					if pais == "co":
						Egresados = DBEgresado.objects.all()
						for user in Egresados:
							if user.email == email:
								return email
			raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co, o revisa si esta correctamente escrito")
		

	def clean_nombre(self):
		nombre = self.cleaned_data.get("nombre")
		#validaciones
		return nombre