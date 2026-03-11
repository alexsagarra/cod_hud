import json
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_ROOT, "config.json")

DEFAULT_CONFIG = {
    "position": {"x": 20, "y": 20},
    "opacity": 0.88,
    "update_interval_ms": 1500,
    "colors": {
        "accent": "#00FF41",
        "background": "#111111",
        "text": "#CCCCCC",
        "warn": "#FFA500",
        "danger": "#FF4444"
    }
}


def load_config() -> dict:
    if os.path.exists(_CONFIG_PATH):
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                user = json.load(f)
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(user)
            return cfg
        except Exception:
            pass
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    try:
        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass
