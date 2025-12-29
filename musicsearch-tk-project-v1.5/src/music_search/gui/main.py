"""GUI module - Main application window and frames."""

import tkinter as tk
from tkinter.messagebox import showerror
import customtkinter as ctk

from ..api.itunes import ITunesAPI
from ..config import AppConfig
from ..utils.constants import (
    FONT_HEADING,
    FONT_LABEL,
    FONT_ENTRY,
    FONT_BUTTON,
    FONT_TEXT,
    COLOR_BUTTON_FG,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_TEXT,
    ZOOM_MIN,
    ZOOM_MAX,
    ZOOM_STEP,
)


class App(ctk.CTk):
    """Main application window."""

    def __init__(self, config: AppConfig):
        """
        Initialize main application.

        Args:
            config: Application configuration.
        """
        super().__init__()
        self.config = config
        self.api = ITunesAPI()
        self.current_scaling = 1.0

        # Configure appearance
        ctk.set_appearance_mode(self.config.appearance)
        ctk.set_default_color_theme(self.config.theme)
        ctk.set_widget_scaling(self.config.widget_scaling)
        ctk.set_window_scaling(self.config.window_scaling)

        # Window setup
        self.title(self.config.app_title)
        self.geometry(f"{self.config.window_width}x{self.config.window_height}")

        # App heading
        app_heading = ctk.CTkLabel(
            self,
            text="Search for music terms",
            font=FONT_HEADING,
            text_color="orange",
        )
        app_heading.pack(pady=20)

        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bind scroll events
        self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind_all("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind_all("<Button-5>", self._on_mousewheel)

        # Bind zoom events
        self.scrollable_frame.bind_all("<Control-MouseWheel>", self._on_zoom)
        self.scrollable_frame.bind_all("<Control-Button-4>", self._on_zoom)
        self.scrollable_frame.bind_all("<Control-Button-5>", self._on_zoom)

        # Create frames
        self.result_frame = ResultFrame(self.scrollable_frame, self.api)
        self.search_frame = SearchFrame(
            self.scrollable_frame, self.result_frame, self.api
        )

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:
            self.scrollable_frame._parent_canvas.yview_scroll(-3, "units")
        elif event.num == 5 or event.delta < 0:
            self.scrollable_frame._parent_canvas.yview_scroll(3, "units")

    def _on_zoom(self, event):
        """Handle Ctrl+Scroll zoom."""
        if event.num == 4 or event.delta > 0:
            self.current_scaling *= ZOOM_STEP
        elif event.num == 5 or event.delta < 0:
            self.current_scaling /= ZOOM_STEP

        self.current_scaling = max(ZOOM_MIN, min(ZOOM_MAX, self.current_scaling))
        ctk.set_widget_scaling(self.current_scaling)


class SearchFrame(ctk.CTkFrame):
    """Search input frame."""

    def __init__(self, master, result_frame, api: ITunesAPI):
        """
        Initialize search frame.

        Args:
            master: Parent widget.
            result_frame: Result frame reference.
            api: iTunes API instance.
        """
        super().__init__(master)
        self.result_frame = result_frame
        self.api = api

        self.search_term = tk.StringVar()
        self.search_history = tk.StringVar(value="Search history: ")
        self.result_limit = tk.StringVar(value="5")

        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Row 0: Search history
        ctk.CTkLabel(
            self, textvariable=self.search_history, font=FONT_LABEL
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # Row 1: Search term
        ctk.CTkLabel(self, text="Search term:", font=FONT_LABEL).grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        self.entry_widget = ctk.CTkEntry(
            self,
            textvariable=self.search_term,
            width=200,
            font=FONT_ENTRY,
            placeholder_text="Enter search term...",
        )
        self.entry_widget.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        # Placeholder handling
        self.placeholder_text = "Enter search term..."
        self.entry_widget.bind("<FocusIn>", self._clear_placeholder)
        self.entry_widget.bind("<FocusOut>", self._restore_placeholder)

        # Row 2: Limit
        ctk.CTkLabel(self, text="Results to display:", font=FONT_LABEL).grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )

        self.limit_widget = ctk.CTkEntry(
            self, textvariable=self.result_limit, width=150, font=FONT_ENTRY
        )
        self.limit_widget.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Button (rows 1-2)
        ctk.CTkButton(
            self,
            text="Search",
            font=FONT_BUTTON,
            command=self.search,
            width=110,
            height=50,
            fg_color=COLOR_BUTTON_FG,
            hover_color=COLOR_BUTTON_HOVER,
            text_color=COLOR_BUTTON_TEXT,
        ).grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.pack(pady=20, padx=20, fill="x")

    def _clear_placeholder(self, event):
        """Clear placeholder text on focus."""
        if getattr(self, "_placeholder_active", False):
            self.entry_widget.delete(0, "end")
            self._placeholder_active = False

    def _restore_placeholder(self, event):
        """Restore placeholder text on blur."""
        if not self.entry_widget.get().strip():
            self.entry_widget.insert(0, self.placeholder_text)
            self._placeholder_active = True

    def search(self):
        """Execute search."""
        term = self.search_term.get().strip()
        #if not term:
        if term == self.placeholder_text or not term:
            showerror("Info", "Please enter a search term!")
            return


        # Parse limit
        limit_str = self.result_limit.get().strip().lower()
        try:
            if limit_str == "all":
                limit = 200
            else:
                limit = int(limit_str)
                if limit < 1:
                    showerror("Info", "Limit must be >= 1!")
                    return
        except ValueError:
            showerror("Info", "Limit must be a number or 'all'!")
            return

        # Update history
        current_history = self.search_history.get()
        if current_history == "Search history: ":
            new_history = f"Search history: {term}"
        else:
            new_history = f"{current_history} | {term}"
        self.search_history.set(new_history)

        # Clear input
        self.entry_widget.delete(0, tk.END)

        # Search
        self.result_frame.perform_search(term, limit)


class ResultFrame(ctk.CTkFrame):
    """Results display frame."""

    def __init__(self, master, api: ITunesAPI):
        """
        Initialize result frame.

        Args:
            master: Parent widget.
            api: iTunes API instance.
        """
        super().__init__(master)
        self.api = api

        self.result_txt = ctk.CTkTextbox(
            self, font=FONT_TEXT, wrap="word", state="normal"
        )
        self.result_txt.pack(pady=20, fill="both", expand=True, padx=20)
        self.result_txt.insert("1.0", "Results come here ...")

        self.pack(pady=20, padx=20, fill="both")

    def perform_search(self, term: str, limit: int):
        """
        Perform search and display results.

        Args:
            term: Search term.
            limit: Max results.
        """
        try:
            data = self.api.search(term, limit)
            formatted = self.api.format_results(data)
            output_text = "\n".join(formatted)
        except Exception as e:
            output_text = f"Error: {str(e)}"

        self.result_txt.delete("1.0", "end")
        self.result_txt.insert("1.0", output_text)
