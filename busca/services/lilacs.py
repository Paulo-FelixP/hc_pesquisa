import requests

class LilacsService:

    BASE_URL = "https://pesquisa.bvsalud.org/api/"

    @staticmethod
    def buscar_lilacs(query: str, limit: int = 5):
        try:
            params = {
                "site": "lilacs",
                "q": query,
                "lang": "pt",
                "format": "json",
                "count": limit,
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }

            response = requests.get(
                LilacsService.BASE_URL,
                params=params,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            results = []

            for item in data.get("result", []):
                title = item.get("ti", [""])[0] if isinstance(item.get("ti"), list) else item.get("ti", "")
                link = item.get("ur", [""])[0] if isinstance(item.get("ur"), list) else item.get("ur", "")
                summary = item.get("ab", [""])[0] if item.get("ab") else ""

                results.append({
                    "titulo": title,
                    "link": link,
                    "resumo": summary
                })

            return results

        except Exception as e:
            print(f"Erro LILACS/BVS: {e}")
            return []
