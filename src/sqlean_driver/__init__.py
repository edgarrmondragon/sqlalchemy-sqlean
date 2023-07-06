"""Dialect class for SQLAlchemy that uses sqlean.py as the DBAPI."""

from __future__ import annotations

import typing as t
from importlib.metadata import version

from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

if t.TYPE_CHECKING:
    from types import ModuleType

    from sqlalchemy.engine.url import URL


__version__ = version(__package__)


class SQLeanDialect(SQLiteDialect_pysqlite):
    """A dialect for SQLite that uses sqlean.py as the DBAPI."""

    driver = "sqlean"
    supports_statement_cache = True

    @classmethod
    def dbapi(cls: type[SQLeanDialect]) -> ModuleType:  # type: ignore[override]
        """Return the DBAPI module.

        NOTE: This is a legacy method that will stop being used by SQLAlchemy at some point.
        """
        return cls.import_dbapi()

    @classmethod
    def import_dbapi(cls: type[SQLeanDialect]) -> ModuleType:
        """Return the DBAPI module."""
        import sqlean

        return sqlean

    def on_connect_url(self: SQLeanDialect, url: URL) -> t.Callable[[t.Any], t.Any] | None:
        """Return a callable that will be executed on connect."""
        query = url.query.get("extensions", ())
        extensions = query if isinstance(query, tuple) else query.split(",")

        if "all" in extensions:
            self.dbapi.extensions.enable_all()  # type: ignore[attr-defined]
        else:
            self.dbapi.extensions.enable(*extensions)  # type: ignore[attr-defined]

        return super().on_connect_url(url)
