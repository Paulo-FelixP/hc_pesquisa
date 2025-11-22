from django.db import models


class Artigo(models.Model):
    origem = models.CharField(max_length=20)            # pubmed, scielo, lilacs, etc
    pmid = models.CharField(max_length=50, blank=True, null=True)

    titulo = models.TextField()
    link = models.URLField()

    data_publicacao = models.DateField(blank=True, null=True)
    autores = models.TextField(blank=True, null=True)
    resumo = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    # 🔥 Campos importantes
    afiliacao = models.TextField(blank=True, null=True)
    termo_de_busca = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.titulo


class Afiliacao(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome
