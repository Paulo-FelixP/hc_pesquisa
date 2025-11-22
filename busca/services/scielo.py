import requests
from bs4 import BeautifulSoup
from ..utils.filtros import pertence_ao_hc

def buscar_scielo(termo):
    artigos = []
    url = f"https://search.scielo.org/?q={termo.replace(' ', '+')}"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    resultados = soup.select("div.item")

    for item in resultados:
        titulo_el = item.select_one("a.title")
        if not titulo_el:
            continue

        link = titulo_el["href"]
        titulo = titulo_el.get_text(strip=True)

        artigo_page = requests.get(link)
        artigo_soup = BeautifulSoup(artigo_page.text, "html.parser")

        afiliacao_el = artigo_soup.select_one("div.aff span")
        afiliacao = afiliacao_el.get_text(" ", strip=True) if afiliacao_el else ""

        if not pertence_ao_hc(afiliacao):
            continue

        artigos.append({
            "titulo": titulo,
            "link": link,
            "afiliacao": afiliacao
        })

    return artigos
