from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import AuthorityIndex


def export_authorities(authority_index: AuthorityIndex, output_path: str | Path | None = None) -> dict[str, Any]:
    payload = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_directory": authority_index.source_directory,
        "record_count": len(authority_index.records),
        "authorities": [record.to_dict() for record in authority_index.records],
    }
    if output_path is not None:
        destination = Path(output_path)
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
