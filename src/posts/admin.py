from django.contrib import admin

from .models import Post , Interes
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display=["titulo","actualizado","post_categories","timestamp"]
    list_display_links=["actualizado"]
    list_filter = ["timestamp"]
    search_fields = ["titulo","contenido"]
    # list_editable = ["titulo"]

    def post_categories(self, obj):
        print(isinstance(obj, Post))
        return ', '.join(
            [c.nombre for c in obj.categorias.all().order_by('nombre')])
    post_categories.short_description = 'Categorias'
     
    class Meta:
        model = Post
    

    

class InteresModelAdmin(admin.ModelAdmin):
    list_display=["nombre","descripcion","timestamp"]
    list_display_links=["nombre"]
    list_filter = ["timestamp"]
    
    class Meta:
        model = Interes

admin.site.register(Post, PostModelAdmin)
admin.site.register(Interes, InteresModelAdmin)
