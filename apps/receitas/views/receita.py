from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from receitas.models import Receita #mostra como erro mas está funcionando
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    """busca e exibe na pagina principal as receitas publicadas"""
    receitas = Receita.objects.order_by('-data_postagem').filter(publicado=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)
    dados = {
        'receitas': receitas_por_pagina
    }
    return render(request, 'index.html', dados)


def receitas(request, receita_id):
    """busca a receita clicada pelo id e mostra a receita completa"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_exibir = {
        'receita': receita
    }
    return render(request, 'receita.html', receita_exibir)


def cria_receita(request):
    """Cria uma nova receita"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_receita = request.POST['nome_receita']
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto_receita = request.FILES['foto_receita']#por se tratar de um dado do tipo file
            user = get_object_or_404(User, pk=request.user.id)

            if campo_vazio(nome_receita):
                messages.error(request, 'Nome da receita é obrigatório')
                return redirect('cria_receita')

            if campo_vazio(ingredientes):
                messages.error(request, 'ingredientes são obrigatórios')
                return redirect('cria_receita')

            if campo_vazio(modo_preparo):
                messages.error(request, 'Modo de preparo é obrigatório')
                return redirect('cria_receita')

            if campo_vazio(tempo_preparo):
                messages.error(request, 'tempo de preparo é obrigatório')
                return redirect('cria_receita')

            if campo_vazio(rendimento):
                messages.error(request, 'rendimento é obrigatórios')
                return redirect('cria_receita')

            if campo_vazio(categoria):
                messages.error(request, 'categoria é obrigatório')
                return redirect('cria_receita')

            receita = Receita.objects.create(
                pessoa=user,
                nome_receita=nome_receita,
                ingredientes=ingredientes,
                modo_preparo=modo_preparo,
                tempo_preparo=tempo_preparo,
                rendimento=rendimento,
                categoria=categoria,
                publicado=False,
                foto_receita=foto_receita
            )
            receita.save()
            return redirect('dashboard')
        else:
            return render(request, 'cria_receita.html')
    else:
        return redirect('index')


def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_editar = { 'receita': receita }
    return render(request, 'editar_receita.html', receita_editar)


def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()

    return redirect('dashboard')


def campo_vazio(campo):
    return not campo.strip()
