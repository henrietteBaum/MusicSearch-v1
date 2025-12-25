# tk-music-search

Ein Lernprojekt: iTunes Album-Suche mit Tk-GUI und  Projektstruktur. 

Version 1.5 trennt die Programmlogik von den Dateien für die grafische Benutzeroberfläche.

## Features

- **Saubere Architektur**: Trennung von GUI, API, Konfiguration
- **Tk/CustomTkinter GUI**: Dunkel-Theme, Scaling, Zoom (Ctrl+Scroll)
- **iTunes API Integration**: Album-Suche, Historyverfolgung
- **Responsive Design**: Scrollbar, Grid-Layout, Mausrad-Navigation
- **Python Best Practices**: Type Hints, Docstrings, Modulstruktur

## Projektstruktur

```
tk-music-search/
├── src/music_search/
│   ├── __init__.py              # Package init
│   ├── config.py                # App-Konfiguration
│   ├── gui/
│   │   ├── __init__.py
│   │   └── main.py              # GUI-Komponenten (App, SearchFrame, ResultFrame)
│   ├── api/
│   │   ├── __init__.py
│   │   └── itunes.py            # iTunes API Client
│   └── utils/
│       ├── __init__.py
│       └── constants.py         # Konstanten (Farben, Fonts, URLs)
├── tests/
│   ├── __init__.py
│   └── test_api.py              # Unit Tests
├── docs/
│   └── README.md                # Diese Datei
├── main.py                      # Entry Point
├── setup.py                     # Package Setup (pip install)
├── pyproject.toml               # Modern Python Config
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Dev Dependencies
└── .gitignore                   # Git Ignore
```

## Installation

### Aus Source (mit venv)

```bash
# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Oder mit dev-Tools:
pip install -r requirements-dev.txt
```

### Mit pip install (nach setup.py)

```bash
pip install -e .          # Development install
pip install .[dev]        # Inklusive dev-Tools
```

## Verwendung

```bash
# App starten
python main.py
```

## Verwendete Technologien

- **Python 3.8+**
- **CustomTkinter**: Moderne Tk-Wrapper mit Dark-Theme
- **Requests**: HTTP-Requests für iTunes API
- **Pytest**: Unit Testing

## Lernpunkte

Dieses Projekt zeigt:

1. **Projektstruktur**: src-Layout nach PEP 420/517
2. **Modularisierung**: Klare Trennung von Concerns (GUI, API, Config)
3. **API-Integration**: Externe REST-APIs richtig nutzen
4. **GUI-Design**: Responsive Layouts mit Tk
5. **Type Hints**: Moderne Python-Typisierung
6. **Documentation**: Docstrings, README, Code-Kommentare
7. **Testing**: Unit Tests für API

## Nächste Schritte

- [ ] Phase 2: Alternative GUI-Frameworks (PySimpleGUI, PyQt5)
- [ ] Phase 3: Web-Version (Flask/Django) mit Accessibility
- [ ] Erweiterte API-Features (Caching, Rate-Limiting)
- [ ] Persistente Suche-Historie (JSON/SQLite)

## Lizenz

MIT License

---

**Autor**: Henriette Baum | **Version**: 1.5.0
