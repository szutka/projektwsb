import tkinter as tk  # import tkinter do gui
from io import BytesIO  # do przetwarzania obrazkow w pamieci
import requests  # do pobierania danych z internetu
from PIL import Image, ImageTk  # do obslugi obrazow i integracji z tkinter

class NASAImages:
    def __init__(self):
        self.api_url = "https://images-api.nasa.gov/search"  # api nasa do wyszukiwania obrazow

    def fetch_images(self, query):
        params = {'q': query}  # parametry zapytania z kluczem 'q'
        response = requests.get(self.api_url, params=params)  # wyslij zapytanie get do api
        if response.status_code == 200:  # jesli odpowiedz ok
            return response.json()  # zwroc dane w formacie json
        else:
            # rzuc wyjatek gdy status inny niz 200
            raise Exception(f"nie można pobrać danych,kod:{response.status_code}")

    def extract_results(self, data, limit=9):
        # wyciagnij liste elementow z jsona
        elements = data.get("collection", {}).get("items", [])
        if not elements:  # sprawdz czy sa elementy
            return []  # zwroc pusta liste jesli brak

        results = []  # lista na wyniki
        for element in elements[:limit]:  # ogranicz do limitu wynikow
            data_element = element.get("data", [])
            links = element.get("links", [])

            # pobierz tytul jesli jest, inaczej tekst domyslny
            title = data_element[0].get("title", "brak tytułu") if data_element else "brak tytułu"
            # pobierz link do obrazka lub placeholder
            link = links[0].get("href", "brak linku") if links else "brak linku"

            results.append((title, link))  # dodaj tuple (tytul,link) do wynikow
        return results  # zwroc liste wynikow

class ImageLoader:
    def __init__(self, log_widget):
        self.log_widget = log_widget  # widget do wyswietlania logow

    def log(self, message):
        # dodaj wiadomosc do text widgetu i przewin do konca
        self.log_widget.insert("end", message + "\n")
        self.log_widget.see("end")

    def show_image_from_url(self, url):
        response = requests.get(url)  # pobierz obrazek z internetu
        if response.status_code == 200:  # jesli pobranie sie powiodlo
            img_data = response.content  # zawartosc obrazka w bajtach
            img = Image.open(BytesIO(img_data)).resize((600, 600))  # otworz i zmien rozmiar

            top = tk.Toplevel(bg="black")  # nowe okno do wyswietlania obrazka
            top.title("podgląd")  # tytul okna
            top.state("zoomed")  # otworz w trybie pelnoekranowym

            border_frame = tk.Frame(top, bg="green", padx=5, pady=5)  # ramka z zielona ramka
            border_frame.pack(padx=20, pady=20)  # odstepy zewnatrz ramki

            inner_frame = tk.Frame(border_frame, bg="black")  # czarna ramka w srodku
            inner_frame.pack()

            tk_img = ImageTk.PhotoImage(img)  # konwersja obrazka do formatu tkinter
            label = tk.Label(inner_frame, image=tk_img, bg="black")  # etykieta do wyswietlania
            label.image = tk_img  # zapamietaj referencje zeby obrazek sie nie usunal
            label.pack()  # umiesc etykiete w ramce
        else:
            self.log("nie udało się załadować obrazka")  # blad przy pobieraniu obrazka

    def load_thumbnail(self, url, label, size=(100, 100)):
        try:
            self.log(f"pobieranie miniatury:{url}")  # loguj rozpoczecie pobierania miniatury
            response = requests.get(url)  # pobierz obrazek
            if response.status_code == 200:  # jesli ok
                img_data = response.content
                img = Image.open(BytesIO(img_data))  # otworz obrazek
                img.thumbnail(size)  # zmien rozmiar na miniature
                tk_img = ImageTk.PhotoImage(img)  # konwersja do tkinter
                label.configure(image=tk_img, bg="black")  # ustaw obrazek w label
                label.image = tk_img  # zapamietaj referencje
                self.log("udało się, załadowano miniaturę")  # log sukcesu
            else:
                self.log(f"błąd http:{response.status_code}")  # log kod bledu http
        except Exception as e:
            self.log(f"błąd podczas ładowania miniatury:{e}")  # log wyjatku

class SearchInterface:
    def __init__(self, root):
        self.root = root  # glowne okno aplikacji
        self.root.title("nasa images")  # tytul okna
        self.root.geometry("1000x800")  # rozmiar okna
        self.style = {"bg": "black", "fg": "green"}  # definicja stylu kolorow
        self.root.config(bg=self.style["bg"])  # ustaw kolor tla glownego okna
        self.root.rowconfigure(1, weight=1)  # konfiguracja wiersza 1 na rozciagliwy
        self.root.columnconfigure(0, weight=4)  # kolumna 0 - 4 razy szersza
        self.root.columnconfigure(1, weight=1)  # kolumna 1 - mniej szeroka

        self.setup_gui()  # budowa interfejsu

        self.nasa_fetcher = NASAImages()  # obiekt do pobierania danych z api
        self.image_loader = ImageLoader(self.text_log)  # obiekt do ladowania obrazkow i logowania
        self.loading_label = None  # label pokazujacy status ladowania

    def setup_gui(self):
        input_frame = tk.Frame(self.root, bg=self.style["bg"])  # ramka na pole tekstowe i przycisk
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)  # umiesc u gory

        tk.Label(input_frame, text="podaj zapytanie:", **self.style).pack(side="left", padx=5)  # label
        self.entry = tk.Entry(input_frame, width=40, bg=self.style["bg"], fg=self.style["fg"],
                              insertbackground=self.style["fg"])  # pole tekstowe
        self.entry.pack(side="left", padx=5)
        tk.Button(input_frame, text="szukaj", command=self.search, bg=self.style["bg"], fg=self.style["fg"],
                  highlightbackground=self.style["fg"]).pack(side="left", padx=5)  # przycisk szukaj

        self.output_frame = tk.LabelFrame(self.root, text="wyniki", bg=self.style["bg"], fg=self.style["fg"],
                                          highlightbackground=self.style["fg"], bd=2)  # ramka na wyniki
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 80), pady=10)  # po lewej
        self.output_frame.grid_propagate(False)  # nie zmieniaj rozmiaru ramki automatycznie

        self.log_frame = tk.LabelFrame(self.root, text="logi", bg=self.style["bg"], fg=self.style["fg"],
                                       highlightbackground=self.style["fg"], bd=2)  # ramka na logi
        self.log_frame.grid(row=1, column=1, sticky="nsew", padx=(80, 10), pady=10)  # po prawej

        self.text_log = tk.Text(self.log_frame, width=10, height=30, bg=self.style["bg"], fg=self.style["fg"],
                                insertbackground=self.style["fg"])  # widget text do logow
        self.text_log.pack(fill="both", expand=True)

    def search(self):
        query = self.entry.get().strip()  # pobierz tekst z pola i obetnij spacje
        for widget in self.output_frame.winfo_children():
            widget.destroy()  # wyczysc poprzednie wyniki wyswietlania

        self.loading_label = tk.Label(self.output_frame, text="ładowanie...", **self.style)  # pokaz label z napisem
        self.loading_label.pack(pady=10)
        self.root.update_idletasks()  # wymusz odswiezenie GUI

        try:
            data = self.nasa_fetcher.fetch_images(query)  # pobierz dane z api nasa
            results = self.nasa_fetcher.extract_results(data)  # wyciagnij z jsona tytuly i linki

            if self.loading_label and self.loading_label.winfo_exists():
                self.loading_label.destroy()  # usun label ladowania

            if not results:
                # brak wynikow wyswietl komunikat
                tk.Label(self.output_frame, text="nie znaleziono", **self.style).pack(pady=10)
                self.text_log.insert("end", f"brak wyników dla:{query}\n")  # wpisz do logow
                self.text_log.see("end")
                return

            # konfiguruj siatke 3x3 w output_frame
            for i in range(3):
                self.output_frame.columnconfigure(i, weight=1)  # 3 kolumny rowne
                self.output_frame.rowconfigure(i, weight=1)  # 3 wiersze rowne

            for i, (title, link) in enumerate(results):  # iteruj po wynikach z numerem i
                row = i // 3  # wylicz wiersz
                column = i % 3  # wylicz kolumne

                result_frame = tk.Frame(self.output_frame, bg=self.style["bg"], bd=2, relief="groove", padx=5, pady=5)
                    # ramka pojedynczego wyniku
                result_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")  # umiesc w gridzie

                thumbnail_label = tk.Label(result_frame, bg=self.style["bg"], fg=self.style["fg"], cursor="hand2")
                    # label na miniature
                thumbnail_label.pack(fill="both", expand=True, pady=5)
                    # powiaz klikniecie etykiety z funkcja pokazujaca obrazek

                thumbnail_label.bind("<Button-1>", lambda e, url=link: self.image_loader.show_image_from_url(url))
                self.image_loader.load_thumbnail(link, thumbnail_label)  # zaladuj miniature do labela

                title_label = tk.Label(result_frame, text=f"{i+1}. {title}", anchor="w", justify="left", **self.style)
                    # etykieta tytulu
                title_label.pack(fill="x")  # wypelnij poziomo

            self.text_log.insert("end", f"sukces,pobrano:{query}\n")  # log sukcesu
            self.text_log.see("end")  # przewin log

        except Exception as e:
            if self.loading_label and self.loading_label.winfo_exists():
                self.loading_label.destroy()  # usun label ladowania w razie bledu
            self.text_log.insert("end", f"błąd:{e}\n")  # wypisz blad do logu
            self.text_log.see("end")

if __name__ == "__main__":
    root = tk.Tk()  # utworz glowne okno
    app = SearchInterface(root)  # stworz instancje aplikacji
    root.mainloop()  # uruchom petle zdarzen
