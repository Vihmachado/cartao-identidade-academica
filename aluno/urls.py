from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('', login_required(views.aluno), name='listar_alunos'),
    path('novo/', login_required(views.criar_aluno), name='criar_aluno'),
    path('<int:pk>/editar/', login_required(views.editar_aluno), name='editar_aluno'),
    path(
        '<int:pk>/excluir/',
        login_required(views.excluir_aluno),
        name='excluir_aluno',
    ),
    path('dashboard/', login_required(views.dashboard_aluno), name='dashboard_aluno'),
    path(
        '<int:pk>/dashboard/',
        login_required(views.dashboard_aluno),
        name='dashboard_aluno_pk',
    ),
]