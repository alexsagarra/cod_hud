import sys
import psutil
from PyQt6.QtWidgets import QApplication

from config.config_loader import load_config
from overlay.overlay_window import OverlayWindow


def main() -> None:
    # Ersten psutil-Aufruf "aufwärmen" – sonst liefert cpu_percent() beim
    # ersten echten Aufruf immer 0.0.
    psutil.cpu_percent(interval=0.1)

    app = QApplication(sys.argv)
    app.setApplicationName("DACH Warzone Overlay")
    app.setQuitOnLastWindowClosed(True)

    config = load_config()
    window = OverlayWindow(config)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
