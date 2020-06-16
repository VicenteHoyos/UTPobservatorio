from django import forms
from datetime import date

from .models import User
from posts.models import Interes


class userForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={"imagen_Perfil",
        "username",
        "first_name",
        "last_name",
        "email", 
         "website",
         "telefono",
         "ciudad", 
         "dni_administrador",
         "fecha_Nacimiento",
         "genero",
         "Confirmacion_manejo_datos_sensibles",
         "biografia"
        }
        # widgets = {
        #     'fecha_Nacimiento': forms.SelectDateWidget(),
        #     }

    def clean_dni_administrador(self):
        dni_administrador = self.cleaned_data.get("dni_administrador")
        if dni_administrador < 4000000 or dni_administrador > 1999999999:
            raise forms.ValidationError("Su Cedula esta fuera del rango permitido")
        else:
            return dni_administrador

    def clean_fecha_Nacimiento(self):
        fecha_Nacimiento = self.cleaned_data.get("fecha_Nacimiento")
        if fecha_Nacimiento > date.today():
            raise forms.ValidationError("Su fecha de nacimiento no puede ser mayor a la fecha actual del sistema")
        else:
            return fecha_Nacimiento
    
    def clean_Confirmacion_manejo_datos_sensibles(self):
        Confirmacion_manejo_datos_sensibles = self.cleaned_data.get("Confirmacion_manejo_datos_sensibles")
        if Confirmacion_manejo_datos_sensibles == False:
            raise forms.ValidationError("Por favor debe confirmar el manejo de datos")
        else:
            return Confirmacion_manejo_datos_sensibles
    
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
                        return email
            raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co")

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if telefono < 3000000000 or telefono > 3519999999:
            raise forms.ValidationError("Su numero de telefono esta fuera del rango permitido")
        else:
            return telefono


class userEgresadoForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={"imagen_Perfil",
        "username",
        "first_name",
        "last_name",
        "email", 
         "website",
         "telefono",
         "ciudad", 
         "dni_administrador",
         "fecha_Nacimiento",
         "genero",
         "Confirmacion_manejo_datos_sensibles",
         "biografia",
         'categorias'
        }
        widgets = {
        'categorias': forms.CheckboxSelectMultiple(),
        # 'fecha_Nacimiento': forms.SelectDateWidget(),
        
        }
    # categorias = forms.ModelMultipleChoiceField(queryset=Interes.objects.all())
    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if telefono < 3000000000 or telefono > 3519999999:
            raise forms.ValidationError("Su numero de telefono esta fuera del rango permitido")
        else:
            return telefono

    def clean_dni_administrador(self):
        dni_administrador = self.cleaned_data.get("dni_administrador")
        if dni_administrador < 4000000 or dni_administrador > 1999999999:
            raise forms.ValidationError("Su Cedula esta fuera del rango permitido")
        else:
            return dni_administrador

    def clean_fecha_Nacimiento(self):
        fecha_Nacimiento = self.cleaned_data.get("fecha_Nacimiento")
        if fecha_Nacimiento > date.today():
            raise forms.ValidationError("Su fecha de nacimiento no puede ser mayor a la fecha actual del sistema")
        else:
            return fecha_Nacimiento

    def clean_Confirmacion_manejo_datos_sensibles(self):
        Confirmacion_manejo_datos_sensibles = self.cleaned_data.get("Confirmacion_manejo_datos_sensibles")
        if Confirmacion_manejo_datos_sensibles == False:
            raise forms.ValidationError("Por favor debe confirmar el manejo de datos")
        else:
            return Confirmacion_manejo_datos_sensibles

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
                        return email
            raise forms.ValidationError("Por favor utiliza un correo institucional @utp.edu.co")

    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categorias'] = [t.pk for t in 
                kwargs['instance'].categorias.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.categorias.clear()
            for interes in self.cleaned_data['categorias']:
                instance.categorias.add(interes)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        #if commit:
        instance.save()
        self.save_m2m()

        return instance

class userAgregarInteresForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {
          'categorias'
        }
        widgets = {
         'categorias': forms.CheckboxSelectMultiple(),
        }
    # categorias = forms.ModelMultipleChoiceField(queryset=Interes.objects.all())

    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categorias'] = [t.pk for t in 
                kwargs['instance'].categorias.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.categorias.clear()
            for interes in self.cleaned_data['categorias']:
                instance.categorias.add(interes)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        #if commit:
        instance.save()
        self.save_m2m()

        return instance

class userEnableForm(forms.ModelForm):
    class Meta:
        model = User
        fields ={
        # "username",
        # "email", 
        "Administrador", 
        }

class userEnableEgresadoForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={
        # "username",
        # "email", 
        "Egresado", 
        }

class userDisableForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={
        # "username",
        # "email",
        "Administrador", 
        }
class userDisableEgresadoForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={
        # "username",
        # "email",
        "Egresado", 
        }

class userAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={
        # "username",
        "first_name",
        "last_name",
        # "email", 
         "website",
         "telefono",
         "ciudad", 
         "genero",
         "biografia"
        }

class userEgresadoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields ={
        # "username",
        "first_name",
        "last_name", 
         "website",
         "telefono",
         "ciudad",
         "biografia",
        }
    