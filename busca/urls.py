from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("resultados/", views.resultados, name="resultados"),
    path("importar/", views.upload_artigos, name="upload_artigos"),
    path("historico/", views.historico, name="historico"),
    path("excluir/<int:id>/", views.excluir_artigo, name="excluir_artigo"),


]
