import json
from datetime import datetime, timezone
from typing import Any

from config import DATA_DIR, LEADS_FILE


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_leads() -> list[dict[str, Any]]:
    _ensure_data_dir()
    if not LEADS_FILE.exists():
        return []
    with LEADS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def save_lead(lead: dict[str, Any]) -> None:
    leads = _load_leads()
    lead["created_at"] = datetime.now(timezone.utc).isoformat()
    leads.append(lead)
    _ensure_data_dir()
    with LEADS_FILE.open("w", encoding="utf-8") as file:
        json.dump(leads, file, ensure_ascii=False, indent=2)
