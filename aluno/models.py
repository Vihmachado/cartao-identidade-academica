from django.db import models
from django.utils import timezone


class Aluno(models.Model):
    STATUS_ATIVO = "ativo"
    STATUS_TRANCADO = "trancado"
    STATUS_FORMADO = "formado"

    STATUS_CHOICES = [
        (STATUS_ATIVO, "Ativo"),
        (STATUS_TRANCADO, "Trancado"),
        (STATUS_FORMADO, "Formado"),
    ]

    # --- Identificação ---------------------------------------------------
    nome = models.CharField("Nome", max_length=150)
    matricula = models.CharField("Matrícula", max_length=20, blank=True, default="")
    email = models.CharField("E-mail", max_length=150, blank=True, default="")
    cpf = models.CharField("CPF", max_length=14, blank=True, default="")

    # --- Dados acadêmicos --------------------------------------------------
    curso = models.CharField("Curso", max_length=150)
    semestre = models.IntegerField("Semestre", default=1)
    status = models.CharField(
        "Status", max_length=10, choices=STATUS_CHOICES, default=STATUS_ATIVO
    )
    bolsista = models.BooleanField("Bolsista", default=False)

    # --- Dados pessoais / complementares ------------------------------------
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    bio = models.TextField("Bio", blank=True)

    # --- Controle -----------------------------------------------------------
    criado_em = models.DateTimeField("Cadastrado em", default=timezone.now)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome