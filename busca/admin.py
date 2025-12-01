from django.contrib import admin
from .models import Artigo, SearchHistory, Planilha, ItemPlanilha

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


@admin.register(Planilha)
class PlanilhaAdmin(admin.ModelAdmin):
    list_display = ("nome", "user", "criado_em")
    search_fields = ("nome", "user__username")

@admin.register(ItemPlanilha)
class ItemPlanilhaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "planilha", "origem", "data_publicacao", "adicionado_em")
    search_fields = ("titulo", "autores")