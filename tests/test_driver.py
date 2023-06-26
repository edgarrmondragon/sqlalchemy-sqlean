"""Test the driver class."""

from __future__ import annotations

import typing as t

import pytest
from sqlalchemy import create_engine, text

if t.TYPE_CHECKING:
    from sqlalchemy.engine import Engine


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
    assert engine.dialect.dbapi.__name__ == "sqlean"


def test_sql(engine: Engine):
    """Test that the SQL works."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
    assert result.fetchone() == (1,)


@pytest.mark.parametrize(
    ("extensions", "query", "expected"),
    [
        (
            "all",
            """
            select
                hex(md5('hello' || value)) as crypto,
                median(value) as stats
            from generate_series(1, 99)
            """,
            ("203AD5FFA1D7C650AD681FDFF3965CD2", 50),
        ),
        ("stats", "select median(value) from generate_series(1, 99)", (50,)),
        ("crypto", "select hex(md5('hello'))", ("5D41402ABC4B2A76B9719D911017C592",)),
        ("ipaddr", "select ipfamily('192.168.1.1')", (4,)),
        (
            "ipaddr,crypto",
            """select
                ipnetwork('192.168.16.12/24') as network,
                hex(md5('hello')) as hash
            """,
            ("192.168.16.0/24", "5D41402ABC4B2A76B9719D911017C592"),
        ),
    ],
    ids=["all", "stats", "crypto", "ipaddr", "multiple"],
)
def test_extensions(extensions: str, query: str, expected: tuple):
    """Test that the extensions work."""
    url = f"sqlite+sqlean:///:memory:?extensions={extensions}"
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text(query))
    assert result.fetchone() == expected
