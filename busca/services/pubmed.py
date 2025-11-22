import requests
from bs4 import BeautifulSoup
from ..utils.filtros import pertence_ao_hc

def buscar_pubmed(termo):
    artigos = []
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + termo.replace(" ", "+")

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    resultados = soup.select(".docsum-content")

    for r in resultados:
        titulo_el = r.select_one(".docsum-title")
        if not titulo_el:
            continue

        titulo = titulo_el.get_text(strip=True)
        link = "https://pubmed.ncbi.nlm.nih.gov" + titulo_el["href"]

        # pegando a página do artigo para extrair afiliacao
        artigo_page = requests.get(link)
        artigo_soup = BeautifulSoup(artigo_page.text, "html.parser")

        afiliacao_el = artigo_soup.select_one(".affiliations")
        afiliacao = afiliacao_el.get_text(" ", strip=True) if afiliacao_el else ""

        # aplicar filtro HC-UFPE
        if not pertence_ao_hc(afiliacao):
            continue

        artigos.append({
            "titulo": titulo,
            "link": link,
            "afiliacao": afiliacao
        })

    return artigos
