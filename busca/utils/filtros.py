import re

PADROES_HC = [
    "Hospital das Clinicas - UFPE",
    "Hospital das Clínicas - UFPE",
    "Hospital das Clinicas da UFPE",
    "Hospital das Clínicas da UFPE",
    "HC UFPE",
    "HC EBSERH",
    "Universidade Federal de Pernambuco hospital",
    "Hospital das Clinicas - Universidade Federal de Pernambuco",
    "Hospital das Clínicas - Universidade Federal de Pernambuco",
    "Hospital das Clinicas da Universidade Federal de Pernambuco",
    "Hospital das Clínicas da Universidade Federal de Pernambuco",
    "Hospital das Clinicas, Universidade Federal de Pernambuco",
    "Hospital das Clínicas, Universidade Federal de Pernambuco",
    "Hospital das Clinicas de Pernambuco",
    "Hospital das Clínicas de Pernambuco",
    "Hospital das Clinicas de Pernambuco-Empresa Brasileira de Servicos Hospitalares",
    "Hospital das Clínicas de Pernambuco-Empresa Brasileira de Serviços Hospitalares",
    "Hospital das Clinicas/EBSER-UFPE",
    "Hospital das Clínicas/EBSER-UFPE",
    "Clinics Hospital of Pernambuco Federal University",
    "hospital das clínicas",
    "hc-ufpe",
    "universidade federal de pernambuco",
    "ufpe",
    "hc ufpe",
    "hospital das clinicas ufpe",
]

def pertence_ao_hc(texto: str) -> bool:
    """
    Retorna True se qualquer padrão conhecido do HC-UFPE estiver no texto.
    """
    if not texto:
        return False

    texto = texto.lower().strip()

    return any(p in texto for p in PADROES_HC)
