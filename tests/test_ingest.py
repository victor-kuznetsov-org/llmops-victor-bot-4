import io
import json
from unittest.mock import patch

from pkgscout.ingest import PACKAGES, fetch_package


def test_fetch_package_parses_pypi_json() -> None:
    payload = {
        "info": {"name": "x", "version": "1.0", "summary": "s", "description": "d"},
        "releases": {"1.0": [{"upload_time_iso_8601": "2026-01-01T00:00:00Z"}]},
    }
    with patch("urllib.request.urlopen", return_value=io.StringIO(json.dumps(payload))):
        row = fetch_package("x")
    assert row["release_date"] == "2026-01-01T00:00:00Z"
    assert row["version"] == "1.0"


def test_package_list_size() -> None:
    assert len(PACKAGES) == 25
