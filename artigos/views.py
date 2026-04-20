from django.shortcuts import render, get_object_or_404
from .models import Artigo, Categoria
from django.db.models import Q 

def home(request):
    return render(request, 'home.html')

def base_conhecimento(request):
    categorias = Categoria.objects.all()
    artigos = Artigo.objects.all()
    context = {
        'categorias': categorias,
        'artigos': artigos,
    }
    return render(request, 'base_conhecimento.html', context)

def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    return render(request, 'artigo_conteudo.html', {'artigo': artigo})

def buscar_artigos(request):
    query = request.GET.get('q', '').strip()
    if query:
        # Filtra os artigos por título ou conteúdo
        resultados = Artigo.objects.filter(
            Q(titulo__icontains=query) | Q(conteudo__icontains=query)
        )
    else:
        resultados = Artigo.objects.none()
    
    return render(request, 'resultado_busca.html', {'resultados': resultados, 'query': query})