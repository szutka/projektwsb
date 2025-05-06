import tkinter as tk
from io import BytesIO
import requests
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from imagesfetcher import fetchNASAimages


class NASAimages:
    def __init__(self):
        self.api_url = "https://images-api.nasa.gov/search"

    def pobierzZdjecia(self, query):
        params = {'q': query}
        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Nie można pobrać danych, kod: {response.status_code}")

    def showResults(self, data, limit=9):
        elements = data.get("collection", {}).get("items", [])
        if not elements:
            print("Nie znaleziono wyników")
            return []

        results = []
        for element in elements[:limit]:
            data_element = element.get("data", [])
            links = element.get("links", [])

            title = data_element[0].get("title", "Brak tytułu") if data_element else "Brak tytułu"
            link = links[0].get("href", "Brak linku") if links else "Brak linku"

            results.append((title, link))
        return results


def showImageFromUrl(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((400, 400))

        top = tk.Toplevel(bg="black")
        top.title("Podgląd")

        border_frame = tk.Frame(top, bg="green", padx=5, pady=5)
        border_frame.pack(padx=20, pady=20)

        inner_frame = tk.Frame(border_frame, bg="black")
        inner_frame.pack()

        tk_img: PhotoImage = ImageTk.PhotoImage(img)
        label = tk.Label(inner_frame, image=tk_img, bg="black")
        label.image = tk_img
        label.pack()
    else:
        print("Nie udało się załadować obrazka")


def loadThumbnail(url, label, size=(100, 100)):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail(size)
            tk_img = ImageTk.PhotoImage(img)
            label.configure(image=tk_img, bg="black")
            label.image = tk_img
    except Exception as e:
        print(f"Błąd podczas ładowania zdjęcia: {e}")


def search():
    query = entry.get()
    for widget in output_frame.winfo_children():
        widget.destroy()

    global loading_label
    loading_label = tk.Label(output_frame, text="Ładowanie...", bg="black", fg="green")
    loading_label.pack(pady=10)
    root.update_idletasks()

    fetcher = NASAimages()

    try:
        data = fetcher.pobierzZdjecia(query)
        results = fetcher.showResults(data)

        if loading_label and loading_label.winfo_exists():
            loading_label.destroy()

        if not results:
            no_results = tk.Label(output_frame, text="Nie znaleziono", bg="black", fg="green")
            no_results.pack(pady=10)
            text_log.insert("end", f"Brak wyników dla: {query}\n")
            text_log.see("end")
            return

        # Konfiguracja siatki 3x3
        for col in range(3):
            output_frame.columnconfigure(col, weight=1)
        for row in range(3):
            output_frame.rowconfigure(row, weight=1)

        for i, (title, link) in enumerate(results):
            row = i // 3
            column = i % 3

            result_frame = tk.Frame(output_frame, bg="black", bd=2, relief="groove", padx=5, pady=5)
            result_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

            thumbnail_label = tk.Label(result_frame, bg="black", fg="green")
            thumbnail_label.pack(fill="both", expand=True, pady=5)
            loadThumbnail(link, thumbnail_label)

            text_button_frame = tk.Frame(result_frame, bg="black")
            text_button_frame.pack(fill="both", expand=True)

            title_label = tk.Label(text_button_frame, text=f"{i+1}. {title}", anchor="w", justify="left", bg="black", fg="green")
            title_label.pack(fill="x")

            button = tk.Button(
                text_button_frame,
                text="Pokaż pełny obraz",
                command=lambda url=link: showImageFromUrl(url),
                bg="black",
                fg="green",
                activebackground="green",
                activeforeground="black",
                highlightbackground="green",
            )
            button.pack(pady=5)

        text_log.insert("end", f"Sukces, pobrano {query}\n")
        text_log.see("end")

    except Exception as e:
        if loading_label and loading_label.winfo_exists():
            loading_label.destroy()
        text_log.insert("end", f"Błąd: {e}\n")
        text_log.see("end")


root = tk.Tk()
root.title("NASAimages")
root.geometry("1000x800")
root.config(bg="black")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=2)

input_frame = tk.Frame(root, bg="black")
input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

tk.Label(input_frame, text="Podaj zapytanie: ", bg="black", fg="green").pack(side="left", padx=5)
entry = tk.Entry(input_frame, width=40, bg="black", fg="green", insertbackground="green")
entry.pack(side="left", padx=5)
tk.Button(input_frame, text="Szukaj", command=search, bg="black", fg="green", highlightbackground="green").pack(side="left", padx=5)

output_frame = tk.LabelFrame(root, text="Wyniki", bg="black", fg="green", highlightbackground="green", highlightcolor="green", bd=2)
output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
output_frame.grid_propagate(False)  # zapobiega zmianie rozmiaru przez zawartość

log_frame = tk.LabelFrame(root, text="Logi", bg="black", fg="green", highlightbackground="green", highlightcolor="green", bd=2)
log_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

loading_label = None

text_log = tk.Text(log_frame, width=40, height=30, bg="black", fg="green", insertbackground="green")
text_log.pack(fill="both", expand=True)

root.mainloop()
