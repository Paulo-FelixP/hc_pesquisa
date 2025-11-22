from django.contrib import admin
from .models import Artigo

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'origem', 'termo_de_busca', 'afiliacao', 'criado_em')
    search_fields = ('titulo', 'autores', 'termo_de_busca', 'afiliacao')
