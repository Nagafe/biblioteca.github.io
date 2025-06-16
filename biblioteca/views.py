from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Funcionario, Livro, Emprestimo, Leitor

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            funcionario = Funcionario.objects.get(email=email)
            if funcionario.senha == senha:  # Em produção, use hash de senha
                auth_login(request, funcionario)
                return redirect('home')
            else:
                messages.error(request, 'Senha inválida.')
        except Funcionario.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
    
    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def home(request):
    total_livros = Livro.objects.count()
    emprestimos_ativos = Emprestimo.objects.filter(status='A').count()
    total_leitores = Leitor.objects.count()
    total_funcionarios = Funcionario.objects.count()
    
    context = {
        'total_livros': total_livros,
        'emprestimos_ativos': emprestimos_ativos,
        'total_leitores': total_leitores,
        'total_funcionarios': total_funcionarios
    }
    
    return render(request, 'home.html', context)

@login_required
def funcionario(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionario/funcionario.html', {'funcionarios': funcionarios})

@login_required
def cadastrar_funcionario(request):
    if request.method == 'POST':
        funcionario = Funcionario(
            nome=request.POST['nome'],
            email=request.POST['email'],
            senha=request.POST['senha'],
            cargo=request.POST['cargo'],
            telefone=request.POST['telefone'],
            cpf=request.POST['cpf'],
            endereco=request.POST['endereco'],
            data_nascimento=request.POST['data_nascimento']
        )
        funcionario.save()
        messages.success(request, 'Funcionário cadastrado com sucesso!')
        return redirect('funcionario')
    return render(request, 'funcionario/cadastrar_funcionario.html')

@login_required
def editar_funcionario(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    
    if request.method == 'POST':
        funcionario.nome = request.POST.get('nome')
        funcionario.email = request.POST.get('email')
        funcionario.telefone = request.POST.get('telefone')
        funcionario.cpf = request.POST.get('cpf')
        funcionario.endereco = request.POST.get('endereco')
        funcionario.data_nascimento = request.POST.get('data_nascimento')
        funcionario.cargo = request.POST.get('cargo')
        funcionario.save()
        
        messages.success(request, 'Funcionário atualizado com sucesso!')
        return redirect('funcionario')
    
    return render(request, 'funcionario/editar_funcionario.html', {'funcionario': funcionario})

@login_required
def excluir_funcionario(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    
    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('funcionario')
    
    return render(request, 'funcionario/excluir_funcionario.html', {'funcionario': funcionario})

@login_required
def consultar_funcionario(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionario/consultar_funcionario.html', {'funcionarios': funcionarios})

@login_required
def livro(request):
    livros = Livro.objects.all()
    return render(request, 'livro/livro.html', {'livros': livros})

@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        genero = request.POST.get('genero')
        copias = request.POST.get('copias')
        ano = request.POST.get('ano')

        Livro.objects.create(
            titulo=titulo,
            autor=autor,
            genero=genero,
            copias=copias,
            ano=ano
        )

        messages.success(request, 'Livro cadastrado com sucesso!')
        return redirect('livro')

    return render(request, 'livro/cadastrar_livro.html')

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    
    if request.method == 'POST':
        livro.titulo = request.POST.get('titulo')
        livro.autor = request.POST.get('autor')
        livro.genero = request.POST.get('genero')
        livro.copias = request.POST.get('copias')
        livro.ano = request.POST.get('ano')
        livro.save()
        
        messages.success(request, 'Livro atualizado com sucesso!')
        return redirect('livro')
    
    return render(request, 'livro/atualizar_livro.html', {'livro': livro})

@login_required
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('livro')
    
    return render(request, 'livro/excluir_livro.html', {'livro': livro})

@login_required
def consultar_livro(request):
    livros = Livro.objects.all()
    return render(request, 'livro/consultar_livro.html', {'livros': livros})

@login_required
def relatorio_emprestimo(request):
    # Get filter parameters
    usuario = request.GET.get('usuario', '')
    data = request.GET.get('data', '')
    
    # Base queryset
    emprestimos = Emprestimo.objects.all()
    
    # Apply filters if provided
    if usuario:
        emprestimos = emprestimos.filter(leitor__nome_completo__icontains=usuario)
    if data:
        emprestimos = emprestimos.filter(data_emprestimo__date=data)
    
    # Calculate statistics
    total_emprestimos = emprestimos.count()
    total_devolucoes = emprestimos.filter(status='D').count()
    total_atrasos = emprestimos.filter(status='T').count()
    
    # Handle loan renewal
    if request.method == 'POST' and 'renovar' in request.POST:
        emprestimo_id = request.POST.get('emprestimo_id')
        emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
        
        # Check if loan can be renewed
        if emprestimo.status == 'A' and not emprestimo.renovacao:
            # Update loan data
            emprestimo.data_devolucao = timezone.now() + timedelta(days=emprestimo.numero_dias)
            emprestimo.renovacao = True
            emprestimo.save()
            
            messages.success(request, 'Empréstimo renovado com sucesso!')
        else:
            messages.error(request, 'Este empréstimo não pode ser renovado.')
        
        return redirect('relatorio_emprestimo')
    
    context = {
        'emprestimos': emprestimos,
        'total_emprestimos': total_emprestimos,
        'total_devolucoes': total_devolucoes,
        'total_atrasos': total_atrasos,
    }
    
    return render(request, 'emprestimo/relatorio.html', context)

@login_required
def leitor(request):
    leitores = Leitor.objects.all()
    return render(request, 'leitor/leitor.html', {'leitores': leitores})

@login_required
def acervo(request):
    livros = Livro.objects.all()
    return render(request, 'livro/acervo.html', {'livros': livros})

@login_required
def consulta_emprestimo(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'emprestimo/consulta.html', {'emprestimos': emprestimos})

@login_required
def cadastrar_leitor(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        cpf = request.POST['cpf']
        endereco = request.POST['endereco']
        data_nascimento = request.POST['data_nascimento']
        
        leitor = Leitor(
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf,
            endereco=endereco,
            data_nascimento=data_nascimento
        )
        leitor.save()
        messages.success(request, 'Leitor cadastrado com sucesso!')
        return redirect('consultar_leitor')
    return render(request, 'leitor/cadastrar_leitor.html')

@login_required
def editar_leitor(request, leitor_id):
    leitor = get_object_or_404(Leitor, id=leitor_id)
    if request.method == 'POST':
        leitor.nome = request.POST['nome']
        leitor.email = request.POST['email']
        leitor.telefone = request.POST['telefone']
        leitor.cpf = request.POST['cpf']
        leitor.endereco = request.POST['endereco']
        leitor.data_nascimento = request.POST['data_nascimento']
        leitor.save()
        messages.success(request, 'Leitor atualizado com sucesso!')
        return redirect('consultar_leitor')
    return render(request, 'leitor/editar_leitor.html', {'leitor': leitor})

