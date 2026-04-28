from django.db import models
from django.conf import settings 
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import Group


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    categoria_pai = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategorias'
    )

    def __str__(self):
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome


class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Artigo(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = RichTextUploadingField() 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    nome_autor_snapshot = models.CharField(max_length=255, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name='artigos')

    imagem_capa = models.ImageField(upload_to='artigos/fotos/', null=True, blank=True)
    arquivo_pdf = models.FileField(upload_to='artigos/documentos/', null=True, blank=True)

    
    grupos_permitidos = models.ManyToManyField(Group, blank=True)

    def exige_credencial(self):
        return self.grupos_permitidos.exists()

    def __str__(self):
        return self.titulo