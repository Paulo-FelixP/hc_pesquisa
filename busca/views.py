from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Artigo, SearchHistory
from .utils.filtros import pertence_ao_hc
from .services.pubmed import buscar_pubmed
from .services.scielo import buscar_scielo
from .services.lilacs import buscar_lilacs
import pandas as pd
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404




# ============================
# 🔍 BUSCA EM TODAS AS BASES
# ============================
def buscar_artigos(termo):
    artigos = []

    artigos += buscar_pubmed(termo)
    artigos += buscar_scielo(termo)
    artigos += buscar_lilacs(termo)

    filtrados = []

    for art in artigos:
        texto = (
            (art.get("titulo") or "")
            + " "
            + (art.get("autores") or "")
            + " "
            + (art.get("resumo") or "")
            + " "
            + (art.get("afiliacao") or "")
        ).lower()

        if pertence_ao_hc(texto):
            filtrados.append(art)

    return filtrados


# ============================
# 🏠 HOME
# ============================
def home(request):
    return render(
        request,
        "busca/home.html",
        {
            "total": Artigo.objects.count(),
            "pubmed": Artigo.objects.filter(origem="pubmed").count(),
            "scielo": Artigo.objects.filter(origem="scielo").count(),
            "lilacs": Artigo.objects.filter(origem="lilacs").count(),
            "outros": Artigo.objects.exclude(origem__in=["pubmed", "scielo", "lilacs"]).count(),
        },
    )


# ============================
# 🔍 RESULTADOS
# ============================
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from .models import Artigo

def resultados(request):
    termo = request.GET.get("q", "").strip()
    origem = request.GET.get("origem", "").strip().lower()
    tipo = request.GET.get("tipo", "").strip().lower()
    data_inicio = request.GET.get("data_inicio", "").strip()
    data_fim = request.GET.get("data_fim", "").strip()

    artigos = Artigo.objects.all()

    # suportar múltiplas origens separadas por vírgula
    if origem:
        lista_origens = [o.strip() for o in origem.split(",") if o.strip()]
        if lista_origens:
            artigos = artigos.filter(origem__in=lista_origens)

    # filtro por tipo/termo (mantém sua lógica)
    if termo:
        termo_normalizado = termo.replace("[Affiliation]", "").strip(" '\"")

        if tipo == "autor":
            artigos = artigos.filter(autores__icontains=termo_normalizado)
        elif tipo in ["título", "titulo"]:
            artigos = artigos.filter(titulo__icontains=termo_normalizado)
        elif tipo == "tema":
            artigos = artigos.filter(
                Q(resumo__icontains=termo_normalizado) |
                Q(titulo__icontains=termo_normalizado)
            )
        else:
            artigos = artigos.filter(
                Q(titulo__icontains=termo_normalizado) |
                Q(autores__icontains=termo_normalizado) |
                Q(resumo__icontains=termo_normalizado) |
                Q(afiliacao__icontains=termo_normalizado) |
                Q(termo_de_busca__icontains=termo_normalizado)
            )

    # ---------------------------
    # SALVA O HISTÓRICO (sempre que houver filtros ou termo)
    # ---------------------------
    should_save = bool(termo or origem or data_inicio or data_fim or tipo)
    if should_save:
        try:
            # converte dates para None se vierem vazias
            di = data_inicio or None
            df = data_fim or None

            SearchHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                termo=termo,
                origem=origem,
                tipo=tipo,
                data_inicio=di,
                data_fim=df,
                query_string=request.META.get('QUERY_STRING', '')
            )
        except Exception:
            # não quebrar a página se houver erro ao salvar histórico
            pass

    if data_inicio:
        try:
            data_i = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            artigos = artigos.filter(data_publicacao__gte=data_i)
        except:
            pass

    if data_fim:
        try:
            data_f = datetime.strptime(data_fim, "%Y-%m-%d").date()
            artigos = artigos.filter(data_publicacao__lte=data_f)
        except:
            pass

    return render(request, "busca/resultados.html", {
            "artigos": artigos,
            "query": termo,
            "origem": origem,
            "tipo": tipo,
            "data_inicio": data_inicio,
            "data_fim": data_fim
        })


# ============================
#  IMPORTAÇÃO UNIVERSAL
# ============================
import dateparser
from datetime import datetime

@login_required
def upload_artigos(request):

    if request.method == "POST" and request.FILES.get("arquivo"):

        arquivo = request.FILES["arquivo"]

        try:
            nome = arquivo.name.lower()

            df = (
                pd.read_csv(arquivo)
                if nome.endswith(".csv")
                else pd.read_excel(arquivo)
            )

            df.columns = df.columns.str.lower().str.strip()

            total = 0

            # 🔍 Detectar automaticamente a coluna de data
            colunas_possiveis_data = [
                "data",
                "data_publicacao",
                "data de publicação",
                "data de publicacao",
                "publicacao",
                "publication date",
                "publication",
                "ano",
                "year"
            ]

            coluna_data = None
            for c in df.columns:
                if any(key in c for key in colunas_possiveis_data):
                    coluna_data = c
                    break

            for _, row in df.iterrows():
                titulo = row.get("titulo") or row.get("título")
                link = row.get("link")

                if not titulo or not link:
                    continue

                # ------------------------------------------
                #  1) ORIGEM DETECTADA AUTOMATICAMENTE PELO LINK
                # ------------------------------------------
                link_lower = str(link).lower().strip()

                if "pubmed" in link_lower or "ncbi.nlm.nih.gov" in link_lower:
                    origem = "pubmed"

                elif "scielo" in link_lower:
                    origem = "scielo"

                elif "lilacs" in link_lower or "bvsalud" in link_lower:
                    origem = "lilacs"

                else:
                    origem = "outros"

                # ------------------------------------------
                #  2) Extrair PMID
                # ------------------------------------------
                pmid = None
                if "pmid" in df.columns:
                    pmid = str(row.get("pmid"))
                else:
                    try:
                        pmid = link_lower.rstrip("/").split("/")[-1]
                        pmid = pmid if pmid.isdigit() else None
                    except:
                        pmid = None

                if pmid and Artigo.objects.filter(pmid=pmid).exists():
                    continue

                # ------------------------------------------
                # 🔥 3) Extrair DATA DE PUBLICAÇÃO
                # ------------------------------------------
                data_publicacao = None

                if coluna_data:
                    valor_bruto = str(row.get(coluna_data)).strip()

                    if valor_bruto and valor_bruto.lower() != "nan":

                        # Usa o dateparser para interpretar qualquer formato
                        data_parseada = dateparser.parse(
                            valor_bruto,
                            languages=["pt", "en"],
                            settings={
                                "PREFER_DAY_OF_MONTH": "first",
                                "DATE_ORDER": "DMY",
                            }
                        )

                        if data_parseada:
                            data_publicacao = data_parseada.date()
                        else:
                            data_publicacao = None

                # ------------------------------------------
                # 🔥 4) Criar registro no banco
                # ------------------------------------------
                afiliacao = (
                    row.get("termo de busca")
                    or row.get("termo_de_busca")
                    or row.get("afiliacao")
                    or row.get("afiliação")
                    or ""
                )

                if isinstance(afiliacao, str):
                    afiliacao = afiliacao.strip().strip("'").strip('"')

                autores = row.get("autores") or row.get("authors") or ""
                resumo = row.get("resumo") or row.get("abstract") or ""

                Artigo.objects.create(
                    pmid=pmid,
                    titulo=str(titulo).strip(),
                    link=link,
                    origem=origem,
                    autores=str(autores).strip(),
                    resumo=str(resumo).strip(),
                    afiliacao=afiliacao,
                    termo_de_busca=afiliacao,
                    data_publicacao=data_publicacao,     
                )

                total += 1

            messages.success(request, f"{total} artigos importados!")
            return redirect("upload_artigos")

        except Exception as e:
            messages.error(request, f"Erro ao importar: {e}")
            return redirect("upload_artigos")

    return render(request, "busca/upload_artigos.html")

def historico(request):
    qs = SearchHistory.objects.all().select_related("user")
    paginator = Paginator(qs, 30)  # 30 por página
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, "busca/historico.html", {
        "page_obj": page_obj
    })


from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def excluir_artigo(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    artigo.delete()
    messages.success(request, "Artigo excluído com sucesso!")
    return redirect("resultados")

