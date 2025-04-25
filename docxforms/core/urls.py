from django.urls import path
from core import views

app_name='core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('edit/', views.editar_docx, name='editar')
]