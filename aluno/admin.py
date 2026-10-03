from django.contrib import admin
from .models import Aluno, Professor, Materia, Nota


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "curso", "semestre", "status", "criado_em")
    search_fields = ("nome", "matricula", "curso")
    list_filter = ("curso", "status", "bolsista")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "especialidade", "email", "ativo")
    search_fields = ("nome", "especialidade")
    list_filter = ("ativo",)


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "professor", "carga_horaria", "semestre")
    search_fields = ("nome", "codigo")
    list_filter = ("semestre", "professor")


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "materia", "nota", "faltas", "data_lancamento")
    search_fields = ("aluno__nome", "materia__nome")
    list_filter = ("materia", "aluno")
