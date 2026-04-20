from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Artigo(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem_capa = models.ImageField(upload_to='artigos/fotos/', null=True, blank=True)

    def __str__(self):
        return self.titulo