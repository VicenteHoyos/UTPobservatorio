from django.urls import include, path

from users import views

urlpatterns = [
    path('list_user',views.user_list, name='userlist'),     
    path('detail_user',views.user_detail, name='userdetail'),
    path('detail_user_egresado/<int:id>',views.user_detail_egresado, name='userdetailegresado'),      
    path('find_friend',views.user_find_friend, name='userfindfriend'),     
    path('update_user',views.user_update, name='userupdate'),     
    path('update_interes',views.user_update_Interes, name='userupdateinteres'),     
    path('enable_admin_user',views.user_enable_admin, name='userenableadmin'),     
    path('<int:id>',views.user_enable_detail, name='userenabledetail'),     
    path('admin/<int:id>',views.user_enable_detail_admin, name='userenabledetailadmin'),     
    path('update_user_list',views.user_list_update, name='userlistupdate'),     
    path('update_user_observatorio/<int:id>',views.user_update_observatorio, name='userupdateobservatorio'), 
    path('update_user_observatorio/admin/<int:id>',views.user_Admin_update_observatorio, name='useradminupdateobservatorio'), 
    path('user_list_disable_admin',views.user_list_disable_admin, name='userlistdisableadmin'),     
    path('user_list_disable_egresado',views.user_list_disable_egresado, name='userlistdisableegresado'),     
    path('disable_user/<int:id>',views.user_disable, name='userdisable'),    
    path('disable_user/admin/<int:id>',views.user_admin_disable, name='useradmindisable'),    
    path('enable_egresado_user',views.user_enable_egresado, name='userenableegresado'),
]
