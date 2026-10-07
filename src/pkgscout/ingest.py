"""Read package metadata from the PyPI JSON API."""

import json
import urllib.request

PACKAGES = [
    "requests", "httpx", "numpy", "pandas", "pydantic", "fastapi", "flask", "django",
    "scipy", "matplotlib", "pytest", "ruff", "uv", "polars", "pyarrow", "sqlalchemy",
    "click", "rich", "typer", "loguru", "openai", "mlflow", "boto3", "urllib3", "jinja2",
]  # fmt: skip


def fetch_package(name: str, timeout: int = 20) -> dict:
    """Fetch one package from PyPI and keep the fields we store."""
    url = f"https://pypi.org/pypi/{name}/json"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        data = json.load(response)
    info = data["info"]
    files = data["releases"].get(info["version"]) or data.get("urls") or []
    release_date = files[0]["upload_time_iso_8601"] if files else None
    return {
        "name": info["name"],
        "version": info["version"],
        "summary": info.get("summary"),
        "release_date": release_date,
        "description": info.get("description"),
    }


def fetch_all(names: list[str] | None = None) -> list[dict]:
    """Fetch every package of the list, skipping those that fail."""
    rows = []
    for name in names or PACKAGES:
        try:
            rows.append(fetch_package(name))
        except Exception as e:
            print(f"skipped {name}: {e}")
    return rows
