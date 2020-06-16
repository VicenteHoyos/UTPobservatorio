from django.conf.urls import url
from . import views
from django.urls import  path

urlpatterns = [
	path('list/', views.listview, name="home"),

	path('follow/',views.user_follow,name="user_follow"),

	path('follow/<int:id>', views.detailview, name="user_detail"),

]