"""
Docstring for musicsearch-tk v1.3
Show the search results from Label to ScrolledText,
search history added inside a Label.
"""

import tkinter as tk
from tkinter.messagebox import showerror
import customtkinter as ctk
import requests

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(3.0)
ctk.set_window_scaling(1.8)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tk-MusicSearch")
        self.geometry("1300x1100")

        app_heading = ctk.CTkLabel(
            self,
            text="Search for music terms",
            font=("Ubuntu", 32),
            text_color="orange"
            )
        app_heading.pack(pady=20)

        # Scrollable container for content
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Enable mouse wheel scrolling
        self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind_all("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.scrollable_frame.bind_all("<Button-5>", self._on_mousewheel)  # Linux scroll down

        self.result_frame = ResultFrame(self.scrollable_frame)
        self.search_frame = SearchFrame(self.scrollable_frame, self.result_frame)
    
    def _on_mousewheel(self, event):
        # Windows/MacOS: event.delta (positive=up, negative=down)
        # Linux: event.num (4=up, 5=down)
        if event.num == 4 or event.delta > 0:
            self.scrollable_frame._parent_canvas.yview_scroll(-3, "units")
        elif event.num == 5 or event.delta < 0:
            self.scrollable_frame._parent_canvas.yview_scroll(3, "units")


class SearchFrame(ctk.CTkFrame):
    """Input and search-button"""

    def __init__(self, master, result_frame):
        super().__init__(master)
        self.result_frame = result_frame
        
        self.search_term = tk.StringVar()
        self.search_history = tk.StringVar(value="Search history: ")
        self.result_limit = tk.StringVar(value="5")

        self.entry_widget = ctk.CTkEntry(
            self,
            textvariable=self.search_term,
            width=300,
            font=("Carlito", 18),
            placeholder_text="Enter search term..."
        )
        self.entry_widget.focus()
        self.entry_widget.pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Results to display (or 'all'):",
            font=("Carlito", 16)
        ).pack(pady=5)

        self.limit_widget = ctk.CTkEntry(
            self,
            textvariable=self.result_limit,
            width=80,
            font=("Carlito", 16)
        )
        self.limit_widget.pack(pady=5)

        ctk.CTkButton(
            self, 
            text="Search",
            font=("Carlito", 18),
            command=self.search,
            width=150,
            height=50,
            fg_color="orange",      # Button-Hintergrund (Hex oder Name wie "orange", "green")
            hover_color="#FF8C42",
            text_color="black"
       ).pack(pady=20)

        ctk.CTkLabel(
            self,
            textvariable=self.search_history,
            font=("Carlito", 16)
        ).pack(pady=20)

        self.pack(pady=20, padx=20, fill="both")

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


class ResultFrame(ctk.CTkFrame):
    """Show API-results"""

    def __init__(self, master):
        super().__init__(master)

        # Text for results output:
        self.result_txt = ctk.CTkTextbox(
            self,
            font=("Carlito", 16),
            wrap="word",
            state="normal"
        )
        self.result_txt.pack(pady=20, fill="both", expand=True, padx=20)
        self.result_txt.insert("1.0", "Results come here ...")

        self.pack(pady=20, padx=20, fill="both")

    def perform_search(self, term, limit=5):
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
            self._show_error(exc)
            return
        
        result_count = data["resultCount"]
        output_lst = []
        output_lst.append(f'Results found for term "{term}": {result_count}\n')

        for result in data["results"]:
            artist = result["artistName"]
            album = result["collectionName"]
            tracks = result["trackCount"]
            output_lst.append(f"{artist} – {album} (Tracks: {tracks})")

        output_text = "\n".join(output_lst) if output_lst else "No results found."
        
        # Update CTkTextbox (no state lock needed)
        self.result_txt.delete("1.0", "end")
        self.result_txt.insert("1.0", output_text)

    def _show_error(self, exc):
        self.result_txt.delete("1.0", "end")
        self.result_txt.insert("1.0", f"Error on request:\n{str(exc)}")
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
