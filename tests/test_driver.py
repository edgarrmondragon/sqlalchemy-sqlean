"""Test the driver class."""

from __future__ import annotations

import typing as t
from types import ModuleType

import pytest
from sqlalchemy import column, create_engine, func, select
from sqlalchemy.exc import OperationalError

if t.TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.sql.selectable import Select


@pytest.fixture()
def engine() -> Engine:
    """Return a SQLAlchemy engine."""
    url = "sqlite+sqlean:///:memory:"
    return create_engine(url)


def test_driver_name(engine: Engine):
    """Test that the URL works."""
    assert engine.dialect.driver == "sqlean"


def test_driver_dbapi(engine: Engine):
    """Test that the DBAPI is sqlean."""
    assert isinstance(engine.dialect.dbapi, ModuleType)
    assert engine.dialect.dbapi.__name__ == "sqlean"


def test_sql(engine: Engine):
    """Test that the SQL works."""
    with engine.connect() as conn:
        result = conn.execute(select(1))
    assert result.fetchone() == (1,)


def test_no_extensions(engine: Engine):
    """Test that the extensions are not loaded."""
    with pytest.raises(OperationalError), engine.connect() as conn:
        conn.execute(
            select(
                func.median(column("value")),
            ).select_from(
                func.generate_series(1, 99).alias("generate_series_1"),
            ),
        )


@pytest.mark.parametrize(
    ("extensions", "query", "expected"),
    [
        (
            "all",
            select(
                func.hex(func.md5(func.concat("hello", column("value")))).label("crypto"),
                func.median(column("value")).label("stats"),
            ).select_from(
                func.generate_series(1, 99).alias("generate_series_1"),
            ),
            ("203AD5FFA1D7C650AD681FDFF3965CD2", 50),
        ),
        (
            "stats",
            select(
                func.median(column("value")),
            ).select_from(
                func.generate_series(1, 99).alias("generate_series_1"),
            ),
            (50,),
        ),
        ("crypto", select(func.hex(func.md5("hello"))), ("5D41402ABC4B2A76B9719D911017C592",)),
        (
            "ipaddr",
            select(func.ipfamily("192.168.1.1")),
            (4,),
        ),
        (
            "ipaddr,crypto",
            select(
                func.ipnetwork("192.168.16.12/24").label("network"),
                func.hex(func.md5("hello")).label("hash"),
            ),
            ("192.168.16.0/24", "5D41402ABC4B2A76B9719D911017C592"),
        ),
    ],
    ids=["all", "stats", "crypto", "ipaddr", "multiple"],
)
def test_extensions(extensions: str, query: Select, expected: tuple):
    """Test that the extensions work."""
    url = f"sqlite+sqlean:///:memory:?extensions={extensions}"
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(query)
    assert result.fetchone() == expected
