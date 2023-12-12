"""Test the custom types."""

from __future__ import annotations

import sys
import typing as t
import uuid
from ipaddress import IPv4Interface, IPv4Network, IPv6Interface

import pytest
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Table,
    create_engine,
    func,
    select,
)

from sqlean_driver.custom_types import CIDR, INET, UUID

if t.TYPE_CHECKING:
    from sqlalchemy import Select

metadata = MetaData()
table = Table(
    "test_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ip", INET),
    Column("cidr", CIDR),
    Column("uuid_col", UUID),
)


@pytest.mark.xfail(
    sys.platform == "win32",
    reason="'ipaddr' extension not available on Windows",
)
@pytest.mark.parametrize(
    ("data", "query", "expected"),
    [
        pytest.param(
            [{"ip": None}],
            select(table.c.ip, table.c.ip.ipnetwork()),
            (None, None),
            id="nullable",
        ),
        pytest.param(
            [{"cidr": None}],
            select(table.c.cidr),
            (None,),
            id="nullable_cidr",
        ),
        pytest.param(
            [{"cidr": IPv4Network("192.168.16.3/32")}],
            select(table.c.cidr),
            (IPv4Network("192.168.16.3/32"),),
            id="cidr",
        ),
        pytest.param(
            [{"ip": IPv4Network("192.168.1.1")}],
            select(func.ipfamily(table.c.ip), table.c.ip.ipfamily()),
            (4, 4),
            id="ipfamily",
        ),
        pytest.param(
            [{"ip": IPv6Interface("2001:db8::123/64")}],
            select(func.iphost(table.c.ip), table.c.ip.iphost()),
            ("2001:db8::123", "2001:db8::123"),
            id="iphost",
        ),
        pytest.param(
            [{"ip": IPv4Interface("192.168.16.12/24")}],
            select(func.ipmasklen(table.c.ip), table.c.ip.ipmasklen()),
            (24, 24),
            id="ipmasklen",
        ),
        pytest.param(
            [{"ip": IPv4Interface("192.168.16.12/24")}],
            select(func.ipnetwork(table.c.ip), table.c.ip.ipnetwork()),
            (
                IPv4Network("192.168.16.0/24"),
                IPv4Network("192.168.16.0/24"),
            ),
            id="ipnetwork",
        ),
        pytest.param(
            [{"ip": IPv4Interface("192.168.16.0/24")}],
            select(
                func.ipcontains(table.c.ip, "192.168.16.3"),
                table.c.ip.ipcontains("192.168.16.3"),
            ),
            (True, True),
            id="ipcontains_lhs",
        ),
        pytest.param(
            [{"ip": IPv4Interface("192.168.16.3")}],
            select(
                func.ipcontains("192.168.16.0/24", table.c.ip),
            ),
            (True,),
            id="ipcontains_rhs",
        ),
    ],
)
def test_ipaddr_types(
    data: list[dict[str, t.Any]],
    query: Select[t.Any],
    expected: tuple[t.Any, ...],
) -> None:
    """Test that the types work."""
    engine = create_engine("sqlite+sqlean:///:memory:?extensions=ipaddr")
    metadata.create_all(engine)
    with engine.connect() as conn, conn.begin():
        conn.execute(table.insert(), data)
        result = conn.execute(query)
        assert result.fetchone() == expected


@pytest.mark.parametrize(
    ("data", "query", "expected"),
    [
        pytest.param(
            [{"uuid_col": None}],
            select(table.c.uuid_col),
            (None,),
            id="nullable",
        ),
    ],
)
def test_uuid_types(
    data: list[dict[str, t.Any]],
    query: Select[t.Any],
    expected: tuple[t.Any, ...],
) -> None:
    """Test that the types work."""
    engine = create_engine("sqlite+sqlean:///:memory:?extensions=uuid")
    metadata.create_all(engine)
    with engine.connect() as conn, conn.begin():
        conn.execute(table.insert(), data)
        result = conn.execute(query)
        assert result.fetchone() == expected


def test_function_uuid4() -> None:
    """Test that the function works."""
    engine = create_engine("sqlite+sqlean:///:memory:?extensions=uuid")
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(select(func.uuid4()))
        row = result.fetchone()
        assert row is not None
        assert isinstance(row[0], uuid.UUID)


def test_function_uuid_str() -> None:
    """Test that the function works."""
    engine = create_engine("sqlite+sqlean:///:memory:?extensions=uuid")
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(select(func.uuid_str("8d144638-3baf-4901-a554-b541142c152b")))
        row = result.fetchone()
        assert row is not None
        assert row[0] == uuid.UUID("8d144638-3baf-4901-a554-b541142c152b")


def test_function_uuid_blob() -> None:
    """Test that the function works."""
    engine = create_engine("sqlite+sqlean:///:memory:?extensions=uuid")
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(
            select(
                func.uuid_blob("8d144638-3baf-4901-a554-b541142c152b"),
                func.uuid_blob(func.uuid4()),
            ),
        )
        row = result.fetchone()
        assert row is not None
        assert isinstance(row[0], bytes)
        assert isinstance(row[1], bytes)
