"""Configuration for pytest."""

from __future__ import annotations

import os
from importlib.metadata import version


def pytest_report_header() -> list[str]:
    """Return a list of strings to be displayed in the header of the report."""
    pip_env_vars = (f"{var}={value}" for var, value in os.environ.items() if var.startswith("PIP_"))
    gh_env_vars = (
        f"{var}={value}" for var, value in os.environ.items() if var.startswith("GITHUB_")
    )
    return [
        f"sqlalchemy: {version('sqlalchemy')}",
        f"sqlean.py: {version('sqlean.py')}",
        f"PIP_*: {','.join(pip_env_vars)}",
        f"GITHUB_*: {','.join(gh_env_vars)}",
    ]
