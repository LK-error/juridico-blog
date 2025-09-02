# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs de listagem e detalhe
    path('', views.lista_de_artigos, name='lista_de_artigos'),
    path('artigo/<int:pk>/', views.detalhe_do_artigo, name='detalhe_do_artigo'),
    path('categoria/<int:categoria_id>/', views.artigos_por_categoria, name='artigos_por_categoria'),

    # URLs para criar e editar conteúdo
    path('artigo/novo/', views.criar_conteudo, name='criar_conteudo'),
    path('artigo/<int:pk>/editar/', views.editar_artigo, name='editar_artigo'),
    
    # URLs de autenticação
    path('login/', views.pagina_de_login, name='login'),
    path('logout/', views.pagina_de_logout, name='logout'),

    # NOVA ROTA para a página da equipe
    path('equipe/', views.pagina_equipe, name='equipe'),
]