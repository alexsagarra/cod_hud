"""
Liest Hardware-Sensoren via psutil aus.
Temperaturen werden über psutil.sensors_temperatures() abgerufen (Linux/Windows).
Für NVIDIA-GPUs wird nvidia-smi als Fallback verwendet.
"""
import subprocess
import psutil


# Bekannte Schlüssel für CPU-Temperaturen (psutil)
_CPU_TEMP_KEYS = ("coretemp", "k10temp", "zenpower", "cpu_thermal", "acpitz")
# Bekannte Schlüssel für GPU-Temperaturen (psutil)
_GPU_TEMP_KEYS = ("amdgpu", "radeon", "nouveau")


def _cpu_temp_psutil() -> float | None:
    try:
        all_temps = psutil.sensors_temperatures()
        if not all_temps:
            return None
        for key in _CPU_TEMP_KEYS:
            entries = all_temps.get(key, [])
            vals = [e.current for e in entries if e.current and e.current > 0]
            if vals:
                return round(max(vals), 1)
        # Generischer Fallback: erster verfügbarer Sensor
        for entries in all_temps.values():
            vals = [e.current for e in entries if e.current and e.current > 0]
            if vals:
                return round(max(vals), 1)
    except Exception:
        pass
    return None


def _gpu_temp_psutil() -> float | None:
    try:
        all_temps = psutil.sensors_temperatures()
        if not all_temps:
            return None
        for key in _GPU_TEMP_KEYS:
            entries = all_temps.get(key, [])
            vals = [e.current for e in entries if e.current and e.current > 0]
            if vals:
                return round(max(vals), 1)
    except Exception:
        pass
    return None


def _gpu_temp_nvidia_smi() -> float | None:
    """Liest GPU-Temperatur über nvidia-smi (NVIDIA-Karten)."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            val = result.stdout.strip().splitlines()[0].strip()
            return float(val)
    except Exception:
        pass
    return None


def get_hardware_data() -> dict:
    """Gibt einen Dict mit aktuellen Hardware-Metriken zurück."""
    data: dict = {}

    # CPU-Auslastung (non-blocking, liefert Wert seit letztem Aufruf)
    data["cpu_percent"] = psutil.cpu_percent(interval=None)

    # RAM
    mem = psutil.virtual_memory()
    data["ram_percent"] = mem.percent
    data["ram_used_gb"] = round(mem.used / 1024 ** 3, 1)
    data["ram_total_gb"] = round(mem.total / 1024 ** 3, 1)

    # CPU-Temperatur
    data["cpu_temp"] = _cpu_temp_psutil()

    # GPU-Temperatur: zuerst psutil, dann nvidia-smi
    gpu_temp = _gpu_temp_psutil()
    if gpu_temp is None:
        gpu_temp = _gpu_temp_nvidia_smi()
    data["gpu_temp"] = gpu_temp

    return data
