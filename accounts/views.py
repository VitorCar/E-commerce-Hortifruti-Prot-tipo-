from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import EnderecoForm
from .models import Endereco



def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lista_produtos')

    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('lista_produtos') # Corrigido para evitar loop infinito

    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('carrinho') 
    else:
        login_form = AuthenticationForm()
        
    # Em caso de GET ou POST inválido, renderiza o template com o formulário
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):   # Sair do login do usuario
    logout(request)
    return redirect('lista_produtos')


def listar_enderecos(request):
    usuario_logado = request.user
    
    enderecos_do_usuario = []
    if usuario_logado.is_authenticated:
        # Acessamos os endereços usando o 'related_name' definido no modelo
        enderecos_do_usuario = usuario_logado.enderecos.all()

    return render(request, 'lista_enderecos.html', {'enderecos': enderecos_do_usuario})

@login_required
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            return redirect('lista_de_enderecos') # Redirecione para a página que lista os endereços
    else:
        # Se for uma requisição GET, mostra um formulário vazio
        form = EnderecoForm()

    return render(request, 'adicionar_endereco.html', {'form': form})


@login_required
def editar_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id, usuario=request.user)
    if request.method == 'POST':
        # Instancia o formulário com os dados POST e a instância do endereço a ser editado
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            return redirect('lista_de_enderecos')
    else:
        # Se for um GET, preenche o formulário com os dados do endereço
        form = EnderecoForm(instance=endereco)

    return render(request, 'editar_endereco.html', {'form': form})

@login_required
def remover_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id, usuario=request.user)
    # Remove o endereço do banco de dados
    endereco.delete()
    
    return redirect('lista_de_enderecos')