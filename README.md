# DACH Warzone Overlay

Leichtgewichtiges Desktop-Overlay fuer Windows, das waehrend des Spielens wichtige Hardwaredaten anzeigt.

Aktueller Stand:
- CPU-Auslastung
- RAM-Auslastung und RAM-Belegung
- CPU-Temperatur (wenn vom System verfuegbar)
- GPU-Temperatur (psutil, bei NVIDIA zusaetzlich ueber nvidia-smi)

## Tech Stack

- Python 3.11+
- PyQt6
- psutil

## Schnellstart (Windows)

Die vollstaendige Anleitung steht in [setup.md](setup.md).

Kurzfassung:

```powershell
cd C:\dev\cod_hud
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Projektstruktur

```text
cod_hud/
  config/
  hardware/
  overlay/
  data/
  main.py
  config.json
  requirements.txt
  setup.md
```

## Konfiguration

Die Overlay-Einstellungen liegen in [config.json](config.json):

- position.x / position.y
- opacity
- update_interval_ms
- colors

## GitHub Upload (erste Veroeffentlichung)

Im Projektordner ausfuehren:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/DEIN-USERNAME/DEIN-REPO.git
git push -u origin main
```

Hinweis: Durch die [.gitignore](.gitignore) werden virtuelle Umgebungen, Caches und lokale Artefakte nicht mit hochgeladen.

## Bekannte Hinweise

- Temperaturwerte koennen je nach Treiber/Hardware als N/A erscheinen.
- Fuer bestes Overlay-Verhalten im Spiel Borderless Window verwenden.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE).