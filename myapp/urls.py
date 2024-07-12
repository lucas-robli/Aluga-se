from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.list_location, name='list-location'),
    path('form-client/', views.form_client, name='client-create'),
    path('form-immobile/', views.form_immobile, name='immobile-create'),
    path('form-immobile/<int:id>', views.edit_immobile, name='immobile-edit'),
    path('form-location/<int:id>/', views.form_location, name='location-create'),
    path('reports/', views.reports, name='reports')
]