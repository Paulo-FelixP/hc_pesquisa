import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://search.scielo.org/?q={query}&lang=pt&count=50"


def buscar_scielo_raw(query: str) -> str:
    url = BASE_URL.format(query=query)
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text


def limpar_periodico(texto: str) -> str:
    # Remove blocos inúteis
    lixo = [
        "Métricas do periódico",
        "Sobre o periódico",
        "SciELO Analytics",
    ]
    for l in lixo:
        texto = texto.replace(l, "")

    return " ".join(texto.split()).strip()


def buscar_scielo(query: str, max_results=10):
    html = buscar_scielo_raw(query)
    soup = BeautifulSoup(html, "html.parser")

    resultados = []

    artigos = soup.select(".item")

    for art in artigos[:max_results]:

        # TÍTULO (texto dentro do <a>)
        a_tag = art.select_one(".line a")
        titulo = a_tag.get_text(strip=True) if a_tag else "Sem título"

        # LINK
        link = a_tag["href"] if a_tag else ""

        # AUTORES
        autores_tag = art.select_one(".authors")
        autores = autores_tag.get_text(" ", strip=True) if autores_tag else "Sem autores"

        # PERIÓDICO (limpo)
        periodico_tag = art.select_one(".source")
        periodico = limpar_periodico(periodico_tag.get_text(" ", strip=True)) if periodico_tag else "Sem periódico"

        # ANO — extrair 4 dígitos
        ano = "Sem ano"
        achou_ano = re.search(r"(\d{4})", periodico)
        if achou_ano:
            ano = achou_ano.group(1)

        resultados.append({
            "titulo": titulo,
            "autores": autores,
            "ano": ano,
            "periodico": periodico,
            "link": link,
            "origem": "Scielo",
            "fonte": "Scielo",
        })

    return resultados
