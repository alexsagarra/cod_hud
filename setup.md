# Setup unter Windows (Installation + Start)

Diese Anleitung zeigt dir Schritt fuer Schritt, wie du das Overlay auf einem Windows-System installierst und startest.

---

## 1) Voraussetzungen

- Windows 10 oder Windows 11
- Python 3.11 oder neuer (64-bit)
- Internetzugang fuer die Paketinstallation

Hinweis:
Wenn dein Projekt aktuell in WSL liegt (z. B. unter `/home/...`), nutze fuer Windows eine normale Windows-Kopie des Projekts (z. B. `C:\Users\<Name>\Desktop\cod_hud`) und erstelle dort ein eigenes Windows-venv.

---

## 2) Projektordner in Windows oeffnen

1. Kopiere den Projektordner in ein Windows-Verzeichnis (z. B. `C:\dev\cod_hud`).
2. Oeffne den Ordner in VS Code oder im Explorer.
3. Starte ein Terminal im Projektordner:
	- PowerShell in VS Code: `Terminal -> New Terminal`
	- oder Windows-Terminal / PowerShell im Ordner

---

## 3) Python und pip pruefen

Im Terminal ausfuehren:

```powershell
py --version
```

Wenn Python nicht gefunden wird, Python installieren:
- https://www.python.org/downloads/windows/
- Bei der Installation die Option "Add Python to PATH" aktivieren.

Falls `pip` spaeter fehlt, kannst du es so reparieren:

```powershell
py -m ensurepip --upgrade
```

---

## 4) Virtuelle Umgebung erstellen und aktivieren

Im Projektordner:

```powershell
py -3.11 -m venv .venv
```

PowerShell aktivieren:

```powershell
.\.venv\Scripts\Activate.ps1
```

Falls eine Execution-Policy-Fehlermeldung kommt:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Du erkennst die aktive venv am Praefix `(.venv)` im Terminal.

---

## 5) Abhaengigkeiten installieren

Wichtig: immer ueber den aktiven Interpreter installieren:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Installiert werden aktuell:
- `PyQt6`
- `psutil`

---

## 6) Overlay starten

Im selben (aktivierten) Terminal:

```powershell
python main.py
```

Danach sollte das Overlay oben links erscheinen.

Bedienung:
- Linke Maustaste halten und ziehen: Overlay verschieben
- Rechte Maustaste: Overlay beenden

---

## 7) Konfiguration anpassen

Die Einstellungen stehen in `config.json`.

Wichtige Felder:
- `position.x`, `position.y`: Startposition
- `opacity`: Transparenz (z. B. `0.88`)
- `update_interval_ms`: Aktualisierungsintervall
- `colors`: Farbschema

Nach Aenderungen Datei speichern und das Overlay neu starten.

---

## 8) Typische Probleme und Loesungen

### `ModuleNotFoundError` (z. B. `PyQt6` oder `psutil`)

Ursache: Falscher Interpreter oder venv nicht aktiv.

Loesung:
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

### `No module named pip`

Loesung:
```powershell
py -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### CPU/GPU-Temperatur zeigt `N/A`

Das kann auf Windows je nach Hardware/Treiber normal sein.

Hinweise:
- CPU-Temperaturen sind nicht auf jedem System direkt ueber `psutil` verfuegbar.
- Fuer NVIDIA-GPU wird zusaetzlich `nvidia-smi` verwendet (kommt i. d. R. mit dem NVIDIA-Treiber).

### Overlay ist im Spiel nicht sichtbar

Pruefe:
- Spiel im "Borderless Window" statt exklusivem Fullscreen starten.
- Overlay und Spiel mit gleichem Rechtestatus starten (beide normal oder beide als Admin).

---

## 9) Beenden und spaeter neu starten

venv verlassen:

```powershell
deactivate
```

Spaeter erneut starten:

```powershell
cd C:\dev\cod_hud
.\.venv\Scripts\Activate.ps1
python main.py
```

---

## 10) Kurzfassung (Quick Start)

```powershell
cd C:\dev\cod_hud
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```