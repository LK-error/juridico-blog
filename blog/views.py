# blog/views.py

# --- 1. IMPORTS ORGANIZADOS ---
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
# MUDANÇA AQUI: Adicionamos Perfil à lista
from .models import Artigo, Categoria, LinkExterno, Perfil 
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ConteudoForm
from django.http import HttpResponseForbidden


# --- 2. VIEWS RELACIONADAS AO CONTEÚDO ---

@login_required 
def lista_de_artigos(request):
    #... (código existente, sem alterações)
    titulo_query = request.GET.get('titulo')
    autor_query = request.GET.get('autor')
    categoria_query_id = request.GET.get('categoria')
    artigos_list = Artigo.objects.all()
    links_list = LinkExterno.objects.all()
    if titulo_query:
        artigos_list = artigos_list.filter(titulo__icontains=titulo_query)
        links_list = links_list.filter(titulo__icontains=titulo_query)
    if autor_query:
        autor_filter = Q(autor__first_name__icontains=autor_query) | Q(autor__last_name__icontains=autor_query)
        artigos_list = artigos_list.filter(autor_filter)
        links_list = links_list.filter(autor_filter)
    if categoria_query_id:
        artigos_list = artigos_list.filter(categoria__id=categoria_query_id)
        links_list = links_list.filter(categoria__id=categoria_query_id)
    lista_combinada = []
    for artigo in artigos_list:
        artigo.tipo = 'Artigo'
        lista_combinada.append(artigo)
    for link in links_list:
        link.tipo = 'LinkExterno'
        lista_combinada.append(link)
    lista_combinada.sort(key=lambda item: item.data_publicacao, reverse=True)
    paginator = Paginator(lista_combinada, 10)
    page_number = request.GET.get('page')
    pagina_de_conteudo = paginator.get_page(page_number)
    categorias = Categoria.objects.all()
    titulo_da_pagina = "Conteúdo Recente"
    contexto = {
        'pagina_de_conteudo': pagina_de_conteudo,
        'categorias': categorias,
        'titulo_da_pagina': titulo_da_pagina,
        'titulo_query': titulo_query,
        'autor_query': autor_query,
        'categoria_query_id': int(categoria_query_id) if categoria_query_id else None,
    }
    return render(request, 'blog/index.html', contexto)


@login_required
def detalhe_do_artigo(request, pk):
    #... (código existente, sem alterações)
    artigo = get_object_or_404(Artigo, pk=pk)
    categorias = Categoria.objects.all()
    contexto = {
        'artigo': artigo,
        'categorias': categorias,
    }
    return render(request, 'blog/artigo_detalhe.html', contexto)


@login_required
def artigos_por_categoria(request, categoria_id):
    #... (código existente, sem alterações)
    categoria = get_object_or_404(Categoria, id=categoria_id)
    artigos_list = Artigo.objects.filter(categoria=categoria)
    links_list = LinkExterno.objects.filter(categoria=categoria)
    lista_combinada = []
    for artigo in artigos_list:
        artigo.tipo = 'Artigo'
        lista_combinada.append(artigo)
    for link in links_list:
        link.tipo = 'LinkExterno'
        lista_combinada.append(link)
    lista_combinada.sort(key=lambda item: item.data_publicacao, reverse=True)
    categorias = Categoria.objects.all()
    paginator = Paginator(lista_combinada, 10)
    page_number = request.GET.get('page')
    pagina_de_conteudo = paginator.get_page(page_number)
    contexto = {
        'pagina_de_conteudo': pagina_de_conteudo,
        'categoria_atual': categoria,
        'categorias': categorias,
        'titulo_da_pagina': f"Conteúdo na categoria: {categoria.nome}",
    }
    return render(request, 'blog/index.html', contexto)


@login_required
def pagina_equipe(request):
    query = request.GET.get('q')
    perfis = Perfil.objects.all().order_by('usuario__first_name')

    if query:
        perfis = perfis.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(area_atuacao__icontains=query)
        ).distinct()

    categorias = Categoria.objects.all()
    contexto = {
        'perfis': perfis,
        'categorias': categorias,
        'query': query,
    }
    return render(request, 'blog/equipe.html', contexto)


# --- 3. VIEWS PARA CRIAR E EDITAR CONTEÚDO ---

@login_required
def criar_conteudo(request):
    if request.method == 'POST':
        form = ConteudoForm(request.POST)
        if form.is_valid():
            # Pega os dados validados do formulário
            dados = form.cleaned_data
            tipo_conteudo = dados.get('tipo_conteudo')
            
            # Lógica para salvar um ARTIGO
            if tipo_conteudo == 'artigo':
                novo_artigo = Artigo.objects.create(
                    titulo=dados.get('titulo'),
                    categoria=dados.get('categoria'),
                    conteudo=dados.get('conteudo'),
                    autor=request.user
                )
                return redirect('detalhe_do_artigo', pk=novo_artigo.pk)

            # Lógica para salvar um LINK EXTERNO
            elif tipo_conteudo == 'link':
                LinkExterno.objects.create(
                    titulo=dados.get('titulo'),
                    categoria=dados.get('categoria'),
                    link_url=dados.get('link_url'),
                    resumo=dados.get('resumo'),
                    autor=request.user
                )
                return redirect('lista_de_artigos')
    else:
        form = ConteudoForm()

    contexto = {'form': form, 'titulo_pagina': 'Criar Novo Conteúdo'}
    return render(request, 'blog/artigo_form.html', contexto)


@login_required
def editar_artigo(request, pk):
    # A lógica de edição ficará focada apenas em Artigos por enquanto
    # para manter a simplicidade.
    artigo = get_object_or_404(Artigo, pk=pk)

    if artigo.autor != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este artigo.")
        
    # O formulário de edição usará o ConteudoForm, mas adaptado
    if request.method == 'POST':
        # Como é um formulário genérico, precisamos preencher manualmente
        form = ConteudoForm(request.POST, initial={'tipo_conteudo': 'artigo'})
        if form.is_valid():
            dados = form.cleaned_data
            artigo.titulo = dados.get('titulo')
            artigo.categoria = dados.get('categoria')
            artigo.conteudo = dados.get('conteudo')
            artigo.save()
            return redirect('detalhe_do_artigo', pk=artigo.pk)
    else:
        form = ConteudoForm(initial={
            'tipo_conteudo': 'artigo',
            'titulo': artigo.titulo,
            'categoria': artigo.categoria,
            'conteudo': artigo.conteudo,
        })
    
    contexto = {'form': form, 'titulo_pagina': 'Editar Artigo'}
    return render(request, 'blog/artigo_form.html', contexto)


# --- 4. VIEWS RELACIONADAS À AUTENTICAÇÃO ---

def pagina_de_login(request):
    #...código existente...
    if request.method == 'POST':
        email_formulario = request.POST.get('username')
        senha = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email_formulario)
            nome_de_usuario_real = user_obj.username
            user = authenticate(request, username=nome_de_usuario_real, password=senha)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('lista_de_artigos')
        else:
            contexto = {'error_message': 'E-mail ou senha inválidos.'}
            return render(request, 'blog/login.html', contexto)
    else:
        return render(request, 'blog/login.html')


def pagina_de_logout(request):
    #...código existente...
    logout(request)
    return redirect('login')