import requests
from datetime import datetime

class LilacsService:

    BASE_URL = "https://fi-admin-api.bvsalud.org/api/resource/search/"

    @staticmethod
    def buscar_lilacs(query: str, data_inicio=None, data_fim=None, limit: int = 5):
        try:
            params = {
                "q": query,
                "page_size": limit
            }

            # -----------------------------
            # 📌 Filtro de período
            # -----------------------------
            if data_inicio or data_fim:
                
                # Formatar para YYYYMMDD
                def fmt(d):
                    return datetime.strptime(d, "%Y-%m-%d").strftime("%Y%m%d")

                inicio = fmt(data_inicio) if data_inicio else "00000000"
                fim = fmt(data_fim) if data_fim else "99999999"

                params["fq"] = f"created_date:[{inicio} TO {fim}]"

            resp = requests.get(
                LilacsService.BASE_URL,
                params=params,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            resp.raise_for_status()
            data = resp.json()

            docs = data["diaServerResponse"][0]["response"].get("docs", [])

            resultados = []

            for d in docs:
                titulo = d.get("title", "")
                resumo = d.get("abstract", "")

                links = d.get("link", [])
                link = links[0] if links else ""

                resultados.append({
                    "titulo": titulo.strip() if titulo else "",
                    "link": link.strip() if link else "",
                    "resumo": resumo.strip() if resumo else "",
                    "origem": "Lilacs",
                })

            return resultados

        except Exception as e:
            print("Erro LILACS JSON:", e)
            return []
