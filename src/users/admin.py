from django.contrib import admin

from .models import User

from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display =["id","username","password","first_name","last_name","email","is_staff","is_active","is_superuser", "Superusuario" , "Administrador" , "Egresado","imagen_Perfil", "website","telefono","ciudad", "dni_administrador","fecha_Nacimiento", "genero","Confirmacion_manejo_datos_sensibles","interes", "biografia",'last_login','date_joined']
    list_display_links=["username"]
    list_filter = ["timestamp"]
    search_fields = ["dni_administrador"]
    # list_editable = ["titulo"]

    def interes(self, obj):
        #print(isinstance(obj, User))
        return ', '.join(
            [c.nombre for c in obj.categorias.all().order_by('nombre')])
    interes.short_description = 'Categorias'

    class Meta:
        model = User

admin.site.register(User, UserAdmin)
