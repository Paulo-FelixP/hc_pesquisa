from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import csv

from .models import Planilha, ItemPlanilha


# ---------------------------------------------
#  LISTAR PLANILHAS DO USUÁRIO
# ---------------------------------------------
@login_required
def lista_planilhas(request):
    planilhas = Planilha.objects.filter(user=request.user)
    return render(request, "busca/planilhas.html", {"planilhas": planilhas})


# ---------------------------------------------
#  CRIAR PLANILHA
# ---------------------------------------------
@login_required
def criar_planilha(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()

        if not nome:
            messages.error(request, "O nome da planilha não pode estar vazio.")
            return redirect("lista_planilhas")

        # evitar nome duplicado
        if Planilha.objects.filter(user=request.user, nome=nome).exists():
            messages.error(request, "Você já tem uma planilha com esse nome.")
            return redirect("lista_planilhas")

        Planilha.objects.create(user=request.user, nome=nome)
        messages.success(request, "Planilha criada com sucesso!")
        return redirect("lista_planilhas")

    return redirect("lista_planilhas")


# ---------------------------------------------
#  ADICIONAR ARTIGO À PLANILHA
# ---------------------------------------------
@login_required
def adicionar_item(request, planilha_id):
    """
    Adiciona item POST para uma planilha.
    Aceita tanto campos sem prefixo (titulo, autores, ...) quanto com prefixo h_ (h_titulo...).
    Tenta parsear data em formatos comuns e trunca link para evitar erro de comprimento.
    """
    planilha = get_object_or_404(Planilha, id=planilha_id, user=request.user)

    if request.method != "POST":
        return redirect(request.META.get('HTTP_REFERER', 'lista_planilhas'))

    # helper: pega key ou h_key
    def get_post(key):
        return request.POST.get(key) or request.POST.get(f"h_{key}") or ""

    titulo = get_post("titulo").strip()
    autores = get_post("autores").strip()
    resumo = get_post("resumo").strip()
    origem = get_post("origem").strip()
    link = get_post("link").strip()
    data_raw = get_post("data_publicacao").strip()

    if not titulo:
        messages.error(request, "Título do artigo ausente — impossível adicionar.")
        return redirect(request.META.get('HTTP_REFERER', 'lista_planilhas'))

    # parse de data tolerante
    data_pub = None

    if data_raw:
        data_raw = data_raw.strip()

        formatos = [
            "%Y-%m-%d",      # 2020-03-15
            "%d/%m/%Y",      # 15/03/2020
            "%Y/%m/%d",      # 2020/03/15
            "%Y",            # 2020
            "%Y %b",         # 2020 Mar
            "%Y %b %d",      # 2020 Mar 15
            "%d %b %Y",      # 15 Mar 2020
        ]

        for fmt in formatos:
            try:
                data_pub = datetime.strptime(data_raw, fmt).date()
                break
            except:
                pass

    # fallback: ano sozinho com garantia
    if not data_pub and len(data_raw) == 4 and data_raw.isdigit():
        data_pub = datetime.strptime(data_raw, "%Y").date().replace(month=1, day=1)

    # evita erros de DB por comprimento de campo (URLField default 200)
    if link and len(link) > 200:
        link = link[:200]

    try:
        ItemPlanilha.objects.create(
            planilha=planilha,
            titulo=titulo,
            autores=autores[:500],
            resumo=resumo[:2000],
            origem=origem or 'indefinido',
            link=link or '',
            data_publicacao=data_pub or None,
        )
        messages.success(request, f"Artigo adicionado à planilha '{planilha.nome}'.")
    except Exception as e:
        # evita 500 silencioso e fornece mensagem amigável
        messages.error(request, f"Erro ao adicionar artigo: {e}")
        print(f"[ERRO adicionar_item] user={request.user} planilha={planilha_id} erro={e}")

    return redirect(request.META.get('HTTP_REFERER', 'lista_planilhas'))

# ---------------------------------------------
#  REMOVER ITEM DA PLANILHA
# ---------------------------------------------
@login_required
def remover_item(request, planilha_id, item_id):
    planilha = get_object_or_404(Planilha, id=planilha_id, user=request.user)
    item = get_object_or_404(ItemPlanilha, id=item_id, planilha=planilha)
    item.delete()
    messages.success(request, "Artigo removido da planilha.")
    return redirect("lista_planilhas")


# ---------------------------------------------
#  APAGAR PLANILHA COMPLETA
# ---------------------------------------------
@login_required
def apagar_planilha(request, planilha_id):
    planilha = get_object_or_404(Planilha, id=planilha_id, user=request.user)
    planilha.delete()
    messages.success(request, "Planilha apagada com sucesso.")
    return redirect("lista_planilhas")



# ---------------------------------------------
#  DOWNLOAD CSV
# ---------------------------------------------
@login_required
def download_planilha(request, planilha_id):
    planilha = get_object_or_404(Planilha, id=planilha_id, user=request.user)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{planilha.nome}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Título", "Autores", "Resumo", "Data", "Origem", "Link"])

    for item in planilha.itens.all():
        writer.writerow([
            item.titulo,
            item.autores,
            item.resumo,
            item.data_publicacao or "",
            item.origem,
            item.link,
        ])

    return response

# ---------------------------------------------
#  visualizar PLANILHA
# ---------------------------------------------
@login_required

@login_required
def visualizar_planilha(request, planilha_id):
    planilha = get_object_or_404(Planilha, id=planilha_id, user=request.user)
    itens = planilha.itens.all()

    return render(request, "busca/visualizar_planilha.html", {
        "planilha": planilha,
        "itens": itens,
    })
