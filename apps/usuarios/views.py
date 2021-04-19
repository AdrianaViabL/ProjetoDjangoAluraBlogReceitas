from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome) or campo_vazio(email):
            messages.error(request, 'digite um valor válido!')
            return redirect('cadastro')

        if senha != senha2:
            messages.error(request, 'As senhas não batem!')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já cadastrado!')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'email de usuário já cadastrado!')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem estar vazios')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
        else:
            messages.error(request, 'usuário não cadastrado')
            return redirect('login')
    return render(request, 'login.html')


def dashboard(request):
    """busca as receitas e as retorna para o usuário cadastrado"""
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


def campo_vazio(campo):
    return not campo.strip()

