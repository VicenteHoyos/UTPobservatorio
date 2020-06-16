from django.urls import include, path

from posts import views

urlpatterns = [
    path('',views.post_list, name='list'),
    path('news_list_egresado',views.post_list_Egresado, name='listnewsegresado'),
    path('news_list',views.post_list_update, name='newslistupdate'),
    path('create_news/',views.post_create, name='create'),
    path('create_interes/',views.interes_create, name='createinteres'),
    path('<slug:slug>/',views.post_detail, name='detail'),
    path('edit/<int:id>',views.post_update, name="update"),
    # path('<slug:slug>/delete/',views.post_delete, name='delete'),
    path('delete/<int:id>',views.post_delete, name='delete'),

]