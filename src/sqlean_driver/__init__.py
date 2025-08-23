"""Dialect class for SQLAlchemy that uses sqlean.py as the DBAPI."""

from __future__ import annotations

import typing as t
import uuid
from importlib.metadata import version

import sqlalchemy.types as sqltypes
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite
from sqlalchemy.sql.functions import GenericFunction

from sqlean_driver.custom_types import UUID

if t.TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType

    from sqlalchemy.engine.url import URL
    from sqlalchemy.sql.type_api import TypeEngine

    from sqlean_driver.custom_types import IPAddress, IPNetwork

__version__ = version(__package__)


class SQLeanTypeCompiler(SQLiteTypeCompiler):
    """A type compiler for SQLite that uses sqlean.py as the DBAPI."""

    def visit_INET(  # noqa: PLR6301
        self,
        type_: TypeEngine[IPAddress],  # noqa: ARG002
        **kw: t.Any,  # noqa: ARG002
    ) -> str:
        """Visit an INET node."""
        return "INET"

    def visit_CIDR(self, type_: TypeEngine[IPNetwork], **kw: t.Any) -> str:  # noqa: ARG002, PLR6301
        """Visit a CIDR nodes."""
        return "CIDR"

    def visit_UUID(self, type_: TypeEngine[uuid.UUID], **kw: t.Any) -> str:  # noqa: ARG002, PLR6301
        """Visit a UUID node."""
        return "UUID"


class uuid4(GenericFunction[uuid.UUID]):  # noqa: N801
    """Generates a version 4 (random) UUID as a string.

    Aliased as gen_random_uuid() for PostgreSQL compatibility.
    """

    name = "uuid4"
    type = UUID()
    inherit_cache = True


class gen_random_uuid(uuid4):  # noqa: N801
    """Generates a version 4 (random) UUID as a string."""

    name = "gen_random_uuid"


class uuid_str(GenericFunction[uuid.UUID]):  # noqa: N801
    """Converts a UUID `X` into a well-formed UUID string.

    `X` can be either a string or a blob.
    """

    name = "uuid_str"
    type = UUID()
    inherit_cache = True


class uuid_blob(GenericFunction[bytes]):  # noqa: N801
    """Converts a UUID `X` into a well-formed UUID string.

    `X` can be either a string or a blob.
    """

    name = "uuid_blob"
    type = sqltypes.BLOB()
    inherit_cache = True


class SQLeanDialect(SQLiteDialect_pysqlite):
    """A dialect for SQLite that uses sqlean.py as the DBAPI."""

    driver = "sqlean"
    supports_statement_cache = True
    type_compiler = SQLeanTypeCompiler

    @classmethod
    def dbapi(cls) -> ModuleType:  # type: ignore[override]
        """Return the DBAPI module.

        NOTE: This is a legacy method that will stop being used by SQLAlchemy at some point.
        """
        return cls.import_dbapi()

    @classmethod
    def import_dbapi(cls) -> ModuleType:
        """Return the DBAPI module."""
        import sqlean  # noqa: PLC0415

        return sqlean  # type: ignore[no-any-return]

    def on_connect_url(self, url: URL) -> Callable[[t.Any], t.Any] | None:
        """Return a callable that will be executed on connect."""
        query = url.query.get("extensions", ())
        extensions = query if isinstance(query, tuple) else query.split(",")

        if "all" in extensions:
            self.dbapi.extensions.enable_all()  # type: ignore[attr-defined]
        else:
            self.dbapi.extensions.enable(*extensions)  # type: ignore[attr-defined]

        return super().on_connect_url(url)
