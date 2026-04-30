from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from .models import Artigo, Categoria, Tag
from django.db.models import Q
from django.views.decorators.cache import never_cache

# ======================================================
# 1. FUNÇÃO DE RASTREIO
# ======================================================
def obter_todos_grupos_da_linhagem(categoria):
    grupos = set()
    curr = categoria
    while curr:
        if curr.grupos_permitidos.exists():
            grupos.update(curr.grupos_permitidos.values_list('id', flat=True))
        curr = curr.categoria_pai
    return grupos

# ======================================================
# 2. O FILTRO DO INPUT DE BUSCA
# ======================================================
@never_cache
def buscar_artigos(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'resultado_busca.html', {'resultados': [], 'query': query})

    artigos_encontrados = Artigo.objects.filter(
        Q(titulo__icontains=query) | 
        Q(categoria__nome__icontains=query) |
        Q(tags__nome__icontains=query)
    ).distinct()

    resultados_filtrados = []
    user = request.user
    user_group_ids = set(user.groups.values_list('id', flat=True)) if user.is_authenticated else set()

    for artigo in artigos_encontrados:
        grupos_obrigatorios = obter_todos_grupos_da_linhagem(artigo.categoria)
        if artigo.grupos_permitidos.exists():
            grupos_obrigatorios.update(artigo.grupos_permitidos.values_list('id', flat=True))

        if grupos_obrigatorios:
            if not (user_group_ids & grupos_obrigatorios) and not user.is_superuser:
                continue 
        resultados_filtrados.append(artigo)

    return render(request, 'resultado_busca.html', {'resultados': resultados_filtrados, 'query': query})

# ======================================================
# 3. VIEWS PRINCIPAIS
# ======================================================
def home(request):
    return render(request, 'home.html')

def base_conhecimento(request):
    return render(request, 'base_conhecimento.html', {
        'categorias': Categoria.objects.all().order_by('nome'),
        'artigos': Artigo.objects.all().order_by('titulo')
    })

@never_cache
def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    
    # Verifica grupos necessários para o artigo (dele + pais)
    grupos_ids = obter_todos_grupos_da_linhagem(artigo.categoria)
    if artigo.grupos_permitidos.exists():
        grupos_ids.update(artigo.grupos_permitidos.values_list('id', flat=True))

    # LÓGICA DE HERANÇA DE SESSÃO:
    # Se o artigo exige grupo, verificamos se ele OU qualquer categoria pai foi validada
    if grupos_ids and not request.user.is_superuser:
        # 1. Verifica se o artigo em si foi validado
        validado = request.session.get(f"artigo_{artigo_id}")
        
        # 2. Se não, percorre a linhagem de categorias para ver se o pai foi validado
        if not validado:
            curr_cat = artigo.categoria
            while curr_cat:
                if request.session.get(f"categoria_{curr_cat.id}"):
                    validado = True
                    break
                curr_cat = curr_cat.categoria_pai

        if not validado:
            if request.headers.get('HX-Request'):
                return HttpResponseForbidden("Acesso restrito.")
            return render(request, 'base_conhecimento.html', {
                'categorias': Categoria.objects.all().order_by('nome'),
                'abrir_modal_auto': True,
                'artigo_id_pendente': artigo.id
            })

    if request.headers.get('HX-Request'):
        return render(request, 'artigo_conteudo.html', {'artigo': artigo})
    
    return render(request, 'base_conhecimento.html', {
        'categorias': Categoria.objects.all().order_by('nome'),
        'artigo_direto': artigo
    })

# ======================================================
# 4. VALIDAÇÕES DE CREDENCIAIS
# ======================================================
def validar_credencial_artigo(request, artigo_id):
    if request.method != "POST": return JsonResponse({"ok": False})
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    
    if not user: return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})
    
    artigo = get_object_or_404(Artigo, id=artigo_id)
    grupos_permitidos_ids = obter_todos_grupos_da_linhagem(artigo.categoria)
    if artigo.grupos_permitidos.exists():
        grupos_permitidos_ids.update(artigo.grupos_permitidos.values_list('id', flat=True))
    
    user_groups_ids = set(user.groups.values_list('id', flat=True))
    if grupos_permitidos_ids and not user.is_superuser:
        if not (user_groups_ids & grupos_permitidos_ids):
            return JsonResponse({"ok": False, "erro": "Seu usuário não tem permissão para este grupo."})

    request.session.set_expiry(0) 
    request.session[f"artigo_{artigo_id}"] = True
    return JsonResponse({"ok": True})

def validar_credencial_categoria(request, categoria_id):
    if request.method != "POST": return JsonResponse({"ok": False})
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    
    if not user: return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    grupos_permitidos_ids = obter_todos_grupos_da_linhagem(categoria)
    
    user_groups_ids = set(user.groups.values_list('id', flat=True))
    if grupos_permitidos_ids and not user.is_superuser:
        if not (user_groups_ids & grupos_permitidos_ids):
            return JsonResponse({"ok": False, "erro": "Seu usuário não tem permissão para esta categoria."})

    request.session.set_expiry(0)
    request.session[f"categoria_{categoria_id}"] = True
    return JsonResponse({"ok": True})