import requests
from bs4 import BeautifulSoup
from ..utils.filtros import pertence_ao_hc

def buscar_lilacs(termo):
    artigos = []
    url = f"https://pesquisa.bvsalud.org/portal/?q={termo.replace(' ', '+')}"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    resultados = soup.select(".record")

    for r in resultados:
        titulo_el = r.select_one(".title a")
        if not titulo_el:
            continue

        titulo = titulo_el.get_text(strip=True)
        link = titulo_el["href"]

        artigo_page = requests.get(link)
        artigo_soup = BeautifulSoup(artigo_page.text, "html.parser")

        afiliacao_el = artigo_soup.select_one("div.affiliation")
        afiliacao = afiliacao_el.get_text(" ", strip=True) if afiliacao_el else ""

        if not pertence_ao_hc(afiliacao):
            continue

        artigos.append({
            "titulo": titulo,
            "link": link,
            "afiliacao": afiliacao
        })

    return artigos
