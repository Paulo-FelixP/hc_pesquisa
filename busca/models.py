from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Artigo(models.Model):
    origem = models.CharField(max_length=20)            # pubmed, scielo, lilacs, etc
    pmid = models.CharField(max_length=50, blank=True, null=True)

    titulo = models.TextField()
    link = models.URLField()

    data_publicacao = models.DateField(null=True, blank=True)
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

class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Usuário que executou a busca (se autenticado)"
    )

    termo = models.CharField("termo", max_length=500, blank=True)
    origem = models.CharField("origem(s)", max_length=200, blank=True)   # ex: "pubmed,scielo"
    tipo = models.CharField("tipo", max_length=50, blank=True)           # autor / titulo / tema
    data_inicio = models.DateField("data início", null=True, blank=True)
    data_fim = models.DateField("data fim", null=True, blank=True)

    # opcional: armazenar a query string completa para referência
    query_string = models.TextField("query string", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Busca"
        verbose_name_plural = "Histórico de Buscas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.termo or '(sem termo)'} — {self.origem or 'todas'} — {self.created_at:%Y-%m-%d %H:%M'}"
    
class ArtigoSalvo(models.Model):
    titulo = models.CharField(max_length=255)
    autores = models.CharField(max_length=255, blank=True, null=True)
    ano = models.CharField(max_length=10, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    resumo = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    
class Planilha(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="planilhas"
    )
    nome = models.CharField("Nome da planilha", max_length=150)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "nome")
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.user.username})"


class ItemPlanilha(models.Model):
    planilha = models.ForeignKey(
        Planilha,
        on_delete=models.CASCADE,
        related_name="itens"
    )
    titulo = models.CharField("Título", max_length=500)
    autores = models.CharField("Autores", max_length=500, blank=True)
    resumo = models.TextField("Resumo", blank=True)  # breve trecho do artigo
    data_publicacao = models.DateField("Data de publicação", null=True, blank=True)
    origem = models.CharField("Origem", max_length=30)  # "pubmed", "scielo", "lilacs" ou "outros"
    link = models.URLField("Link")
    adicionado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-adicionado_em"]

    def __str__(self):
        return self.titulo[:80]