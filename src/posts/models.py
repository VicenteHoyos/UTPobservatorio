from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from datetime import date

# Create your models here.
# Modelo Intereses 
#class Intereses 

class Interes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=30, unique= True, null=False)
    descripcion=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True , auto_now = False)

    # posts = models.ForeignKey( Post , on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('portal:inicio') #namespace posts
        #"/posts/%s/" %(self.id)

class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte= timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Post (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE) 
    titulo = models.CharField(max_length= 150)
    slug = models.SlugField(unique= True)
    imagen = models.ImageField(upload_to=upload_location,
        null = True,
        blank = True,
        height_field="height_field", 
        width_field="width_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    contenido=models.TextField()
    draft = models.BooleanField(default= False)
    publish = models.DateField(auto_now_add=False , auto_now = False, default = timezone.now())
    timestamp = models.DateTimeField(auto_now_add=True , auto_now = False, editable=False)
    actualizado= models.DateTimeField(auto_now_add=False , auto_now = True)
    objects = PostManager()
    
    # interes= models.CharField(max_length=150)

    #interes = models.ForeignKey(Interes,  on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Interes ,verbose_name='Categorías')

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={"slug":self.slug}) #namespace posts
        #"/posts/%s/" %(self.id)
    
    # def save(self, *args): # args will be M2M data
    #     super().save() # now that the instance is saved, we can access toppings
    #     if args:
    #         self.categorias.add(*args)

    class Meta:
        ordering = ["-timestamp","actualizado"]

def create_slug(instance, new_slug= None):
    slug = slugify(instance.titulo)
    if new_slug is not None:
        slug = new_slug
    queryset = Post.objects.filter(slug= slug).order_by("-id")
    exists = queryset.exists()
    if exists:
        new_slug="%s-%s" %(slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
