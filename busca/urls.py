from django.urls import path
from . import views
from . import views_planilhas

urlpatterns = [
    path("", views.home, name="home"),
    path("resultados/", views.resultados, name="resultados"),
    path("importar/", views.upload_artigos, name="upload_artigos"),
    path("historico/", views.historico, name="historico"),
    path("excluir/<int:id>/", views.excluir_artigo, name="excluir_artigo"),
    path("salvar/", views.salvar_artigo, name="salvar_artigo"),
    path("salvos/", views.lista_salvos, name="lista_salvos"),
    path("remover/<int:id>/", views.remover_salvo, name="remover_salvo"),
    path("historico/delete/<int:id>/", views.apagar_historico, name="apagar_historico"),
    path("planilhas/", views_planilhas.lista_planilhas, name="lista_planilhas"),
    path("planilhas/criar/", views_planilhas.criar_planilha, name="criar_planilha"),
    path("planilhas/<int:planilha_id>/adicionar/", views_planilhas.adicionar_item, name="adicionar_item"),
    path("planilhas/<int:planilha_id>/remover/<int:item_id>/", views_planilhas.remover_item, name="remover_item"),
    path("planilhas/<int:planilha_id>/apagar/", views_planilhas.apagar_planilha, name="apagar_planilha"),
    path("planilhas/<int:planilha_id>/download/", views_planilhas.download_planilha, name="download_planilha"),
    path("planilhas/<int:planilha_id>/", views_planilhas.visualizar_planilha, name="visualizar_planilha"),



]
