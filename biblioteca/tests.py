from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Usuario, Funcionario, Livro, Acervo, Emprestimo

class UsuarioModelTest(TestCase):
    def test_create_usuario(self):
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_completo='Test User'
        )
        self.assertEqual(usuario.email, 'test@example.com')
        self.assertEqual(usuario.nome_completo, 'Test User')

class FuncionarioModelTest(TestCase):
    def test_create_funcionario(self):
        usuario = Usuario.objects.create_user(
            username='testfunc',
            email='func@example.com',
            password='testpass123',
            nome_completo='Test Func'
        )
        funcionario = Funcionario.objects.create(
            usuario=usuario,
            cargo='Bibliotecário',
            senha='testpass123'
        )
        self.assertEqual(funcionario.cargo, 'Bibliotecário')

class LivroModelTest(TestCase):
    def test_create_livro(self):
        livro = Livro.objects.create(
            titulo='Test Livro',
            autor='Test Autor',
            isbn='1234567890123',
            quantidade=5
        )
        self.assertEqual(livro.titulo, 'Test Livro')
        self.assertEqual(livro.quantidade, 5)

class AcervoModelTest(TestCase):
    def test_create_acervo(self):
        livro = Livro.objects.create(
            titulo='Test Livro',
            autor='Test Autor',
            isbn='1234567890123',
            quantidade=5
        )
        acervo = Acervo.objects.create(
            livro=livro,
            quantidade_disponivel=3
        )
        self.assertEqual(acervo.quantidade_disponivel, 3)

class EmprestimoModelTest(TestCase):
    def test_create_emprestimo(self):
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_completo='Test User'
        )
        funcionario = Funcionario.objects.create(
            usuario=usuario,
            cargo='Bibliotecário',
            senha='testpass123'
        )
        livro = Livro.objects.create(
            titulo='Test Livro',
            autor='Test Autor',
            isbn='1234567890123',
            quantidade=5
        )
        emprestimo = Emprestimo.objects.create(
            usuario=usuario,
            livro=livro,
            funcionario=funcionario
        )
        self.assertEqual(emprestimo.usuario, usuario)
        self.assertEqual(emprestimo.livro, livro) 