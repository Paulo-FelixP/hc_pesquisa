# busca/utils/filtros.py
import unicodedata
import re
import logging

logger = logging.getLogger(__name__)

PADROES_BRUTOS = [
    "hospital das clinicas",
    "hospital das clínicas",
    "hospital das clinicas ufpe",
    "hospital das clínicas ufpe",
    "hc ufpe",
    "hc-ufpe",
    "hc",
    "hc ebserh",
    "ebserh",
    "hospital das clinicas da ufpe",
    "hospital das clínicas da ufpe",
    "universidade federal de pernambuco",
    "ufpe",
    "clinics hospital of pernambuco federal university",
    "hospital das clinicas pernambuco",
    "hospital das clínicas pernambuco",
]

# normaliza padrões (remove acentos e espaço duplicado)
def _normalizar_simples(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.replace("-", " ").replace("–", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

PADROES = [_normalizar_simples(p) for p in PADROES_BRUTOS]

# Compila regexes com limites de palavra para reduzir falsos positivos
PADROES_REGEX = [re.compile(r"\b" + re.escape(p) + r"\b", re.IGNORECASE) for p in PADROES]


def strip_html_simple(text: str) -> str:
    """Remove tags HTML simples para evitar que <sup>, <em>, etc, quebrem a busca."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def pertence_ao_hc(texto: str, debug: bool = False) -> bool:
    """
    Retorna True se detectar padrões conhecidos do HC/UFPE no texto.
    Use debug=True para logar a verificação (útil em console de desenvolvimento).
    """
    if not texto:
        if debug:
            logger.debug("[pertence_ao_hc] texto vazio")
        return False

    # limpa HTML, normaliza
    texto_limpo = strip_html_simple(texto)
    texto_norm = _normalizar_simples(texto_limpo)

    # checa regexes
    for i, rx in enumerate(PADROES_REGEX):
        if rx.search(texto_norm):
            if debug:
                logger.debug(f"[pertence_ao_hc] MATCH padrao='{PADROES[i]}' texto_preview='{texto_norm[:160]}'")
            return True

    if debug:
        logger.debug(f"[pertence_ao_hc] no match preview='{texto_norm[:160]}'")
    return False
