"""Discover Gree units directly when Wi-Fi filters broadcast packets."""

from datetime import datetime, timedelta
import logging

from homeassistant.components.gree.coordinator import GreeConfigEntry
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.event import async_track_time_interval

from .const import CONF_HOSTS, parse_hosts

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Send direct probes through the built-in integration's discovery socket."""
    hosts = parse_hosts(entry.data[CONF_HOSTS])

    async def async_scan(_now: datetime | None = None) -> None:
        # Resolve entries on each scan so a Gree reload cannot leave a stale socket.
        gree_entries: list[GreeConfigEntry] = [
            item
            for item in hass.config_entries.async_entries("gree")
            if item.state is ConfigEntryState.LOADED
        ]
        if not gree_entries:
            raise ConfigEntryNotReady("The built-in Gree integration is not loaded")
        for gree_entry in gree_entries:
            await gree_entry.runtime_data.discovery_service.discovery.scan(
                0, bcast_ifaces=hosts
            )

    await async_scan()

    async def async_periodic_scan(now: datetime) -> None:
        try:
            await async_scan(now)
        except ConfigEntryNotReady:
            _LOGGER.warning("Skipping direct discovery: Gree is not loaded")
        except OSError:
            _LOGGER.exception("Unable to send Gree direct-discovery probes")

    entry.async_on_unload(
        async_track_time_interval(hass, async_periodic_scan, timedelta(seconds=60))
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove only our timer; Gree owns its discovery socket and entities."""
    return True
