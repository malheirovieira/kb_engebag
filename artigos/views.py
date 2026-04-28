from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from .models import Artigo, Categoria, Tag
from django.db.models import Q
from django.views.decorators.cache import never_cache

# ======================================================
# 1. FUNÇÃO DE RASTREIO (VERIFICA AS PASTAS PAI)
# ======================================================
def obter_todos_grupos_da_linhagem(categoria):
    """
    Sobe a árvore de categorias. Se a pasta 'TI' tiver grupo,
    esse grupo é adicionado à lista de restrições do artigo.
    """
    grupos = set()
    curr = categoria
    while curr:
        if curr.grupos_permitidos.exists():
            grupos.update(curr.grupos_permitidos.values_list('id', flat=True))
        curr = curr.categoria_pai
    return grupos

# ======================================================
# 2. O FILTRO DO INPUT DE BUSCA (HTMX)
# ======================================================
@never_cache
def buscar_artigos(request):
    """
    Esta é a função que o seu Search Input acessa.
    O bloqueio acontece AQUI, antes de enviar o HTML para a tela.
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'resultado_busca.html', {'resultados': [], 'query': query})

    # Busca bruta por texto
    artigos_encontrados = Artigo.objects.filter(
        Q(titulo__icontains=query) | Q(categoria__nome__icontains=query)
    ).distinct()

    resultados_filtrados = []
    
    # Identifica o usuário e seus grupos
    user = request.user
    user_group_ids = set(user.groups.values_list('id', flat=True)) if user.is_authenticated else set()

    for artigo in artigos_encontrados:
        # LOGICA DE BLOQUEIO:
        # Pega as restrições de toda a árvore (TI > GOVERNANÇA > ... > INTEGRAÇÃO)
        grupos_obrigatorios = obter_todos_grupos_da_linhagem(artigo.categoria)
        
        # Adiciona também se o artigo tiver grupo próprio
        if artigo.grupos_permitidos.exists():
            grupos_obrigatorios.update(artigo.grupos_permitidos.values_list('id', flat=True))

        # Se houver qualquer cadeado na linhagem e o user não tiver a chave:
        if grupos_obrigatorios:
            # Se for superusuario, você pode decidir se quer ver ou não.
            # Para testar o bloqueio real, deixe o if abaixo comentado.
            # if user.is_superuser: pass 
            
            if not (user_group_ids & grupos_obrigatorios):
                # PULA este artigo. Ele não vai para a lista 'resultados_filtrados'
                continue 

        resultados_filtrados.append(artigo)

    # Retorna apenas o que passou no filtro de segurança
    return render(request, 'resultado_busca.html', {
        'resultados': resultados_filtrados,
        'query': query
    })

# ======================================================
# 3. OUTRAS VIEWS (HOME, DETALHE, ETC)
# ======================================================
def home(request):
    return render(request, 'home.html')

def base_conhecimento(request):
    return render(request, 'base_conhecimento.html', {
        'categorias': Categoria.objects.all().order_by('nome'),
        'artigos': Artigo.objects.all().order_by('titulo')
    })

def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    
    # Proteção extra para acesso via URL direta
    grupos_ids = obter_todos_grupos_da_linhagem(artigo.categoria)
    if grupos_ids and not (set(request.user.groups.values_list('id', flat=True)) & grupos_ids):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Acesso restrito.")
            
    return render(request, 'artigo_conteudo.html', {'artigo': artigo})

def validar_credencial_artigo(request, artigo_id):
    if request.method != "POST": return JsonResponse({"ok": False})
    user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if not user: return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})
    request.session[f"artigo_{artigo_id}"] = True
    return JsonResponse({"ok": True})

def validar_credencial_categoria(request, categoria_id):
    if request.method != "POST": return JsonResponse({"ok": False})
    user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
    if not user: return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})
    request.session[f"categoria_{categoria_id}"] = True
    return JsonResponse({"ok": True})