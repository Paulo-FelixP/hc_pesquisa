from django.contrib import admin
from .models import Artigo, SearchHistory

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'origem', 'termo_de_busca', 'afiliacao', 'criado_em')
    search_fields = ('titulo', 'autores', 'termo_de_busca', 'afiliacao')

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("termo", "origem", "tipo", "data_inicio", "data_fim", "user", "created_at")
    list_filter = ("origem", "tipo", "created_at", "user")
    search_fields = ("termo", "query_string", "origem", "tipo")
    readonly_fields = ("created_at",)