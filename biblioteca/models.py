from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Funcionario(models.Model):
    nome = models.CharField(max_length=100, default='Funcionário')
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    cargo = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField(default=timezone.now)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Leitor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True, default='000.000.000-00')
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField(default=timezone.now)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13, unique=True)
    copias = models.IntegerField(default=1)
    ano = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Emprestimo(models.Model):
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField()
    numero_dias = models.IntegerField(default=7)
    renovado = models.BooleanField(default=False)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.leitor.nome} - {self.livro.titulo}"

    def save(self, *args, **kwargs):
        if not self.data_devolucao:
            self.data_devolucao = timezone.now() + timezone.timedelta(days=self.numero_dias)
        super().save(*args, **kwargs) 