from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Artigo
from .utils.filtros import pertence_ao_hc
from .services.pubmed import buscar_pubmed
from .services.scielo import buscar_scielo
from .services.lilacs import buscar_lilacs
import pandas as pd
from django.db.models import Q


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
def resultados(request):
    termo = request.GET.get("q", "").strip()
    origem = request.GET.get("origem", "").strip().lower()
    tipo = request.GET.get("tipo", "").strip().lower()

    # === Padroniza origem para coincidir com o que está no banco ===
    mapa_origem = {
        "pubmed": "PubMed",
        "scielo": "Scielo",
        "lilacs": "Lilacs",
        "capes": "Capes Periódicos",
    }

    origem_corrigida = mapa_origem.get(origem, "")

    artigos = Artigo.objects.all()

    # ---- FILTRO POR ORIGEM ----
    if origem_corrigida:
        artigos = artigos.filter(origem=origem_corrigida)

    # ---- FILTRO POR TIPO (autor, título, tema) ----
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

    return render(request, "busca/resultados.html", {
        "artigos": artigos,
        "query": termo,
        "origem": origem,
        "tipo": tipo
    })

# ============================
#  IMPORTAÇÃO UNIVERSAL
# ============================
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

            for _, row in df.iterrows():
                titulo = row.get("titulo") or row.get("título")
                link = row.get("link")

                if not titulo or not link:
                    continue

                # ------------------------------------------
                # 🔥 1) ORIGEM DETECTADA AUTOMATICAMENTE PELO LINK
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

                # Extrai PMID
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
                    origem=origem,  # ← ORIGEM FINAL
                    autores=str(autores).strip(),
                    resumo=str(resumo).strip(),
                    afiliacao=afiliacao,
                    termo_de_busca=afiliacao,
                )

                total += 1

            messages.success(request, f"{total} artigos importados!")
            return redirect("upload_artigos")

        except Exception as e:
            messages.error(request, f"Erro ao importar: {e}")
            return redirect("upload_artigos")

    return render(request, "busca/upload_artigos.html")
