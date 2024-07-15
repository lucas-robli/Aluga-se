from django.urls import path 
from myapp import views
from usuarios import views as usuario_views
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.conf.urls import handler404

def custom_page_not_found_view(request, exception):
    print(request, "aaaaa")
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found_view
 
urlpatterns = [
    path('', views.list_location, name='list-location'),
    path('form-client/', views.form_client, name='client-create'),
    path('form-immobile/', views.form_immobile, name='immobile-create'),
    path('form-immobile/<int:id>/', views.update_immobile, name='immobile-edit'),
    path('form-location/<int:id>/', views.form_location, name='location-create'),
    path('reports/', views.reports, name='reports'),
    #Rotas de Usuario
    path('conta/', usuario_views.novo_usuario, name='novo_usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout')
    
]