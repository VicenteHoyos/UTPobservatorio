from django.contrib import admin
from .models import Profile, Follower


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['id','user']

admin.site.register(Follower)