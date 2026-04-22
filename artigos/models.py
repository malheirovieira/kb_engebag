from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    # Adicionamos o campo 'mae' (ou parent)
    categoria_pai = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategorias'
    )

    def __str__(self):
        # Opcional: Mostra o caminho completo no Admin (Ex: Tecnologia > Python)
        if self.categoria_pai:
            return f"{self.categoria_pai.nome} > {self.nome}"
        return self.nome


class Artigo(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    # Este campo continua igual, ele aceitará tanto categorias principais quanto subcategorias
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem_capa = models.ImageField(upload_to='artigos/fotos/', null=True, blank=True)

    def __str__(self):
        return self.titulo