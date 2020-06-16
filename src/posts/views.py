from urllib.parse import quote_plus
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.utils import timezone
from functools import reduce
import operator
from operator import and_
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

from .forms import PostForm ,PostUpdateForm, InteresForm
from .models import Post, Interes #importo mi modelo

from users.models import User
def post_create(request):
    if not request.user.Administrador :
        print("Bienvenido %s" %(request.user))
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit = False)
        # print( form.cleaned_data.get("categorias"))

        interesesPost =list(form.cleaned_data.get("categorias"))
        # print (interesesPost)
        listIntereses = []
        for i in interesesPost:
            listIntereses.append(i)

        # print(len(listIntereses))

        usuarios = User.objects.filter(Egresado = True)

        Correos = []
        for us in usuarios:
            for i in us.categorias.all():
                # intereses.append(i.nombre)
                for j in listIntereses:
                    # print(i,j)
                    if i == j:
                        Correos.append(us.email)
        
        CorreosUsers = []
        for i in  Correos:
            if i not in CorreosUsers:
                CorreosUsers.append(i)
        print(CorreosUsers)

        asunto = 'Nuevo post en Observatorio Egresados'
        link ='http://localhost:8000/posts/news_list_egresado'
        email_from = settings.EMAIL_HOST_USER
        email_to = CorreosUsers
        email_mensaje = "Hola Egresado: Hay un nuevo post en Observatorio Egresados que te interesa, ingresa al link %s para que puedas ver. Enviado por %s.  " %(link,email_from)
        send_mail(asunto, 
            email_mensaje,
            email_from,
            email_to,
            fail_silently=False
            )

        instance.user = request.user
        instance.save()
        # messages.success(request, "tu Noticia ha sido creado con exito")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {        
        "form": form,
    }
    if request.user.Administrador:
        return render(request,"post_form.html", context)
    else:
        raise PermissionDenied

def interes_create(request):
    if not request.user.Administrador :
        raise Http404

    form = InteresForm(request.POST or None, request.FILES or None)
    #if request.method == "POST":
    #print (request.POST.get("titulo"))
    if form.is_valid():
        instance = form.save(commit = False)
        #print( form.cleaned_data.get("titulo"))
        instance.user = request.user
        instance.save()
        messages.success(request, "Interes creado con exito")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {        
        "form": form,
    }
    if request.user.Administrador:
        return render(request,"interes_form.html", context)
    else:
        raise PermissionDenied

def post_detail(request, slug=None):
    #instance= Post.objects.get(id=None)
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.Administrador:
            raise Http404    
    share_string = quote_plus(instance.titulo)
    context = {        
        "title": instance.titulo,
        "instance": instance,
        "share_string":share_string,
    }
    if request.user.Administrador or request.user.Egresado:
        return render(request,"post_detail.html", context)
    else:
        raise PermissionDenied
    
def post_list(request):
    if not request.user.Administrador :
        raise Http404
    hoy = timezone.now().date()
    queryset = Post.objects.active()#filter(draft=False).filter(publish__lte= timezone.now())#all(),order_by("-timestamp")
    if request.user.Administrador and not request.user.is_superuser:
        queryset = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset=queryset.filter(
            Q(titulo__icontains=query)|
            Q(categorias__nombre__icontains=query)|
            Q(contenido__icontains=query)|
            Q(user__first_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    
    context = {
        "objects_list": objects_list,
        "title": "Listado Noticias", 
        "hoy": hoy,        
    }

    if request.user.Administrador:
        return render(request,"post_list.html", context)
    else:
        raise PermissionDenied

def post_list_Egresado(request):
    if not request.user.Egresado :
        raise Http404
    intereses =[]
    if request.user.Egresado:
        for i in request.user.categorias.all():
            intereses.append(i.nombre)

    hoy = timezone.now().date()
    queryset = Post.objects.active()#filter(publish__lte= hoy).filter(draft=False).filter(publish__lte= timezone.now())#all(),order_by("-timestamp")
    if request.user.Egresado and not request.user.Administrador and not request.user.is_superuser:
        q = Q()
        for i in intereses:
            q |= Q(categorias__nombre__icontains = i)
        
    queryset = Post.objects.filter(q).filter(publish__lte= timezone.now()).distinct()
    query = request.GET.get("q")

    if query:
        queryset=queryset.filter(
            Q(titulo__icontains=query)|
            Q(categorias__nombre__icontains=query)|
            Q(contenido__icontains=query)|
            Q(user__first_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    
    context = {
        "objects_list": objects_list,
        "title": "Listado Noticias Egresado", 
        "hoy": hoy,        
    }

    if request.user.Egresado:
        return render(request,"post_list.html", context)
    else:
        raise PermissionDenied

def post_list_update(request):
    hoy = timezone.now().date()
    queryset = Post.objects.active()#filter(draft=False).filter(publish__lte= timezone.now())#all(),order_by("-timestamp")
    if request.user.Administrador and not request.user.is_superuser:
        queryset = Post.objects.filter(user=request.user)
    query = request.GET.get("q")
    if query:
        queryset=queryset.filter(
            Q(titulo__icontains=query)|
            Q(categorias__nombre__icontains=query)|
            Q(contenido__icontains=query)|
            Q(user__first_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset, 2) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    
    context = {
        "objects_list": objects_list,
        "title": "Listado Noticias", 
        "hoy": hoy,        
    }

    if request.user.Administrador:
        return render(request,"post_list_update.html", context)
    else:
        raise PermissionDenied

def post_update(request, id= None):
    Bandequery= 0
    if not request.user.Administrador :
        raise Http404
    instance = get_object_or_404(Post, id=id) 

    if request.user == instance.user:
        Bandequery= 1

    if Bandequery== 1:
        form = PostUpdateForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            # messages.success(request, "Tu Noticia ha sido modificada", extra_tags="html_safe")                
            return HttpResponseRedirect(instance.get_absolute_url())    

        context = {        
            "title": instance.titulo,
            "instance": instance,
            "form": form,
        }

    if Bandequery== 1:
        if request.user.Administrador:
            return render(request,"post_form_update.html", context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

def post_delete(request, id=None):
    Bandequery= 0
    if not request.user.Administrador:
        raise Http404
    instance = get_object_or_404(Post, id=id)

    if request.user == instance.user:
        Bandequery= 1

    if Bandequery== 1:
        instance.delete()
        # messages.success(request, "tu post ha sido Eliminado")

    if Bandequery== 1:
        if request.user.Administrador:
            return redirect("posts:list")
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied
    
# def post_update(request, slug= None):
#     if not request.user.Administrador :
#         raise Http404
#     instance = get_object_or_404(Post, slug=slug) 

#     form = PostForm(request.POST or None, request.FILES or None, instance= instance)# edit el form
#     if form.is_valid():
#         instance = form.save(commit = False)
#         instance.save()
#         messages.success(request, "tu <a href='#'> post </a> ha sido modificado", extra_tags="html_safe")                
#         return HttpResponseRedirect(instance.get_absolute_url())    

#     context = {        
#         "title": instance.titulo,
#         "instance": instance,
#         "form": form,
#     }
#     if request.user.Administrador:
#         return render(request,"post_form.html", context)
#     else:
#         raise PermissionDenied
