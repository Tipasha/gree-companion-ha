"""Constants and address validation for Gree direct discovery."""

from ipaddress import IPv4Address

DOMAIN = "gree_direct"
CONF_HOSTS = "hosts"


def parse_hosts(value: str) -> list[IPv4Address]:
    """Parse a comma-separated list of unicast IPv4 destinations."""
    hosts = list(dict.fromkeys(IPv4Address(host.strip()) for host in value.split(",")))
    if not hosts or any(
        host.is_unspecified
        or host.is_multicast
        or host.is_loopback
        or host.is_reserved
        or host == IPv4Address("255.255.255.255")
        for host in hosts
    ):
        raise ValueError("Provide unicast IPv4 addresses")
    return hosts
