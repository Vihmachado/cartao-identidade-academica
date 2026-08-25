from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.aluno,name='aluno'),
    path("admin/", admin.site.urls),
]

