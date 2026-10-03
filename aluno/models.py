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

    nome = models.CharField("Nome", max_length=150)
    matricula = models.CharField("Matrícula", max_length=20, blank=True, default="")
    email = models.EmailField("E-mail", blank=True, default="")
    cpf = models.CharField("CPF", max_length=14, blank=True, default="")
    curso = models.CharField("Curso", max_length=150)
    semestre = models.IntegerField("Semestre", default=1)
    status = models.CharField(
        "Status", max_length=10, choices=STATUS_CHOICES, default=STATUS_ATIVO
    )
    bolsista = models.BooleanField("Bolsista", default=False)
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    bio = models.TextField("Bio", blank=True)
    criado_em = models.DateTimeField("Cadastrado em", default=timezone.now)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome


class Professor(models.Model):
    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("E-mail")
    especialidade = models.CharField("Especialidade", max_length=100)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Materia(models.Model):
    nome = models.CharField("Nome da matéria", max_length=150)
    codigo = models.CharField("Código", max_length=20, unique=True)
    carga_horaria = models.IntegerField("Carga horária")
    semestre = models.IntegerField("Semestre", default=1)
    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materias",
    )
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Matéria"
        verbose_name_plural = "Matérias"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

Disciplina = Materia


class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="notas")
    nota = models.DecimalField("Nota", max_digits=4, decimal_places=2)
    faltas = models.IntegerField("Faltas", default=0)
    data_lancamento = models.DateTimeField("Data de lançamento", default=timezone.now)

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ["-data_lancamento"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.materia.nome}: {self.nota}"
