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
    """Retorna o conteúdo do artigo com rastro de pão completo e infinito."""
    artigo = get_object_or_404(Artigo, id=artigo_id)
    
    def get_caminho_recursivo(categoria):
        """Função interna para escalar a árvore de categorias até o topo."""
        if not categoria:
            return []
        
        # Tenta pegar o pai (testa 'pai' ou 'parent')
        pai = None
        if hasattr(categoria, 'pai'):
            pai = categoria.pai
        elif hasattr(categoria, 'parent'):
            pai = categoria.parent
            
        # RECURSÃO: Pega o caminho do pai e adiciona o nome da categoria atual no final
        return get_caminho_recursivo(pai) + [categoria.nome]

    # Gera a lista completa: ['DEPARTAMENTO', 'PROGRAMA', 'SUBCATEGORIA']
    caminho = get_caminho_recursivo(artigo.categoria)

    context = {
        'artigo': artigo,
        'caminho': caminho,
    }
    
    response = render(request, 'artigo_conteudo.html', context)
    
    # Cabeçalhos para o JavaScript e HTMX
    response['X-Artigo-ID'] = str(artigo.id)
    if artigo.categoria:
        response['X-Categoria-ID'] = str(artigo.categoria.id)
    
    return response

def buscar_artigos(request):
    """Busca precisa por Título, Nome da Categoria ou Tags."""
    query = request.GET.get('q', '').strip()
    if query:
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