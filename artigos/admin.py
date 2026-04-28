from django.contrib import admin
from .models import Categoria, Artigo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria_pai')

    # permite adicionar/remover grupos facilmente
    filter_horizontal = ('grupos_permitidos',)


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    readonly_fields = ('data_criacao',)

    list_display = ('titulo', 'categoria', 'autor', 'data_criacao')

    filter_horizontal = ('grupos_permitidos',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            usuario = obj.autor
            obj.nome_autor_snapshot = usuario.get_full_name() or usuario.username

        super().save_model(request, obj, form, change)