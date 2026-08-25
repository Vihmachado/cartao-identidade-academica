from django.shortcuts import render
from .models import Aluno
 
 
def aluno(request):
    alunos = list(Aluno.objects.all())
 
    for a in alunos:
        partes = a.nome.split()
        if len(partes) >= 2:
            a.iniciais = (partes[0][0] + partes[-1][0]).upper()
        elif partes:
            a.iniciais = partes[0][0].upper()
        else:
            a.iniciais = "?"
 
    return render(request, "aluno.html", {"alunos": alunos})