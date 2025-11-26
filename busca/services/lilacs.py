import requests

class LilacsService:

    BASE_URL = "https://fi-admin-api.bvsalud.org/api/resource/search/"

    @staticmethod
    def buscar_lilacs(query: str, limit: int = 5):
        try:
            params = {
                "q": query,
                "page_size": limit
            }

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

                # O campo "link" sempre vem como lista
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
