from django.contrib import admin
from .models import Aluno
 
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "curso", "criado_em")
    search_fields = ("nome", "curso")
    list_filter = ("curso",)
