from datetime import date, datetime, timedelta

from django.conf import settings
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import NoReverseMatch, reverse
from .models import Aluno, Nota


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


# ===========================================================================
# DASHBOARD ACADÊMICO
# ===========================================================================
# ---------------------------------------------------------------------------
# Regras de exibição (o model Nota não define escala nem média mínima)
# ---------------------------------------------------------------------------
NOTA_MAXIMA = 10        # escala usada para preencher as barras
NOTA_MINIMA = 6         # abaixo disso a barra recebe destaque de atenção

DIAS_CURTOS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
DIAS_LONGOS = [
    "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo",
]

# tipo do evento -> (rótulo, ícone). Tipo desconhecido usa o padrão "outro".
TIPOS_EVENTO = {
    "prova": ("Prova", "📚"),
    "trabalho": ("Trabalho", "💻"),
    "entrega": ("Entrega", "💻"),
    "apresentacao": ("Apresentação", "🎤"),
    "seminario": ("Seminário", "🎓"),
    "aula_especial": ("Aula especial", "🧑‍🏫"),
    "evento": ("Evento acadêmico", "🏛️"),
    "outro": ("", "📌"),
}

# ---------------------------------------------------------------------------
# Acesso rápido
# As URLs dos portais da FEPI não constam no projeto: defina-as em settings.py
# (FEPI_PORTAL_ALUNO_URL e FEPI_ENSINO_DIGITAL_URL). Até lá, o atalho aponta
# para o site institucional.
# ---------------------------------------------------------------------------

def _grupos_acesso_rapido():
    return [
        {
            "titulo": "Microsoft 365",
            "itens": [
                {"nome": "Word", "sigla": "W", "cor": "word",
                 "url": "https://www.office.com/launch/word"},
                {"nome": "Excel", "sigla": "X", "cor": "excel",
                 "url": "https://www.office.com/launch/excel"},
                {"nome": "PowerPoint", "sigla": "P", "cor": "powerpoint",
                 "url": "https://www.office.com/launch/powerpoint"},
                {"nome": "Teams", "sigla": "T", "cor": "teams",
                 "url": "https://teams.microsoft.com"},
            ],
        },
        {
            "titulo": "Portais acadêmicos",
            "itens": [
                {"nome": "Portal do Aluno FEPI", "icone": "portal", "cor": "fepi",
                 "url": getattr(settings, "FEPI_PORTAL_ALUNO_URL")},
                {"nome": "Ensino Digital FEPI", "icone": "digital", "cor": "fepi",
                 "url": getattr(settings, "FEPI_ENSINO_DIGITAL_URL")},
            ],
        },
    ]


# ---------------------------------------------------------------------------
# Eventos (ainda sem fonte de dados)
# ---------------------------------------------------------------------------
def _buscar_eventos(aluno, inicio, fim):
    """
    PONTO DE INTEGRAÇÃO para os eventos acadêmicos.

    Os models atuais não têm campos de data/horário de avaliações nem um model
    de evento, então esta função devolve lista vazia (nenhum dado fictício).

    Quando houver uma fonte de dados, basta devolver, para o período
    [inicio, fim], uma lista de dicts neste formato:

        {
            "data": date(2026, 9, 22),      # obrigatório
            "titulo": "Prova de Banco de Dados",  # obrigatório
            "horario": time(19, 0),         # opcional (datetime.time ou None)
            "tipo": "prova",                # opcional; chaves de TIPOS_EVENTO
        }
    """
    return []


def _formatar_horario(horario):
    if not horario:
        return ""
    return f"{horario.hour}h" if horario.minute == 0 else f"{horario.hour}h{horario.minute:02d}"


def _montar_semana(aluno, hoje):
    # Fim de semana: mostra a semana seguinte, que é a que interessa ao aluno.
    if hoje.weekday() >= 5:
        inicio = hoje + timedelta(days=7 - hoje.weekday())
    else:
        inicio = hoje - timedelta(days=hoje.weekday())
    fim = inicio + timedelta(days=6)

    por_dia = {}
    for ev in _buscar_eventos(aluno, inicio, fim):
        rotulo, icone = TIPOS_EVENTO.get(ev.get("tipo") or "outro", TIPOS_EVENTO["outro"])
        por_dia.setdefault(ev["data"], []).append({
            "titulo": ev["titulo"],
            "horario": _formatar_horario(ev.get("horario")),
            "tipo": rotulo,
            "icone": icone,
        })

    dias = []
    for i in range(7):
        dia = inicio + timedelta(days=i)
        # Sábado e domingo só aparecem quando há evento.
        if i >= 5 and dia not in por_dia:
            continue
        dias.append({
            "sigla": DIAS_CURTOS[i],
            "numero": dia.day,
            "rotulo": f"{DIAS_LONGOS[i]}, {dia:%d/%m}",
            "hoje": dia == hoje,
            "eventos": por_dia.get(dia, []),
        })

    return {
        "dias": dias,
        "dias_com_evento": [d for d in dias if d["eventos"]],
        "intervalo": f"{inicio:%d/%m} a {(inicio + timedelta(days=4)):%d/%m}",
    }


# ---------------------------------------------------------------------------
# Evolução das notas (usa Nota.data_lancamento, dado real do banco)
# ---------------------------------------------------------------------------
def _nota_br(valor):
    return f"{valor:.1f}".replace(".", ",")


def _evolucao(notas_qs, limite=12):
    """Monta as coordenadas do gráfico SVG (viewBox 300x120) com as últimas notas."""
    ultimas = list(notas_qs.select_related("materia").order_by("-data_lancamento")[:limite])[::-1]
    if not ultimas:
        return None

    largura, altura, margem = 300, 120, 10

    def y_da_nota(v):
        v = max(0.0, min(float(v), NOTA_MAXIMA))
        return altura - margem - (altura - 2 * margem) * v / NOTA_MAXIMA

    total = len(ultimas)
    pontos = []
    for i, registro in enumerate(ultimas):
        proporcao = i / (total - 1) if total > 1 else 0.5
        pontos.append({
            "x": f"{margem + (largura - 2 * margem) * proporcao:.1f}",
            "y": f"{y_da_nota(registro.nota):.1f}",
            "texto": f"{registro.materia.nome}: {_nota_br(float(registro.nota))} em {registro.data_lancamento:%d/%m}",
        })

    linha = " L ".join(f"{p['x']} {p['y']}" for p in pontos)
    base = f"{altura - margem}"
    return {
        "pontos": pontos,
        "linha": f"M {linha}",
        "area": f"M {pontos[0]['x']} {base} L {linha} L {pontos[-1]['x']} {base} Z",
        "y_minima": f"{y_da_nota(NOTA_MINIMA):.1f}",
        "x_fim": str(largura),
        "inicio": f"{ultimas[0].data_lancamento:%d/%m}",
        "fim": f"{ultimas[-1].data_lancamento:%d/%m}",
    }


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------
def _resolver_aluno(request, pk):
    """
    Com pk usa o aluno indicado. Sem pk tenta casar o e-mail do usuário logado
    (a menos que ?escolher=1 force a tela de escolha). Sem aluno: devolve None.
    """
    if pk is not None:
        return get_object_or_404(Aluno, pk=pk)
    if request.GET.get("escolher"):
        return None
    user = request.user
    if user.is_authenticated and user.email:
        return Aluno.objects.filter(email__iexact=user.email).first()
    return None


def _iniciais(nome):
    partes = nome.split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[-1][0]).upper()
    return partes[0][0].upper() if partes else "?"


SESSAO_ULTIMO_ALUNO = "ultimo_aluno_dashboard"


def _selecionar_aluno(request):
    """Tela de escolha: índice de alunos agrupado por curso, com a média de cada um."""
    curso_ativo = request.GET.get("curso", "").strip()

    todos = []
    for a in Aluno.objects.annotate(media=Avg("notas__nota")).order_by("curso", "nome"):
        media = round(float(a.media), 1) if a.media is not None else None
        todos.append({
            "pk": a.pk,
            "nome": a.nome,
            "iniciais": _iniciais(a.nome),
            "matricula": a.matricula,
            "curso": a.curso or "Sem curso",
            "semestre": a.semestre,
            "status": a.status,
            "status_label": a.get_status_display(),
            "media": media,
            "abaixo": media is not None and media < NOTA_MINIMA,
        })

    contagem = {}
    for a in todos:
        contagem[a["curso"]] = contagem.get(a["curso"], 0) + 1
    cursos = [{"curso": c, "total": t} for c, t in sorted(contagem.items())]

    visiveis = [a for a in todos if not curso_ativo or a["curso"] == curso_ativo]
    grupos = {}
    for a in visiveis:
        grupos.setdefault(a["curso"], []).append(a)

    ultimo_pk = request.session.get(SESSAO_ULTIMO_ALUNO) if hasattr(request, "session") else None
    ultimo = next((a for a in todos if a["pk"] == ultimo_pk), None)

    return render(request, "dashboard_selecionar.html", {
        "grupos": [{"curso": c, "alunos": lista} for c, lista in grupos.items()],
        "cursos": cursos if len(cursos) > 1 else [],
        "curso_ativo": curso_ativo,
        "total_alunos": len(todos),
        "ultimo": ultimo,
    })


def dashboard_aluno(request, pk=None):
    aluno = _resolver_aluno(request, pk)
    if aluno is None:
        return _selecionar_aluno(request)

    if hasattr(request, "session"):
        request.session[SESSAO_ULTIMO_ALUNO] = aluno.pk

    notas = Nota.objects.filter(aluno=aluno)

    totais = notas.aggregate(
        media=Avg("nota"),
        faltas=Sum("faltas"),
        avaliacoes=Count("id"),
        disciplinas=Count("materia", distinct=True),
    )

    por_materia = (
        notas.values("materia_id", "materia__nome")
        .annotate(media=Avg("nota"), faltas=Sum("faltas"), avaliacoes=Count("id"))
        .order_by("materia__nome")
    )

    disciplinas = []
    for linha in por_materia:
        media = float(linha["media"])
        disciplinas.append({
            "nome": linha["materia__nome"],
            "media": round(media, 1),
            "largura": max(0, min(100, round(media / NOTA_MAXIMA * 100))),
            "abaixo": media < NOTA_MINIMA,
            "avaliacoes": linha["avaliacoes"],
            "faltas": linha["faltas"] or 0,
        })

    try:
        url_calendario = reverse("calendario")
    except NoReverseMatch:
        url_calendario = None

    partes_nome = aluno.nome.split()
    media_geral = round(float(totais["media"]), 1) if totais["media"] is not None else None
    iniciais = "".join(p[0] for p in ([partes_nome[0], partes_nome[-1]] if len(partes_nome) > 1 else partes_nome[:1])).upper() or "?"

    contexto = {
        "aluno": aluno,
        "sb_aluno": aluno,
        "sb_iniciais": iniciais,
        "sb_ativo": "dashboard",
        "iniciais": iniciais,
        "media_pct": max(0, min(100, round(media_geral / NOTA_MAXIMA * 100))) if media_geral is not None else 0,
        "evolucao": _evolucao(notas),
        "primeiro_nome": partes_nome[0] if partes_nome else aluno.nome,
        "media_geral": media_geral,
        "total_disciplinas": totais["disciplinas"],
        "total_avaliacoes": totais["avaliacoes"],
        "total_faltas": totais["faltas"] or 0,
        "disciplinas": disciplinas,
        "nota_maxima": NOTA_MAXIMA,
        "nota_minima": NOTA_MINIMA,
        "semana": _montar_semana(aluno, date.today()),
        "url_calendario": url_calendario,
        "acesso_rapido": _grupos_acesso_rapido(),
    }
    return render(request, "dashboard_aluno.html", contexto)