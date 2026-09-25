from app.config import DEFAULT_WASTE_PCT
from app.db import connect

DEFAULT_MAX_MODE = "0"


def get_all() -> dict:
    conn = connect()
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        out = {r["key"]: r["value"] for r in rows}
        if "waste_pct" not in out:
            out["waste_pct"] = str(DEFAULT_WASTE_PCT)
        if "max_mode" not in out:
            out["max_mode"] = DEFAULT_MAX_MODE
        return out
    finally:
        conn.close()


def get_waste_pct() -> float:
    raw = get_all().get("waste_pct", str(DEFAULT_WASTE_PCT))
    return float(raw)


def get_max_mode_default() -> bool:
    raw = get_all().get("max_mode", DEFAULT_MAX_MODE)
    return str(raw).strip().lower() in ("1", "true", "yes", "on")


def set_values(values: dict) -> dict:
    conn = connect()
    try:
        for key, value in values.items():
            conn.execute(
                "INSERT INTO settings(key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (str(key), str(value)),
            )
        conn.commit()
    finally:
        conn.close()
    return get_all()
