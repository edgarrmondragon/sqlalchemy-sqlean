"""Configuration for pytest."""

from __future__ import annotations

from sqlalchemy import __version__ as sqlalchemy_version


def pytest_report_header() -> list[str]:
    """Return a list of strings to be displayed in the header of the report."""
    return [f"sqlalchemy: {sqlalchemy_version}"]
