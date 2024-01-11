"""Custom SQLAlchemy types."""

from __future__ import annotations

import ipaddress
import typing as t
import uuid

import sqlalchemy.types as sqltypes
from sqlalchemy.sql.functions import GenericFunction

if t.TYPE_CHECKING:
    import sys

    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias  # noqa: ICN003

    from sqlalchemy.engine.interfaces import Dialect
    from sqlalchemy.sql.type_api import _BindProcessorType, _ResultProcessorType


IPAddress: TypeAlias = t.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPNetwork: TypeAlias = t.Union[ipaddress.IPv4Network, ipaddress.IPv6Network]


def none_or_str(value: t.Any | None) -> str | None:  # noqa: ANN401
    """Return the value or None."""
    return str(value) if value is not None else None


def none_or_ip_interface(
    value: t.Any | None,  # noqa: ANN401
) -> ipaddress.IPv4Interface | ipaddress.IPv6Interface | None:
    """Return the value or None."""
    return ipaddress.ip_interface(value) if value is not None else None


def none_or_ip_network(
    value: t.Any | None,  # noqa: ANN401
) -> ipaddress.IPv4Network | ipaddress.IPv6Network | None:
    """Return the value or None."""
    return ipaddress.ip_network(value) if value is not None else None


def none_or_uuid(
    value: t.Any | None,  # noqa: ANN401
) -> uuid.UUID | None:
    """Return the value or None."""
    return uuid.UUID(value) if value is not None else None


class INET(sqltypes.TypeEngine[IPAddress]):
    """An INET type."""

    __visit_name__ = "INET"

    def bind_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
    ) -> _BindProcessorType[IPAddress] | None:
        """Return a bind processor."""
        return none_or_str

    def result_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
        _coltype: object,
    ) -> _ResultProcessorType[IPAddress] | None:
        """Return a result processor."""
        return none_or_ip_interface

    # TODO(edgarrmondragon): Add missing type parameters:
    # > sqltypes.Indexable.Comparator[IPAddress]
    # > sqltypes.Concatenable.Comparator[IPAddress]
    # https://github.com/edgarrmondragon/sqlean-driver/issues/37
    class Comparator(
        sqltypes.Indexable.Comparator,  # type: ignore[type-arg]
        sqltypes.Concatenable.Comparator,  # type: ignore[type-arg]
    ):
        """Comparator for the INET type."""

        def ipfamily(self) -> _IPAddrIPFamilyFunction:
            """Return the IP family."""
            return _IPAddrIPFamilyFunction(self.expr)

        def iphost(self) -> _IPAddrIPHostFunction:
            """Return the IP host."""
            return _IPAddrIPHostFunction(self.expr)

        def ipmasklen(self) -> _IPAddrIPMaskLenFunction:
            """Return the IP mask length."""
            return _IPAddrIPMaskLenFunction(self.expr)

        def ipnetwork(self) -> _IPAddrIPNetworkFunction:
            """Return the IP network."""
            return _IPAddrIPNetworkFunction(self.expr)

        def ipcontains(self, other: IPAddress | str) -> _IPAddrIPContainsFunction:
            """Return whether the IP address contains another IP address."""
            return _IPAddrIPContainsFunction(self.expr, other)

    comparator_factory = Comparator


class CIDR(sqltypes.TypeEngine[IPNetwork]):
    """A CIDR type."""

    __visit_name__ = "CIDR"

    def bind_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
    ) -> _BindProcessorType[IPNetwork] | None:
        """Return a bind processor."""
        return none_or_str

    def result_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
        _coltype: object,
    ) -> _ResultProcessorType[IPNetwork] | None:
        """Return a result processor."""
        return none_or_ip_network


class UUID(sqltypes.TypeEngine[uuid.UUID]):
    """A UUID type."""

    __visit_name__ = "UUID"

    def bind_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
    ) -> _BindProcessorType[uuid.UUID] | None:
        """Return a bind processor."""
        return none_or_str

    def result_processor(  # noqa: PLR6301
        self,
        _dialect: Dialect,
        _coltype: object,
    ) -> _ResultProcessorType[uuid.UUID] | None:
        """Return a result processor."""
        return none_or_uuid


class _IPAddrIPFamilyFunction(GenericFunction[int]):
    """Returns the family of a specified IP address."""

    name = "ipfamily"
    type = sqltypes.Integer()  # noqa: A003
    inherit_cache = True


class _IPAddrIPHostFunction(GenericFunction[str]):
    """Returns the host part of an IP address."""

    name = "iphost"
    type = sqltypes.String()  # noqa: A003
    inherit_cache = True


class _IPAddrIPMaskLenFunction(GenericFunction[int]):
    """Returns the prefix length of an IP address."""

    name = "ipmasklen"
    type = sqltypes.Integer()  # noqa: A003
    inherit_cache = True


class _IPAddrIPNetworkFunction(GenericFunction[IPNetwork]):
    """Returns the network part of an IP address."""

    name = "ipnetwork"
    type = CIDR()  # noqa: A003
    inherit_cache = True


class _IPAddrIPContainsFunction(GenericFunction[bool]):
    """Returns whether an IP address contains another IP address."""

    name = "ipcontains"
    type = sqltypes.Boolean()  # noqa: A003
    inherit_cache = True
