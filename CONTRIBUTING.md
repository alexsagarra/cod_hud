# Contributing

Danke fuer deinen Beitrag.

## Entwicklungsumgebung

1. Python 3.11+ installieren
2. Virtuelle Umgebung erstellen und aktivieren
3. Abhaengigkeiten installieren

Windows (PowerShell):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Coding Guidelines

- Kleine, fokussierte Commits
- Aussagekraeftige Commit-Messages
- Keine lokalen Artefakte committen (venv, cache, logs)
- Vor PR lokal starten und kurz testen

## Pull Requests

- Klaren Titel und kurze Beschreibung schreiben
- Bei UI-Aenderungen Screenshots anhaengen
- Falls relevant, Schritte zum Testen dokumentieren
