"""The HyperCube Nano integration."""
from __future__ import annotations

import logging
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HyperCube Nano from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Forward the setup to the light platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload the light platform
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "light")
    
    # Remove the entry from hass.data if successful
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok