# biblioteca/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages # Para mensagens de feedback ao usuário
# from django.contrib.auth import authenticate, login, logout # Será usado para o sistema de autenticação real do Django
from .models import Funcionario, Leitor, Livro
from .forms import FuncionarioForm, LeitorForm, LivroForm
from django.utils import timezone

# --- Views de Autenticação (Login e Logout) ---
# Usando a simulação do seu HTML por enquanto.
# O ideal é integrar com o sistema de autenticação do Django (django.contrib.auth)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Simulação de autenticação com o modelo Funcionario
        try:
            funcionario = Funcionario.objects.get(email=email)
            # AQUI: Em um sistema real, você NUNCA compararia senhas em texto puro.
            # Usaria `check_password` do Django. Isso é só para o exemplo inicial.
            if funcionario.senha == senha:
                # Simula o login mantendo o ID e nome na sessão
                request.session['funcionario_logado_id'] = funcionario.id
                request.session['funcionario_logado_nome'] = funcionario.nome
                messages.success(request, f"Bem-vindo, {funcionario.nome}!")
                return redirect('home')
            else:
                messages.error(request, "Email ou senha inválidos.")
        except Funcionario.DoesNotExist:
            messages.error(request, "Email ou senha inválidos.")
    return render(request, 'login.html')

def logout_view(request):
    # Limpa a sessão do funcionário logado
    request.session.pop('funcionario_logado_id', None)
    request.session.pop('funcionario_logado_nome', None)
    messages.info(request, "Você foi desconectado.")
    return redirect('login')

# Middleware simples para proteger as views
def funcionario_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'funcionario_logado_id' not in request.session:
            messages.warning(request, "Você precisa estar logado para acessar esta página.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# --- Views Gerais ---
@funcionario_login_required
def home_view(request):
    return render(request, 'home.html')

# --- Views para Funcionário (CRUD) ---
@funcionario_login_required
def funcionario_index(request):
    # Esta é a página principal de gestão de funcionário (funcionario.html)
    return render(request, 'funcionario/funcionario.html')

@funcionario_login_required
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário cadastrado com sucesso!")
            return redirect('funcionario_consultar') # Redireciona para a lista
        else:
            messages.error(request, "Erro ao cadastrar funcionário. Verifique os dados.")
    else:
        form = FuncionarioForm() # Formulário vazio para GET
    return render(request, 'funcionario/cadastrar_funcionario.html', {'form': form})

@funcionario_login_required
def consultar_funcionario(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionario/consultar_funcionario.html', {'funcionarios': funcionarios})

@funcionario_login_required
def atualizar_funcionario(request, pk): # 'pk' para Primary Key do funcionário
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, "Funcionário atualizado com sucesso!")
            return redirect('funcionario_consultar')
        else:
            messages.error(request, "Erro ao atualizar funcionário. Verifique os dados.")
    else:
        form = FuncionarioForm(instance=funcionario) # Preenche o formulário com dados existentes
    return render(request, 'funcionario/atualizar_funcionario.html', {'form': form, 'funcionario': funcionario})

@funcionario_login_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso!")
        return redirect('funcionario_consultar')
    # Se for GET, apenas exibe uma página de confirmação
    return render(request, 'funcionario/excluir_funcionario.html', {'funcionario': funcionario})

# --- Views para Leitor (CRUD) ---
@funcionario_login_required
def leitor_index(request):
    # Esta é a página principal de gestão de leitor (leitor.html)
    return render(request, 'leitor/leitor.html')

@funcionario_login_required
def cadastrar_leitor(request):
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leitor cadastrado com sucesso!")
            return redirect('leitor_consultar') # Redireciona para a lista
        else:
            messages.error(request, "Erro ao cadastrar leitor. Verifique os dados.")
    else:
        form = LeitorForm() # Formulário vazio para GET
    return render(request, 'leitor/cadastrar_leitor.html', {'form': form})

@funcionario_login_required
def consultar_leitor(request):
    leitores = Leitor.objects.all()
    return render(request, 'leitor/consultar_leitor.html', {'leitores': leitores})

@funcionario_login_required
def atualizar_leitor(request, pk): # 'pk' para Primary Key do leitor
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        if form.is_valid():
            form.save()
            messages.success(request, "Leitor atualizado com sucesso!")
            return redirect('leitor_consultar')
        else:
            messages.error(request, "Erro ao atualizar leitor. Verifique os dados.")
    else:
        form = LeitorForm(instance=leitor) # Preenche o formulário com dados existentes
    return render(request, 'leitor/atualizar_leitor.html', {'form': form, 'leitor': leitor})

@funcionario_login_required
def excluir_leitor(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.delete()
        messages.success(request, "Leitor excluído com sucesso!")
        return redirect('leitor_consultar')
    # Se for GET, apenas exibe uma página de confirmação
    return render(request, 'leitor/excluir_leitor.html', {'leitor': leitor})


# --- Views para Livro (CRUD) ---
@funcionario_login_required
def livro_index(request):
    # Página principal de gestão de livros (livro.html)
    return render(request, 'livro/livro.html')

@funcionario_login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect('livro_consultar') # Redireciona para a lista
        else:
            messages.error(request, "Erro ao cadastrar livro. Verifique os dados.")
    else:
        form = LivroForm() # Formulário vazio para GET
    return render(request, 'livro/cadastrar_livro.html', {'form': form})

@funcionario_login_required
def consultar_livro(request):
    query = request.GET.get('q') # Pega o parâmetro de busca 'q' da URL
    livros = Livro.objects.all()

    if query:
        # Filtra por nome (icontains) ou ISBN (icontains)
        livros = livros.filter(Q(nome__icontains=query) | Q(isbn__icontains=query))
        if not livros.exists():
            messages.info(request, f"Nenhum livro encontrado para a busca: '{query}'.")
    
    return render(request, 'livro/consultar_livro.html', {'livros': livros, 'query': query})

@funcionario_login_required
def atualizar_livro(request, pk): # 'pk' para Primary Key do livro
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('livro_consultar')
        else:
            messages.error(request, "Erro ao atualizar livro. Verifique os dados.")
    else:
        form = LivroForm(instance=livro) # Preenche o formulário com dados existentes
    return render(request, 'livro/atualizar_livro.html', {'form': form, 'livro': livro})

@funcionario_login_required
def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, "Livro excluído com sucesso!")
        return redirect('livro_consultar')
    # Se for GET, apenas exibe uma página de confirmação
    return render(request, 'livro/excluir_livro.html', {'livro': livro})


# --- Views para Livro (CRUD - Manterá o foco na OBRA/TÍTULO) ---
@funcionario_login_required
def livro_index(request):
    return render(request, 'livro/livro.html')

@funcionario_login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro (obra) cadastrado com sucesso!")
            return redirect('livro_consultar')
        else:
            messages.error(request, "Erro ao cadastrar livro. Verifique os dados.")
    else:
        form = LivroForm()
    return render(request, 'livro/cadastrar_livro.html', {'form': form})

@funcionario_login_required
def consultar_livro(request):
    query = request.GET.get('q')
    livros = Livro.objects.all()

    if query:
        livros = livros.filter(Q(nome__icontains=query) | Q(isbn__icontains=query))
        if not livros.exists():
            messages.info(request, f"Nenhum livro (obra) encontrado para a busca: '{query}'.")
    
    return render(request, 'livro/consultar_livro.html', {'livros': livros, 'query': query})

@funcionario_login_required
def atualizar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro (obra) atualizado com sucesso!")
            return redirect('livro_consultar')
        else:
            messages.error(request, "Erro ao atualizar livro. Verifique os dados.")
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livro/atualizar_livro.html', {'form': form, 'livro': livro})

@funcionario_login_required
def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, "Livro (obra) excluído com sucesso!")
        return redirect('livro_consultar')
    return render(request, 'livro/excluir_livro.html', {'livro': livro})

