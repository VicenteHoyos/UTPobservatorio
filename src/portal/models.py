from __future__ import unicode_literals
from django.urls import reverse
from django.db import models

# Create your models here.
class DBEgresado(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(unique=True, null=False)
	programa = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self): #Python 3
		return self.email

class Registrado(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(unique=True, null=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self): #Python 3
		return self.email

	def get_absolute_url(self):
		return reverse('portal:inicio') #namespace posts
        #"/posts/%s/" %(self.id)

class InvitacionAdmin(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(unique=True, null=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self): #Python 3
		return self.email

	def get_absolute_url(self):
		return reverse('portal:inviteadmin') #namespace posts
        #"/posts/%s/" %(self.id)

class Contacto(models.Model):
	nombre = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField()
	comentario = models.TextField(null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self): #Python 3
		return self.email

	def get_absolute_url(self):
		return reverse('portal:inicio') #namespace posts
        #"/posts/%s/" %(self.id)