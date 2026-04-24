from django.shortcuts import render, get_object_or_404
from .models import Artigo, Categoria, Tag
from django.db.models import Q 

def home(request):
    """Renderiza a página inicial do portal."""
    return render(request, 'home.html')

def base_conhecimento(request):
    """Exibe a estrutura da Base de Conhecimento com categorias e artigos."""
    categorias = Categoria.objects.all().order_by('nome')
    artigos = Artigo.objects.all().order_by('titulo')
    
    context = {
        'categorias': categorias,
        'artigos': artigos,
    }
    return render(request, 'base_conhecimento.html', context)

def detalhe_artigo(request, artigo_id):
    """Retorna o conteúdo do artigo e envia IDs para o menu lateral."""
    artigo = get_object_or_404(Artigo, id=artigo_id)
    response = render(request, 'artigo_conteudo.html', {'artigo': artigo})
    
    response['X-Artigo-ID'] = str(artigo.id)
    response['X-Categoria-ID'] = str(artigo.categoria.id)
    
    return response

def buscar_artigos(request):
    """Busca precisa por Título, Nome da Categoria ou Tags."""
    query = request.GET.get('q', '').strip()
    if query:
        # Filtra por Título, Nome da Categoria ou Nome da Tag
        # Removido o filtro de 'conteudo' conforme solicitado
        resultados = Artigo.objects.filter(
            Q(titulo__icontains=query) | 
            Q(categoria__nome__icontains=query) |
            Q(tags__nome__icontains=query)
        ).distinct().order_by('titulo')
    else:
        resultados = Artigo.objects.none()
    
    context = {
        'resultados': resultados, 
        'query': query
    }
    return render(request, 'resultado_busca.html', context)