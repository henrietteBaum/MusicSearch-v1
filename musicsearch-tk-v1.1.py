"""
Docstring for musicsearch-tk-v1.1
GUI with two frames (search and results).
Font and font size have been adjusted.
The results are displayed in a label element.

"""

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import requests

BASE_URL = "https://itunes.apple.com/search"



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tk-MusicSearch")
        self.geometry("1200x800")

        self.app_heading = ttk.Label(
            self,
            text="Search for music terms",
            font=("Ubuntu", 30)
        )
        self.app_heading.pack(pady=20)

        self.result_frame = ResultFrame(self)
        self.search_frame = SearchFrame(self, self.result_frame)


class SearchFrame(ttk.Frame):
    """Input and search-button"""

    def __init__(self, master, result_frame):
        super().__init__(master)
        self.result_frame = result_frame
        
        self.search_term = tk.StringVar()

        search_entry = ttk.Entry(
            self,
            textvariable=self.search_term,
            width=20,
            font=("Carlito", 20)
        )
        search_entry.pack(pady=20)

        search_btn = ttk.Button(
            self, 
            text="Search",
            command=self.search
        )
        search_btn.pack(pady=20)

        self.search_term_lbl = ttk.Label(self, textvariable=self.search_term)
        self.search_term_lbl.pack(pady=20)

        self.pack(pady=20)

    def search(self):
        term = self.search_term.get().strip()
        if not term:
            showinfo("Info", "Bitte einen Suchbegriff eingeben")
            return
            
        self.result_frame.perform_search(term)


class ResultFrame(ttk.Frame):
    """Show API-results"""

    def __init__(self, master):
        super().__init__(master)

        self.result_lbl = ttk.Label(
            self, 
            text=("Results come here..."),
            justify="left",
            font=("Carlito", 14)
        )
        self.result_lbl.pack(pady=20)
        self.pack(pady=20)

    def perform_search(self, term):
        showinfo(title="Info", message=(f"Searching for: {term}"))

        payload = {
            "term": term,
            "entity": "album",
            "limit": 5
            }

        try:
            response = requests.get(BASE_URL, params=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            self.result_lbl.config(text=f"Error on request:\n{exc}")
            return
        
        if data.get("resultCount", 0) == 0:
            self.result_lbl.config(text="No results found.")
            return

        result_count = data["resultCount"]

        output_lst  = []
        output_lst.append(f'Results found for term "{term}": {result_count}\n')

        for result in data["results"]:
            artist = result["artistName"]
            album = result["collectionName"]
            tracks = result["trackCount"]

            output_lst.append(f"{artist} – {album} (Tracks: {tracks})")

        output_text = "\n".join(output_lst) #if output_lst else "Keine Ergebnisse gefunden."         
        
        self.result_lbl.configure(text=output_text)
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
