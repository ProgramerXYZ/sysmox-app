#!/usr/bin/env python3
from psutil import virtual_memory, cpu_count # only what we actually need


# --- BEGIN: FIRST-RUN CONFIG GUARD (ADD TO setup.py) ---
import os
import json
import tempfile
from pathlib import Path

def ensure_user_config_exists():
    """
    Create %APPDATA%/Sysmox directory and config.json with safe defaults.
    Idempotent and uses atomic write to avoid partial files.
    Returns the Path to the config file (or None on failure).
    """
    try:
        # Resolve APPDATA in a robust way; fallback to a sensible location
        appdata = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        cfg_dir = Path(appdata) / "Sysmox"
        cfg_dir.mkdir(parents=True, exist_ok=True)  # ensure directory exists

        cfg_file = cfg_dir / "config.json"

        if not cfg_file.exists():
            default_config = {
                "configured": False,
                "version": "0.2.0-beta"
            }

            # Atomic write: write to a temp file then rename
            tf = None
            try:
                tf = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", dir=str(cfg_dir))
                json.dump(default_config, tf, indent=4)
                tf.flush()
                tf.close()
                # Replace is atomic on modern Windows / POSIX
                os.replace(tf.name, str(cfg_file))
            finally:
                # Cleanup if something went wrong and tmp file still exists
                if tf is not None:
                    tmp_path = Path(tf.name)
                    if tmp_path.exists() and not cfg_file.exists():
                        try:
                            tmp_path.unlink()
                        except Exception:
                            pass

        return cfg_file
    except Exception as e:
        # Fail gracefully: print a warning but do not raise (setup should not crash)
        print(f"[setup.py] Warning: could not create Sysmox config: {e}")
        return None

# Run it immediately when setup.py executes (safe and idempotent)
ensure_user_config_exists()
# --- END: FIRST-RUN CONFIG GUARD (ADD TO setup.py) ---


def create_config():
    APPDATA_DIR = Path(os.environ["APPDATA"]) / "Sysmox" 
    config_path = APPDATA_DIR / "config.json"

    virt = virtual_memory()
    core_C = cpu_count(logical=False)
    cpu_Hyperthred_count = cpu_count(logical=True)

    config = {
        "total_physical_memory": virt.total,
        "total_core_count": core_C,
        "total cpu Hyperthred count": cpu_Hyperthred_count,
        "configured": True
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("[✅] Config file created successfully.")
    print(f"💾 Total physical memory: {virt.total} bytes")
    print(f"⚙️ Total core count: {core_C} cores")
    print(f"🧵 Total Hyperthreading count: {cpu_Hyperthred_count} threads")


