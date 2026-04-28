from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from .models import Artigo, Categoria, Tag
from django.db.models import Q


def home(request):
    return render(request, 'home.html')


def base_conhecimento(request):
    categorias = Categoria.objects.all().order_by('nome')
    artigos = Artigo.objects.all().order_by('titulo')

    context = {
        'categorias': categorias,
        'artigos': artigos,
    }
    return render(request, 'base_conhecimento.html', context)


def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    # 🔐 bloqueio por sessão
    if artigo.grupos_permitidos.exists():
        if not request.session.get(f"artigo_{artigo_id}"):
            return HttpResponseForbidden("Acesso negado")

    def get_caminho_recursivo(categoria):
        if not categoria:
            return []

        pai = None
        if hasattr(categoria, 'categoria_pai'):
            pai = categoria.categoria_pai

        return get_caminho_recursivo(pai) + [categoria]

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
# 🔐 VALIDAÇÃO DE CREDENCIAL (CORRIGIDA E SEGURA)
# ======================================================
def validar_credencial_artigo(request, artigo_id):

    if request.method != "POST":
        return JsonResponse({
            "ok": False,
            "erro": "Método inválido"
        })

    username = request.POST.get("username")
    password = request.POST.get("password")

    artigo = get_object_or_404(Artigo, id=artigo_id)

    # 🔑 autenticação Django
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({
            "ok": False,
            "erro": "Usuário ou senha inválidos"
        })

    # 🔐 valida grupo
    if artigo.grupos_permitidos.exists():

        grupos_artigo = artigo.grupos_permitidos.values_list('id', flat=True)

        if not user.groups.filter(id__in=list(grupos_artigo)).exists():
            return JsonResponse({
                "ok": False,
                "erro": "Usuário não tem permissão para este artigo"
            })

    # ✅ libera sessão
    request.session[f"artigo_{artigo_id}"] = True

    return JsonResponse({"ok": True})