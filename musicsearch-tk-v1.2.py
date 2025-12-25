"""
Docstring for tk-music-search.gui_main_v-0.2
Change the Widget to show the search results from Label to ScrolledText.
The results now can be copied and reused.

"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter.messagebox import showerror
import requests


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tk-MusicSearch")
        self.geometry("1700x1200")

        app_heading = tk.Label(
            self,
            text="Search for music terms",
            font=("Ubuntu", 28),
            fg="darkorange"
            )
        app_heading.pack(pady=20)

        self.result_frame = ResultFrame(self)
        self.search_frame = SearchFrame(self, self.result_frame)


class SearchFrame(ttk.Frame):
    """Input and search-button"""

    def __init__(self, master, result_frame):
        super().__init__(master)
        self.result_frame = result_frame
        
        self.search_term = tk.StringVar()
        self.search_history = tk.StringVar(value="Search history: ")
        self.result_limit = tk.StringVar(value="5")

        self.entry_widget = ttk.Entry(
            self,
            textvariable=self.search_term,
            width=20,
            font=("Carlito", 16)
        )
        self.entry_widget.focus()
        self.entry_widget.pack(pady=20)

        ttk.Label(
            self,
            text="Results to display (or 'all'):"
        ).pack(pady=5)

        self.limit_widget = ttk.Entry(
            self,
            textvariable=self.result_limit,
            width=10,
            font=("Carlito", 14)
        )
        self.limit_widget.pack(pady=5)

        tk.Button(
            self, 
            text="Search",
            font=("Carlito", 14),
            command=self.search
        ).pack(pady=20)

        ttk.Label(
            self,
            textvariable=self.search_history
        ).pack(pady=20)


        self.pack(pady=20)

    def search(self):
        term = self.search_term.get().strip()
        if not term:
            showerror("Info", "Please enter a search term!")
            return

        # Limit validieren
        limit_str = self.result_limit.get().strip().lower()
        if limit_str == "all":
            limit = 200  # iTunes API Maximum
        else:
            try:
                limit = int(limit_str)
                if limit < 1:
                    showerror("Info", "Limit must be >= 1 !")
                    return
            except ValueError:
                showerror("Info", "Limit be a number or 'all' sein!")
                return

        # Suchhistorie aktualisieren
        current_history = self.search_history.get()
        if current_history == "Search history: ":
            new_history = f"Search history: {term}"
        else:
            new_history = f"{current_history} | {term}"
        self.search_history.set(new_history)

        self.entry_widget.delete(0, tk.END)
            
        self.result_frame.perform_search(term, limit)


class ResultFrame(ttk.Frame):
    """Show API-results"""

    def __init__(self, master):
        super().__init__(master)

        # Text for results output:
        self.result_txt = scrolledtext.ScrolledText(
            self,
            width=80,
            height=10,
            wrap="word",
            font=("Carlito", 14),
            spacing2=6
        )
        self.result_txt.pack(pady=20, fill="x", expand=True)

        self.result_txt.configure(state="normal")
        self.result_txt.insert("1.0", "Results com here ...")
        self.result_txt.configure(state="disabled")

        self.pack(pady=20)

    def perform_search(self, term, limit=5):
        #showinfo(title="Info", message=(f"Searching for: {term}"))

        BASE_URL = "https://itunes.apple.com/search"

        payload = {
            "term": term,
            "entity": "album",
            "limit": limit
            }

        try:
            response = requests.get(BASE_URL, params=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            self.result_txt.config(text=("Error on request:\n{str(exc)}"))
            return
        

        result_count = data["resultCount"]

        output_lst  = []
        output_lst.append(f'Resuls found for term "{term}": {result_count}\n')

        for result in data["results"]:
            artist = result["artistName"]
            album = result["collectionName"]
            tracks = result["trackCount"]
            output_lst.append(f"{artist} – {album} (Tracks: {tracks})")

        output_text = "\n".join(output_lst) if output_lst else "Keine Ergebnisse gefunden."         
        
        # update textfield
        self.result_txt.configure(state="normal")   # make editable
        self.result_txt.delete("1.0", "end")        # delete content
        self.result_txt.insert("1.0", output_text)  # add new content
        self.result_txt.configure(state="disabled") # close


        def _show_error(self, exc):
            self.result_txt.configure(state="normal")
            self.result_txt.delete("1.0", "end")
            self.result_txt.insert("1.0", f"Error on request:\n{exc}")
            self.result_txt.configure(state="disabled")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
