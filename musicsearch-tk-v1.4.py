"""
Docstring for tk-music-search.gui_main_v-0.2
Show the search results from Label to ScrolledText,
search history added inside a Label.
Change layout to grid for better spacing.
Implement mouse wheel scrolling and Ctrl+Scroll zooming.
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
        self.geometry("1300x1000")
        
        # Track current scaling for zoom
        self.current_scaling = 1.0

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
        
        # Enable Ctrl+Scroll zoom
        self.scrollable_frame.bind_all("<Control-MouseWheel>", self._on_zoom)
        self.scrollable_frame.bind_all("<Control-Button-4>", self._on_zoom)  # Linux zoom in
        self.scrollable_frame.bind_all("<Control-Button-5>", self._on_zoom)  # Linux zoom out

        self.result_frame = ResultFrame(self.scrollable_frame)
        self.search_frame = SearchFrame(self.scrollable_frame, self.result_frame)
    
    def _on_mousewheel(self, event):
        # Windows/MacOS: event.delta (positive=up, negative=down)
        # Linux: event.num (4=up, 5=down)
        if event.num == 4 or event.delta > 0:
            self.scrollable_frame._parent_canvas.yview_scroll(-3, "units")
        elif event.num == 5 or event.delta < 0:
            self.scrollable_frame._parent_canvas.yview_scroll(3, "units")
    
    def _on_zoom(self, event):
        # Zoom in/out with Ctrl+Scroll
        # Limit zoom between 0.5x and 3.0x
        if event.num == 4 or event.delta > 0:  # Zoom in
            self.current_scaling *= 1.1
        elif event.num == 5 or event.delta < 0:  # Zoom out
            self.current_scaling *= 0.9
        
        # Clamp scaling
        self.current_scaling = max(0.5, min(3.0, self.current_scaling))
        ctk.set_widget_scaling(self.current_scaling)


class SearchFrame(ctk.CTkFrame):
    """Input and search-button"""

    def __init__(self, master, result_frame):
        super().__init__(master)
        self.result_frame = result_frame
        
        self.search_term = tk.StringVar()
        self.search_history = tk.StringVar(value="Search history: ")
        self.result_limit = tk.StringVar(value="5")

        # Configure grid: 2 columns (left for search, right for limit+button)
        self.grid_columnconfigure(1, weight=1)  # Search entry expands
        # Give rows 1 and 2 weight so the button can center vertically across them
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

         # Row 3: Search history
        ctk.CTkLabel(
            self,
            textvariable=self.search_history,
            font=("Carlito", 16)
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="w")

        # Row 0: Search term label + entry (full width)
        ctk.CTkLabel(
            self,
            text="Search term:",
            font=("Carlito", 16)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_widget = ctk.CTkEntry(
            self,
            textvariable=self.search_term,
            width=200,
            font=("Carlito", 18),
        )
            #placeholder_text="Enter search term..."
        
        # Do not force focus here (can hide placeholder); use manual placeholder handling
        self.placeholder_text = "Enter search term..."
        # If placeholder param isn't showing (older CTk), provide a fallback
        try:
            # if entry supports get() and is empty, insert placeholder
            if not self.entry_widget.get():
                self.entry_widget.insert(0, self.placeholder_text)
                self._placeholder_active = True
            else:
                self._placeholder_active = False
        except Exception:
            self._placeholder_active = False

        # Bind focus events to manage placeholder fallback
        self.entry_widget.bind("<FocusIn>", self._clear_placeholder)
        self.entry_widget.bind("<FocusOut>", self._restore_placeholder)
        self.entry_widget.bind("<Return>", lambda event: self.search()) 
        self.entry_widget.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        # Row 2: Limit label + entry (stacked under search term)
        ctk.CTkLabel(
            self,
            text="Results to display:",
            font=("Carlito", 16)
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.limit_widget = ctk.CTkEntry(
            self,
            textvariable=self.result_limit,
            width=150,
            font=("Carlito", 16)
        )
        self.limit_widget.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

        # Row 1-2: Search button (below limit entry)
        ctk.CTkButton(
            self, 
            text="Search",
            font=("Carlito", 18),
            command=self.search,
            width=110,
            height=50,
            fg_color="orange",
            hover_color="#FF8C42",
            text_color="black"
        ).grid(row=1, column=2, rowspan=2, padx=10, pady=10)

       
        self.pack(pady=10, padx=20, fill="both")

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

    # Placeholder handlers (fallback for CTk versions or scaling issues)
    def _clear_placeholder(self, event):
        try:
            if getattr(self, "_placeholder_active", False):
                self.entry_widget.delete(0, "end")
                self._placeholder_active = False
        except Exception:
            pass

    def _restore_placeholder(self, event):
        try:
            if not self.entry_widget.get().strip():
                self.entry_widget.insert(0, getattr(self, "placeholder_text", ""))
                self._placeholder_active = True
        except Exception:
            pass


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
