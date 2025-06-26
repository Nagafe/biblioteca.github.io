# biblioteca/forms.py
from django import forms
from .models import Funcionario, Leitor, Livro

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'senha', 'telefone', 'cpf', 'endereco', 'data_nascimento']
        widgets = {
            'senha': forms.PasswordInput(), # Para o campo de senha
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ['nome', 'cpf', 'email', 'telefone', 'endereco', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['nome', 'isbn', 'autor', 'genero', 'data_publicacao']
        widgets = {
            'data_publicacao': forms.DateInput(attrs={'type': 'date'}),
        }

