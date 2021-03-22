from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from receitas.models import Receita


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if not nome.strip() or not email.strip:
            print('digite um valor válido')
            return redirect('cadastro')

        if senha != senha2:
            print('As senha não batem!')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            print('usuário já cadastrado!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        return redirect('login')
    else:
        return render(request, 'cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        if email.strip() == '' or senha.strip() == '':
            print('dados inválidos')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso!')
                return redirect('dashboard')

    return render(request, 'login.html')


def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_postagem').filter(
            pessoa=request.user.id
        )
        dados = {
            'receitas': receitas
        }
        return render(request, 'dashboard.html', dados)

    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')


def cria_receita(request):
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
            print('passei aqui????')
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