from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import quote_plus
from django.db.models import Prefetch
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.

from .forms import userForm,userEgresadoForm, userEnableForm, userAdminUpdateForm , userDisableForm, userEnableEgresadoForm ,userDisableEgresadoForm, userEgresadoUpdateForm, userAgregarInteresForm
from .models import User #importo mi modelo
from portal.models import InvitacionAdmin, Registrado

#ver perfil
def user_detail(request):
    #instance= Post.objects.get(id=None)
    instance = get_object_or_404(User, id=request.user.id)
  
    context = {        
        "instance": instance,
    }

    return render(request,"user_detail.html", context)

#lista habilitar usuario administrador 
def user_enable_admin(request):
    listquery=[]
    if not request.user.is_authenticated :
        raise Http404

    if request.user.is_superuser:
        queryset = InvitacionAdmin.objects.all()
        querysetusers = User.objects.all()
        
        if len(querysetusers) >= len(queryset):
            for u in querysetusers:
                for u2 in queryset:
                    if (u.email)==(u2.email):
                        if not u.Administrador:
                            listquery.append(u)
                    else:
                        pass
        else:
            for u in queryset:
                for u2 in querysetusers:
                    if (u.email)==(u2.email):
                        if not u2.Administrador:
                            listquery.append(u2)
                    else:
                        pass
    paginator = Paginator(listquery, 1) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    
    context = {
        "objects_list": objects_list,
        "title": "Listado Usuarios", 
    }
    if request.user.is_superuser:
        return render(request,"user_enable_admin.html", context)
    else:
        raise PermissionDenied

#lista habilitar usuario egresado 
def user_enable_egresado(request):
    listquery=[]
    if not request.user.is_authenticated :
        raise Http404

    if request.user.Administrador:
        queryset = Registrado.objects.all()
        querysetusers = User.objects.all()
        
        if len(querysetusers) >= len(queryset):
            for u in querysetusers:
                for u2 in queryset:
                    if (u.email)==(u2.email):
                        if not u.Egresado:
                            listquery.append(u)
                    else:
                        pass
        else:
            for u in queryset:
                for u2 in querysetusers:
                    if (u.email)==(u2.email):
                        if not u2.Egresado:
                            listquery.append(u2)
                    else:
                        pass
    paginator = Paginator(listquery, 1) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    
    context = {
        "objects_list": objects_list,
        "title": "Listado Solicitudes Egresados", 
    }

    if request.user.Administrador:
        return render(request,"user_enable_egresado.html", context)
    else:
        raise PermissionDenied
    
#habiliar usuario egresado indicado 
def user_enable_detail(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404

    instance = get_object_or_404(User, id=id)

    if request.user.Administrador and not request.user.is_superuser:
        queryset = Registrado.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if querysetuser.Egresado == False:
                    Bandquery=1

    if Bandquery == 1:
        formEgresado = userEnableEgresadoForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if formEgresado.is_valid():
            instance = formEgresado.save(commit = False)
            instance.save()
            if request.user.Administrador:
                messages.success(request, "Cuenta Egresado Habilitada", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
            
        context = {        
        "instance": instance,
        "form": formEgresado,
        }

    if  Bandquery==1:    
        if request.user.Administrador:
            return render(request,"user_enable_detail.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#habiliar usuario indicado Admin
def user_enable_detail_admin(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404

    instance = get_object_or_404(User, id=id)

    if request.user.is_superuser:
        queryset = InvitacionAdmin.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if not querysetuser.Administrador:
                    Bandquery=1

    if Bandquery == 1:
        formAdmin = userEnableForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if formAdmin.is_valid():
            instance = formAdmin.save(commit = False)
            instance.save()
            if request.user.is_superuser:
                messages.success(request, "Cuenta Administrador Habilitada", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
            
        context = {        
        "instance": instance,
        "form": formAdmin,
        }

    if  Bandquery==1:    
        if request.user.is_superuser:
            return render(request,"user_enable_detail.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#modificar Egresado usuario indicado
def user_update_observatorio(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404
    #instance= Post.objects.get(id=None)
    instance = get_object_or_404(User, id=id)
    
    if request.user.Administrador and not request.user.is_superuser:
        queryset = Registrado.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if querysetuser.Egresado:
                    Bandquery=1

    if Bandquery == 1:
        form = userEgresadoUpdateForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            if request.user.Administrador and not request.user.is_superuser:
                messages.success(request, "La Informacion ha sido modificado", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
            
        context = {
        "title": "Modificar Datos Cuenta",        
        "instance": instance,
        "form": form,
        }

    if  Bandquery==1:    
        if request.user.Administrador:
            return render(request,"user_update_observatorio.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#modificar Admin usuario indicado
def user_Admin_update_observatorio(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404
    instance = get_object_or_404(User, id=id)
    
    if request.user.is_superuser:
        queryset = InvitacionAdmin.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if querysetuser.Administrador:
                    Bandquery=1
    print (Bandquery)
    if Bandquery == 1:
        form = userAdminUpdateForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            if request.user.is_superuser:
                messages.success(request, "La Informacion ha sido modificado", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
            
        context = {
        "title": "Modificar Datos Cuenta",        
        "instance": instance,
        "form": form,
        }

    if  Bandquery==1:    
        if request.user.is_superuser:
            return render(request,"user_update_observatorio.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#deshabilitar usuario administrador lista
def user_list_disable_admin(request):
	if not request.user.is_superuser :
		raise Http404
	queryset = []
	if request.user.is_superuser:
		queryset = User.objects.filter(Administrador = True)
	query = request.GET.get("q")
	if query:
		queryset=queryset.filter(
			Q(email__icontains=query)|
			Q(username__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset, 1) # Show # contacts per page.
	page_number = request.GET.get('page')
	objects_list = paginator.get_page(page_number)
	
	context = {
		"objects_list": objects_list,
		"title": "Listado Administradores", 
	}
	if request.user.is_superuser:
		return render(request,"user_list_disable_admin.html", context)
	else:
		raise PermissionDenied

#deshabilitar usuario egresado lista
def user_list_disable_egresado(request):
	if not request.user.Administrador :
		raise Http404
	queryset=[]
	if request.user.Administrador:
		queryset = User.objects.filter( Egresado=True)
	query = request.GET.get("q")
	if query:
		queryset=queryset.filter(
			Q(email__icontains=query)|
			Q(username__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset, 1) # Show # contacts per page.
	page_number = request.GET.get('page')
	objects_list = paginator.get_page(page_number)
	
	context = {
		"objects_list": objects_list,
		"title": "Listado Egresados", 
	}
	if request.user.Administrador:
		return render(request,"user_list_disable_egresado.html", context)
	else:
		raise PermissionDenied

#deshabilitar usuario Egresado indicado
def user_disable(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404
    instance = get_object_or_404(User, id=id)

    if request.user.Administrador and not request.user.is_superuser:
        queryset = Registrado.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if querysetuser.Egresado:
                    Bandquery=1

    if Bandquery == 1:
        form = userDisableEgresadoForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            if request.user.Administrador and not request.user.is_superuser:
                messages.success(request, "Cuenta Egresado Deshabilitada", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
            
        context = {        
        "instance": instance,
        "form": form,
        }

    if  Bandquery==1:    
        if request.user.Administrador:
            return render(request,"user_disable.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#deshabilitar usuario administrador indicado
def user_admin_disable(request, id=None):
    Bandquery=0
    if not request.user.is_authenticated :
        raise Http404
    instance = get_object_or_404(User, id=id)

    if request.user.is_superuser:
        queryset = InvitacionAdmin.objects.all()
        querysetuser = instance

        for u in queryset:
            if (u.email)==(querysetuser.email):
                if querysetuser.Administrador:
                    Bandquery=1

    if Bandquery == 1:
        form = userDisableForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            if request.user.is_superuser:
                messages.success(request, "Cuenta Administrador Deshabilitada", extra_tags="html_safe")               
            return HttpResponseRedirect(instance.get_absolute_url())
       
        context = {        
        "instance": instance,
        "form": form,
        }

    if  Bandquery==1:    
        if request.user.is_superuser:
            return render(request,"user_disable.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

#modificar perfil 
def user_update(request):
    #modificar datos propia cuenta
    if not request.user.is_authenticated :
        raise Http404
    #instance= Post.objects.get(id=None)
    instance = get_object_or_404(User, id=request.user.id)
    
    if request.user.Egresado:
        form = userEgresadoForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
    if request.user.Administrador or request.user.is_superuser:       
        form = userForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
    
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "Tus datos han sido modificados", extra_tags="html_safe")                
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {        
        "title": "Editar Perfil",
        "instance": instance,
        "form": form,
    }

    return render(request,"user_update.html", context)

#modificar Intereses perfil  Egresado
def user_update_Interes(request):
    #modificar datos propia cuenta
    if not request.user.is_authenticated :
        raise Http404
    #instance= Post.objects.get(id=None)
    instance = get_object_or_404(User, id=request.user.id)
    
    if request.user.Egresado:
        form = userAgregarInteresForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
    
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "Tus Intereses han sido modificados", extra_tags="html_safe")                
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {        
        "title": "Agregar o Eliminar Interes",
        "instance": instance,
        "form": form,
    }
    if request.user.Egresado:
        return render(request,"user_update.html", context)
    else:
        raise PermissionDenied
    
#modificar usuario lista
def user_list_update(request):
	if request.user.Egresado :
		raise Http404
	titulo = "Listado"
	if request.user.is_superuser:
		queryset = User.objects.filter(Administrador = True)
		titulo = "Listado Administradores"
	if request.user.Administrador and not request.user.is_superuser:
		queryset = User.objects.filter( Egresado=True)
		titulo = "Listado Egresados"
	
	query = request.GET.get("q")
	if query:
		queryset=queryset.filter(
			Q(email__icontains=query)|
			Q(username__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset, 1) # Show # contacts per page.
	page_number = request.GET.get('page')
	objects_list = paginator.get_page(page_number)
	
	context = {
		"objects_list": objects_list,
		"title": titulo, 
	}
	if request.user.Administrador or request.user.is_superuser:
		return render(request,"user_list_update.html", context)
	else:
		raise PermissionDenied
	
#buscar lista usuarios 
def user_list(request):
	if request.user.Egresado :
		raise Http404
	titulo= "listado"
	if request.user.is_superuser:
		queryset = User.objects.filter(Administrador = True)
		titulo = "Listado Administradores"
	if request.user.Administrador and not request.user.is_superuser:
		queryset = User.objects.filter(is_active = True, Egresado=True)
		titulo ="Listado Egresados"

	query = request.GET.get("q")
	if query:
		queryset=queryset.filter(
			Q(email__icontains=query)|
			Q(username__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset, 1) # Show # contacts per page.
	page_number = request.GET.get('page')
	objects_list = paginator.get_page(page_number)
	
	context = {
		"objects_list": objects_list,
		"title": titulo, 
	}
	if request.user.Administrador or request.user.is_superuser:
		return render(request,"user_list.html", context)
	else:
		raise PermissionDenied
	
#buscar lista usuarios 
def user_find_friend(request):
	if not request.user.Egresado :
		raise Http404
	titulo= "Buscar Amigos"
	if request.user.Egresado:
		queryset = User.objects.filter(Egresado = True ).exclude(username=request.user.username)

	query = request.GET.get("q")
	if query:
		queryset=queryset.filter(
			Q(email__icontains=query)|
			Q(username__icontains=query)|
			Q(dni_administrador__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset, 1) # Show # contacts per page.
	page_number = request.GET.get('page')
	objects_list = paginator.get_page(page_number)
	
	context = {
		"objects_list": objects_list,
		"title": titulo, 
	}
	return render(request,"find_friend.html", context)

#ver perfil Egresao
def user_detail_egresado(request, id):
    if not request.user.Egresado:
        raise Http404
    instance = get_object_or_404(User, id=id)
    previous_page = request.META.get('HTTP_REFERER')
    context = {        
        "instance": instance,
        "previous_page" : previous_page,
    }
    
    if request.user.Egresado:
        return render(request,"user_detail_egresado.html", context)
    else:
        raise PermissionDenied

