from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.aluno, name='listar_alunos'),
    path('novo/', views.criar_aluno, name='criar_aluno'),
    path('<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<int:pk>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('admin/', admin.site.urls),
]