"""
URL configuration for biblioteca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from biblioteca import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Página inicial
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # URLs de Funcionário
    path('funcionario/', views.funcionario, name='funcionario'),
    path('funcionario/cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('funcionario/editar/<int:funcionario_id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionario/excluir/<int:funcionario_id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('funcionario/consultar/', views.consultar_funcionario, name='consultar_funcionario'),
    
    # URLs de Livro
    path('livro/', views.livro, name='livro'),
    path('livro/cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livro/editar/<int:livro_id>/', views.editar_livro, name='editar_livro'),
    path('livro/excluir/<int:livro_id>/', views.excluir_livro, name='excluir_livro'),
    path('livro/consultar/', views.consultar_livro, name='consultar_livro'),
    
    # URLs de Empréstimo
    path('emprestimo/relatorio/', views.relatorio_emprestimo, name='relatorio_emprestimo'),
    path('emprestimo/consulta/', views.consulta_emprestimo, name='consulta_emprestimo'),
    
    # URLs de Leitor
    path('leitor/', views.leitor, name='leitor'),
    
    # URLs de Acervo
    path('acervo/', views.acervo, name='acervo'),
]
