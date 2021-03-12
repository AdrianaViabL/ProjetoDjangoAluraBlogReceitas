from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Receita


def index(request):
    receitas = Receita.objects.order_by('-data_postagem').filter(publicado=True)

    dados = {
        'receitas': receitas
    }
    return render(request, 'index.html', dados)


def receitas(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_exibir = {
        'receita': receita
    }
    return render(request, 'receita.html', receita_exibir)


def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_postagem').filter(publicado=True)
    if 'buscar' in request.GET:
        nome_busca = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_busca)

    dados = {
        'receitas' : lista_receitas

    }
    return render(request, 'buscar.html', dados)