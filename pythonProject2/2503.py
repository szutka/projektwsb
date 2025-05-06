#https://images-api.nasa.gov/search?q=Supernova
import json

import requests


def fetch_nasa_images(query):
    url = "https://images-api.nasa.gov/search"

    params_query = {
        'q': query
    }

    response = requests.get(url, params=params_query)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"nie udalo sie pobrac danych, kod statusu: {response.status_code}")

data = fetch_nasa_images('sun')
print(json.dumps(data, indent=4))

def main():
    query = input("Podaj zapytanie: ") #wyswietla terminal z trescia zadania do wykonania
    try:
        data = fetch_nasa_images(query)
        items = data.get("collection", {}).get("items", [])

        if not items:
            print("brak wynikow dla podanego zapytania")
            return

        for item in items[:5]:
            item_data = item.get("data", [])

            if item_data:
                title = item_data[0].get("title", "brak tytulu")
                print(f"Tytul: {title}")


            links = item.get("links", [])

            if links:
                href = links[0].get("href", "Brak linku")
                print(f"Link: {href}")

            print("-" * 40)

    except Exception as e:
        print(f"wystapil blad: {e}")

if __name__ == '__main__':
    main()



class FetchNasaImage:
    def __init__(self, base_url="https://images-api.nasa.gov/search"):
        self.base_url = base_url

    def FetchNasaImage(self, query):
        params_query = {'q': query}
        response = requests.get(self.base_url, params=params_query)
dlaczego te funkcje maja byc w obiekcie