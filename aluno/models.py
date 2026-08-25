from django.db import models
from django.utils import timezone
 
 
class Aluno(models.Model):
    nome = models.CharField("Nome", max_length=150)
    curso = models.CharField("Curso", max_length=150)
    bio = models.TextField("Bio", blank=True)
    criado_em = models.DateTimeField("Cadastrado em", default=timezone.now)
 
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["-criado_em"]
 
    def __str__(self):
        return self.nome