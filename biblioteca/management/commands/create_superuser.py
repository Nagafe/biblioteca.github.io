from django.core.management.base import BaseCommand
from biblioteca.models import Usuario, Funcionario

class Command(BaseCommand):
    help = 'Cria um superusuário que também é funcionário'

    def handle(self, *args, **options):
        # Criar o superusuário
        usuario = Usuario.objects.create_superuser(
            username='admin',
            email='admin@biblioteca.com',
            password='admin123',
            nome_completo='Administrador'
        )
        
        # Criar o funcionário vinculado ao usuário
        funcionario = Funcionario.objects.create(
            usuario=usuario,
            cargo='Administrador',
            senha='admin123'
        )
        
        self.stdout.write(self.style.SUCCESS('Superusuário e funcionário criados com sucesso!'))
        self.stdout.write('Username: admin')
        self.stdout.write('Email: admin@biblioteca.com')
        self.stdout.write('Senha: admin123') 