from ..models import Artigo

def identificar_base(df):
    colunas = [c.lower() for c in df.columns]

    if "pmid" in colunas:
        return "pubmed"

    if "lilacs" in colunas or "decs" in colunas or "id_lilacs" in colunas:
        return "lilacs"

    if "scielo" in colunas or "revista" in colunas:
        return "scielo"

    if "doi" in colunas and "titulo" in colunas:
        return "capes"

    return "desconhecido"

def importar_lilacs(df):
    for _, row in df.iterrows():

        afiliacao = (
            row.get("Afiliacao")
            or row.get("Affiliation")
            or row.get("Termo_de_Busca")
            or row.get("Termo de busca")
            or row.get("termo_de_busca")
            or row.get("Busca")
            or ""
        )

        Artigo.objects.create(
            origem="lilacs",
            pmid=row.get("ID") or row.get("id_lilacs") or "",
            titulo=row.get("Title") or row.get("Titulo"),
            autores=row.get("Authors") or "",
            data_publicacao=None,
            link=row.get("URL"),
            resumo=row.get("Resumo") or "",
            afiliacao=row.get("Afiliação") or "",
            termo_de_busca=row.get("termo_de_busca") or "",
        )

def importar_scielo(df):
    for _, row in df.iterrows():

        afiliacao = (
            row.get("Afiliacao")
            or row.get("Affiliation")
            or row.get("Termo_de_Busca")
            or row.get("Termo de busca")
            or row.get("termo_de_busca")
            or row.get("Busca")
            or ""
        )
        
        Artigo.objects.create(
            origem="scielo",
            pmid="",
            titulo=row.get("Titulo"),
            autores=row.get("Autores"),
            data_publicacao=None,
            link=row.get("Link"),
            resumo=row.get("Resumo") or "",
            afiliacao=row.get("Afiliação") or "",
            termo_de_busca=row.get("termo_de_busca") or "",
        )


def importar_pubmed(df):
    for _, row in df.iterrows():

        afiliacao = (
            row.get("Afiliacao")
            or row.get("Affiliation")
            or row.get("Termo_de_Busca")
            or row.get("Termo de busca")
            or row.get("termo_de_busca")
            or row.get("Busca")
            or ""
        )

        Artigo.objects.create(
            origem="pubmed",
            pmid=row.get("PMID"),
            titulo=row.get("Titulo") or row.get("Title"),
            autores=row.get("Authors"),
            data_publicacao=None,  # PubMed CSV normalmente não tem data exata
            link=row.get("Link"),
            resumo=row.get("Resumo") or "",
            afiliacao=row.get("Afiliacao") or row.get("Affiliation") or "",
            termo_de_busca=row.get("termo_de_busca") or "",
        )

def importar_capes(df):
    for _, row in df.iterrows():

        afiliacao = (
            row.get("Afiliacao")
            or row.get("Affiliation")
            or row.get("Termo_de_Busca")
            or row.get("Termo de busca")
            or row.get("termo_de_busca")
            or row.get("Busca")
            or ""
        )

        Artigo.objects.create(
            origem="capes",
            pmid=row.get("DOI") or "",
            titulo=row.get("Titulo"),
            autores=row.get("Autores"),
            data_publicacao=None,
            link=row.get("Link"),
            resumo=row.get("Resumo") or "",
            afiliacao=row.get("Afiliação") or "",
            termo_de_busca=row.get("termo_de_busca") or "",
        )
