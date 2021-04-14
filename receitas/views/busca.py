from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from receitas.models import Receita


def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_postagem').filter(publicado=True)
    if 'buscar' in request.GET:
        nome_busca = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_busca)

    dados = {
        'receitas': lista_receitas

    }
    return render(request, 'buscar.html', dados)
