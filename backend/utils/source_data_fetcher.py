import requests


class SourceDataFetcher:
    def __init__(self, urls):
        self.urls = urls

    def fetch_data(self):
        try:
            response = requests.get(self.urls)
            if response.status_code == 200:
                return response.json()
            else:
                print(
                    "Error al obtener los datos. Código de estado:",
                    response.status_code,
                )
                return None
        except requests.exceptions.RequestException as e:
            print("Error de conexión:", e)
            return None
