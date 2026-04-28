from django.contrib import admin
from .models import Categoria, Artigo


admin.site.register(Categoria)


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    readonly_fields = ('data_criacao',)
    list_display = ('titulo', 'categoria', 'autor', 'data_criacao')

    # 🔐 MELHORIA: melhor visualização do ManyToMany (GRUPOS)
    filter_horizontal = ('grupos_permitidos',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        # Se o artigo é novo
        if not obj.pk:
            usuario_selecionado = obj.autor
            obj.autor_nome = usuario_selecionado.get_full_name() or usuario_selecionado.username

        super().save_model(request, obj, form, change)