from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno


def _para_inteiro(valor, padrao=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def _para_data(valor):
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


def _dados_do_formulario(request):
    """Extrai e normaliza os dados enviados pelo formulário de aluno."""
    post = request.POST
    return {
        "nome": post.get("nome", "").strip(),
        "matricula": post.get("matricula", "").strip(),
        "email": post.get("email", "").strip(),
        "cpf": post.get("cpf", "").strip(),
        "curso": post.get("curso", "").strip(),
        "semestre": _para_inteiro(post.get("semestre"), padrao=1),
        "status": post.get("status", Aluno.STATUS_ATIVO),
        "bolsista": post.get("bolsista") == "on",
        "data_nascimento": _para_data(post.get("data_nascimento")),
        "bio": post.get("bio", ""),
    }


def aluno(request):
    busca = request.GET.get("q", "").strip()
    curso_filtro = request.GET.get("curso", "").strip()
    status_filtro = request.GET.get("status", "").strip()

    alunos_qs = Aluno.objects.all()

    if busca:
        alunos_qs = alunos_qs.filter(
            Q(nome__icontains=busca) | Q(matricula__icontains=busca)
        )
    if curso_filtro:
        alunos_qs = alunos_qs.filter(curso=curso_filtro)
    if status_filtro:
        alunos_qs = alunos_qs.filter(status=status_filtro)

    alunos = list(alunos_qs)

    for a in alunos:
        partes = a.nome.split()
        if len(partes) >= 2:
            a.iniciais = (partes[0][0] + partes[-1][0]).upper()
        elif partes:
            a.iniciais = partes[0][0].upper()
        else:
            a.iniciais = "?"

    cursos_disponiveis = (
        Aluno.objects.exclude(curso="")
        .order_by("curso")
        .values_list("curso", flat=True)
        .distinct()
    )

    contexto = {
        "alunos": alunos,
        "total_geral": Aluno.objects.count(),
        "cursos_disponiveis": cursos_disponiveis,
        "status_choices": Aluno.STATUS_CHOICES,
        "filtro_q": busca,
        "filtro_curso": curso_filtro,
        "filtro_status": status_filtro,
        "filtros_ativos": bool(busca or curso_filtro or status_filtro),
    }
    return render(request, "aluno.html", contexto)


def criar_aluno(request):
    if request.method == "POST":
        Aluno.objects.create(**_dados_do_formulario(request))
        return redirect("listar_alunos")
    return render(
        request,
        "aluno/form_aluno.html",
        {"titulo": "Novo Aluno", "status_choices": Aluno.STATUS_CHOICES},
    )


def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)

    if request.method == "POST":
        dados = _dados_do_formulario(request)
        for campo, valor in dados.items():
            setattr(aluno, campo, valor)
        aluno.save()
        return redirect("listar_alunos")

    return render(
        request,
        "aluno/form_aluno.html",
        {
            "aluno": aluno,
            "titulo": f"Editar: {aluno.nome}",
            "status_choices": Aluno.STATUS_CHOICES,
        },
    )


def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        aluno.delete()
        return redirect("listar_alunos")
    return render(request, "aluno/confirmar_exclusao.html", {"aluno": aluno})