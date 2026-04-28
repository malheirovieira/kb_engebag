from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from .models import Artigo, Categoria, Tag
from django.db.models import Q


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================
def get_grupos_categoria(categoria):
    while categoria:
        if categoria.grupos_permitidos.exists():
            return categoria.grupos_permitidos.all()
        categoria = categoria.categoria_pai
    return []

def categoria_liberada_session(request, categoria):
    """
    Sobe a árvore: se encontrar restrição direta que NÃO está na sessão, bloqueia.
    Se encontrar uma que ESTÁ na sessão, libera.
    """
    temp_cat = categoria
    while temp_cat:
        if temp_cat.tem_restricao_direta():
            if request.session.get(f"categoria_{temp_cat.id}"):
                return True
            else:
                return False
        temp_cat = temp_cat.categoria_pai
    return True 


# ======================================================
# VIEWS DE NAVEGAÇÃO
# ======================================================
def home(request):
    return render(request, 'home.html')

def base_conhecimento(request):
    categorias = Categoria.objects.all().order_by('nome')
    artigos = Artigo.objects.all().order_by('titulo')

    return render(request, 'base_conhecimento.html', {
        'categorias': categorias,
        'artigos': artigos,
    })

def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    grupos = artigo.grupos_permitidos.all()

    if not grupos.exists():
        categoria = artigo.categoria
        while categoria:
            if categoria.grupos_permitidos.exists():
                grupos = categoria.grupos_permitidos.all()
                break
            categoria = categoria.categoria_pai

    if grupos.exists():
        liberado = (
            request.session.get(f"artigo_{artigo_id}") or
            categoria_liberada_session(request, artigo.categoria)
        )
        if not liberado:
            return HttpResponseForbidden("Acesso negado")

    def get_caminho_recursivo(categoria):
        if not categoria: return []
        return get_caminho_recursivo(categoria.categoria_pai) + [categoria]

    caminho = get_caminho_recursivo(artigo.categoria)

    return render(request, 'artigo_conteudo.html', {
        'artigo': artigo,
        'caminho': caminho,
    })

def buscar_artigos(request):
    query = request.GET.get('q', '').strip()
    if query:
        resultados = Artigo.objects.filter(
            Q(titulo__icontains=query) |
            Q(categoria__nome__icontains=query) |
            Q(tags__nome__icontains=query)
        ).distinct().order_by('titulo')
    else:
        resultados = Artigo.objects.none()

    return render(request, 'resultado_busca.html', {
        'resultados': resultados,
        'query': query
    })


# ======================================================
# VALIDAÇÕES DE CREDENCIAIS
# ======================================================
def validar_credencial_artigo(request, artigo_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "erro": "Método inválido"})

    username = request.POST.get("username")
    password = request.POST.get("password")

    artigo = get_object_or_404(Artigo, id=artigo_id)
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})

    grupos = artigo.grupos_permitidos.all()
    if not grupos.exists():
        categoria = artigo.categoria
        while categoria:
            if categoria.grupos_permitidos.exists():
                grupos = categoria.grupos_permitidos.all()
                break
            categoria = categoria.categoria_pai

    if grupos.exists():
        if not user.groups.filter(id__in=grupos.values_list('id', flat=True)).exists():
            return JsonResponse({"ok": False, "erro": "Sem permissão"})

    request.session[f"artigo_{artigo_id}"] = True
    return JsonResponse({"ok": True})

def validar_credencial_categoria(request, categoria_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "erro": "Método inválido"})

    username = request.POST.get("username")
    password = request.POST.get("password")

    categoria = get_object_or_404(Categoria, id=categoria_id)
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({"ok": False, "erro": "Usuário ou senha inválidos"})

    grupos = get_grupos_categoria(categoria)
    if grupos:
        if not user.groups.filter(id__in=grupos.values_list('id', flat=True)).exists():
            return JsonResponse({"ok": False, "erro": "Sem permissão"})

    request.session[f"categoria_{categoria_id}"] = True
    return JsonResponse({"ok": True})