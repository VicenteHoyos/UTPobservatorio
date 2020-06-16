from django.urls import include, path

from portal import views

urlpatterns = [
    path('',views.inicio, name='inicio'),    
    path('contact',views.contacto, name='contact'),
    path('invite',views.invitacionAdmin, name='inviteadmin'),      
    path('solicitud_registro',views.solicitud_registro, name='solicitudregistro'),      

]