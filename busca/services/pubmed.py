import ssl
import urllib.request
from Bio import Entrez
from datetime import datetime
from django.conf import settings

# Ignorar SSL (necessário em redes com proxy corporativo)
ssl._create_default_https_context = ssl._create_unverified_context
urllib.request.install_opener(
    urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
    )
)

def formatar_data_pubmed(data_str):
    """
    Converte yyyy-mm-dd → yyyymmdd (formato aceito pela API do PubMed)
    """
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%Y%m%d")
    except ValueError:
        return None


def buscar_pubmed(termo, data_inicio=None, data_fim=None):
    """
    Busca artigos diretamente no PubMed usando o Entrez.
    Retorna lista padronizada de dicionários com titulo, autores, data, link, PMID.
    """

    Entrez.email = settings.NCBI_EMAIL
    Entrez.tool = settings.NCBI_TOOL

    termo_busca = termo or ""
    
    # Monta faixa de data
    inicio = formatar_data_pubmed(data_inicio)
    fim = formatar_data_pubmed(data_fim)

    if inicio and fim:
        termo_busca += f" AND ({inicio}:{fim}[dp])"
    elif inicio:
        termo_busca += f" AND ({inicio}[dp])"
    elif fim:
        termo_busca += f" AND (:{fim}[dp])"

    try:
        # 1️⃣ Faz a busca no PubMed
        handle = Entrez.esearch(
            db="pubmed",
            term=termo_busca,
            retmax=20  # limite (recomendado)
        )
        record = Entrez.read(handle)
        handle.close()

        ids = record.get("IdList", [])
        if not ids:
            return []

        # 2️⃣ Puxa os detalhes dos artigos
        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="medline",
            retmode="xml"
        )
        artigos = Entrez.read(handle)
        handle.close()

        resultados = []

        for artigo in artigos["PubmedArticle"]:

            # Título
            titulo = artigo["MedlineCitation"]["Article"].get("ArticleTitle", "")

            # Autores
            autores_lista = artigo["MedlineCitation"]["Article"].get("AuthorList", [])
            autores = ", ".join(
                [
                    f"{a.get('LastName', '')} {a.get('Initials', '')}"
                    for a in autores_lista if "LastName" in a
                ]
            )

            # Data
            data_publ = artigo["MedlineCitation"]["Article"].get("ArticleDate", [])
            if data_publ:
                ano = data_publ[0].get("Year", "")
                mes = data_publ[0].get("Month", "")
                dia = data_publ[0].get("Day", "")
                data_fmt = f"{ano}-{mes}-{dia}"
            else:
                data_fmt = ""

            # PMID
            pmid = artigo["MedlineCitation"].get("PMID", "")

            # Link Oficial
            link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            resultados.append(
                {
                    "titulo": titulo,
                    "autores": autores,
                    "data_publicacao": data_fmt,
                    "link": link,
                    "pmid": pmid,
                    "origem": "PubMed",
                }
            )

        return resultados

    except Exception as e:
        print("Erro PubMed:", e)
        return []
