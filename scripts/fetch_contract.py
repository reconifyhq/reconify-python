"""Fetch and verify the pinned public OpenAPI contract."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / ".openapi-contract.json"
DEFAULT_OUTPUT = ROOT / ".contract" / "reconify.openapi.json"
DEFAULT_MANIFEST_URL = "https://docs.reconifyhq.com/openapi/manifest.json"


def main() -> None:
    output = Path(os.environ.get("RECONIFY_OPENAPI_SPEC", str(DEFAULT_OUTPUT)))
    update_to_latest = "--latest" in sys.argv
    if os.environ.get("RECONIFY_OPENAPI_SPEC"):
        content = output.read_bytes()
        if update_to_latest:
            document = json.loads(content)
            version = document.get("info", {}).get("version")
            if not version:
                raise SystemExit("Local OpenAPI contract has no info.version")
            PIN_PATH.write_text(
                json.dumps(
                    {
                        "version": version,
                        "sha256": hashlib.sha256(content).hexdigest(),
                    },
                    indent=2,
                )
                + "\n"
            )
        print(f"Using local OpenAPI contract: {output}")
        return

    pinned = json.loads(PIN_PATH.read_text())
    manifest_url = os.environ.get("RECONIFY_OPENAPI_MANIFEST_URL", DEFAULT_MANIFEST_URL)
    with urlopen(manifest_url, timeout=30) as response:
        manifest = json.loads(response.read())
    version = manifest["contract_version"] if update_to_latest else pinned["version"]
    artifact = manifest["versions"].get(version)
    if artifact is None:
        raise SystemExit(f"OpenAPI manifest has no version {version}")
    if not update_to_latest and artifact["sha256"] != pinned["sha256"]:
        raise SystemExit(f"OpenAPI manifest checksum changed for pinned version {version}")
    with urlopen(urljoin(manifest_url, artifact["url"]), timeout=30) as response:
        content = response.read()
    digest = hashlib.sha256(content).hexdigest()
    if update_to_latest:
        PIN_PATH.write_text(json.dumps({"version": version, "sha256": digest}, indent=2) + "\n")
    elif digest != pinned["sha256"]:
        raise SystemExit(f"OpenAPI checksum mismatch: expected {pinned['sha256']}, got {digest}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    print(f"Fetched OpenAPI {version} to {output}")


if __name__ == "__main__":
    main()
