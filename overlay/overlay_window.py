from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont

from hardware.sensor_reader import get_hardware_data


class OverlayWindow(QWidget):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
        self._drag_pos: QPoint | None = None

        c = config.get("colors", {})
        self.col_accent  = c.get("accent",     "#00FF41")
        self.col_bg      = c.get("background", "#111111")
        self.col_text    = c.get("text",       "#CCCCCC")
        self.col_warn    = c.get("warn",       "#FFA500")
        self.col_danger  = c.get("danger",     "#FF4444")

        self._setup_window()
        self._setup_ui()
        self._setup_timer()
        self._refresh()          # Sofortige erste Anzeige

    # ------------------------------------------------------------------
    # Fenster-Setup
    # ------------------------------------------------------------------
    def _setup_window(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        pos = self.config.get("position", {"x": 20, "y": 20})
        self.move(pos.get("x", 20), pos.get("y", 20))
        self.setMinimumWidth(230)

    # ------------------------------------------------------------------
    # UI aufbauen
    # ------------------------------------------------------------------
    def _label(self, text: str, size: int = 10, bold: bool = False,
               color: str | None = None) -> QLabel:
        lbl = QLabel(text)
        font = QFont()
        font.setFamily("Consolas")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(size)
        font.setBold(bold)
        lbl.setFont(font)
        lbl.setStyleSheet(f"color: {color or self.col_text}; background: transparent;")
        return lbl

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet(f"background-color: #2a2a2a; border: none;")
        return line

    def _setup_ui(self) -> None:
        root = QVBoxLayout()
        root.setContentsMargins(14, 10, 14, 12)
        root.setSpacing(4)
        self.setLayout(root)

        # ── Titel ──────────────────────────────────────────────────────
        root.addWidget(self._label("◆  DACH WARZONE", size=13, bold=True,
                                   color=self.col_accent))
        root.addWidget(self._divider())

        # ── Hardware-Sektion ───────────────────────────────────────────
        root.addWidget(self._label("HARDWARE", size=8, bold=True, color="#666666"))

        self.lbl_cpu      = self._label("CPU      --  %")
        self.lbl_cpu_temp = self._label("CPU Temp  -- °C")
        self.lbl_gpu_temp = self._label("GPU Temp  -- °C")
        self.lbl_ram      = self._label("RAM      --  %")

        for lbl in (self.lbl_cpu, self.lbl_cpu_temp, self.lbl_gpu_temp, self.lbl_ram):
            root.addWidget(lbl)

        root.addWidget(self._divider())

        # ── Fußzeile ───────────────────────────────────────────────────
        root.addWidget(self._label("Rechtsklick → Beenden", size=7, color="#444444"))

    # ------------------------------------------------------------------
    # Timer
    # ------------------------------------------------------------------
    def _setup_timer(self) -> None:
        interval = self.config.get("update_interval_ms", 1500)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(interval)

    # ------------------------------------------------------------------
    # Daten aktualisieren
    # ------------------------------------------------------------------
    def _color_for_usage(self, pct: float) -> str:
        if pct >= 85:
            return self.col_danger
        if pct >= 65:
            return self.col_warn
        return self.col_accent

    def _color_for_temp(self, deg: float) -> str:
        if deg >= 85:
            return self.col_danger
        if deg >= 70:
            return self.col_warn
        return self.col_accent

    def _set_label(self, label: QLabel, text: str, color: str) -> None:
        label.setText(text)
        label.setStyleSheet(f"color: {color}; background: transparent;")

    def _refresh(self) -> None:
        d = get_hardware_data()

        cpu = d.get("cpu_percent", 0.0)
        ram = d.get("ram_percent", 0.0)
        ram_used  = d.get("ram_used_gb", 0.0)
        ram_total = d.get("ram_total_gb", 0.0)
        cpu_temp  = d.get("cpu_temp")
        gpu_temp  = d.get("gpu_temp")

        self._set_label(self.lbl_cpu,
                        f"CPU      {cpu:5.1f} %",
                        self._color_for_usage(cpu))

        if cpu_temp is not None:
            self._set_label(self.lbl_cpu_temp,
                            f"CPU Temp {cpu_temp:4.0f} °C",
                            self._color_for_temp(cpu_temp))
        else:
            self._set_label(self.lbl_cpu_temp, "CPU Temp   N/A", "#555555")

        if gpu_temp is not None:
            self._set_label(self.lbl_gpu_temp,
                            f"GPU Temp {gpu_temp:4.0f} °C",
                            self._color_for_temp(gpu_temp))
        else:
            self._set_label(self.lbl_gpu_temp, "GPU Temp   N/A", "#555555")

        self._set_label(self.lbl_ram,
                        f"RAM      {ram:5.1f} %  ({ram_used:.1f}/{ram_total:.0f} GB)",
                        self._color_for_usage(ram))

        self.adjustSize()

    # ------------------------------------------------------------------
    # Hintergrund zeichnen
    # ------------------------------------------------------------------
    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(self.col_bg)
        bg.setAlpha(int(self.config.get("opacity", 0.88) * 255))

        border = QColor(self.col_accent)
        border.setAlpha(120)

        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(border, 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)

    # ------------------------------------------------------------------
    # Drag & Drop (linke Maustaste)
    # ------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            QApplication.quit()

    def mouseMoveEvent(self, event) -> None:  # type: ignore[override]
        if self._drag_pos is not None and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None
