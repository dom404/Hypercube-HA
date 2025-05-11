"""Support for HyperCube Nano lights."""
from __future__ import annotations

import logging
import aiohttp
import asyncio
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_TRANSITION,
    COLOR_MODE_RGB,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

EFFECT_LIST = [
    "Mode: Kaleidoscopic",
    "Mode: Calm",
    # ... [all your effects] ...
]

class HyperCubeNanoLight(LightEntity):
    """Representation of a HyperCube Nano light."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_color_modes = {COLOR_MODE_RGB}
    _attr_color_mode = COLOR_MODE_RGB
    _attr_supported_features = LightEntityFeature.TRANSITION | LightEntityFeature.EFFECT
    _attr_effect_list = EFFECT_LIST

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the light."""
        self._entry = entry
        self._host = entry.data[CONF_HOST]
        self._port = entry.data.get(CONF_PORT, DEFAULT_PORT)
        self._name = entry.data.get(CONF_NAME, DEFAULT_NAME)
        self._state = False
        self._brightness = 150
        self._effect = None
        self._rgb_color = [179, 23, 158]
        self._transition = 500
        self._session = aiohttp.ClientSession()
        self._available = True

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"hypercube_nano_{self._host}_{self._port}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            manufacturer="Hyperspace",
            model="HyperCube Nano",
            name=self._name,
            sw_version="hs-1.6",
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._state

    @property
    def brightness(self) -> int:
        """Return the brightness of the light."""
        return self._brightness

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value."""
        return self._rgb_color

    @property
    def effect(self) -> str | None:
        """Return the current effect."""
        return self._effect

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on or control the light."""
        data = {"on": True}

        if ATTR_BRIGHTNESS in kwargs:
            data["bri"] = kwargs[ATTR_BRIGHTNESS]

        if ATTR_EFFECT in kwargs:
            effect = kwargs[ATTR_EFFECT]
            if effect in EFFECT_LIST:
                effect_index = EFFECT_LIST.index(effect)
                data["seg"] = [{"fx": effect_index}]

        if ATTR_TRANSITION in kwargs:
            data["transition"] = kwargs[ATTR_TRANSITION]

        await self._send_command(data)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        data = {"on": False}
        if ATTR_TRANSITION in kwargs:
            data["transition"] = kwargs[ATTR_TRANSITION]
        await self._send_command(data)

    async def async_update(self) -> None:
        """Fetch new state data for this light."""
        try:
            async with self._session.get(
                f"http://{self._host}:{self._port}/json",
                timeout=5
            ) as response:
                data = await response.json()
                self._state = data["state"]["on"]
                self._brightness = data["state"]["bri"]
                
                if "seg" in data["state"] and len(data["state"]["seg"]) > 0:
                    segment = data["state"]["seg"][0]
                    if "col" in segment and len(segment["col"]) > 0:
                        self._rgb_color = segment["col"][0]
                    if "fx" in segment:
                        fx_index = segment["fx"]
                        if fx_index < len(EFFECT_LIST):
                            self._effect = EFFECT_LIST[fx_index]
                
                self._available = True
        except Exception as ex:
            _LOGGER.error("Error updating: %s", ex)
            self._available = False

    async def _send_command(self, data: dict) -> None:
        """Send command to the light."""
        try:
            async with self._session.post(
                f"http://{self._host}:{self._port}/json",
                json=data,
                timeout=5
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Command failed: %s", response.status)
                await self.async_update()
        except Exception as ex:
            _LOGGER.error("Error sending command: %s", ex)
            self._available = False

    async def async_will_remove_from_hass(self) -> None:
        """Clean up resources."""
        await super().async_will_remove_from_hass()
        if hasattr(self, '_session') and self._session:
            await self._session.close()
        _LOGGER.debug("Cleanup completed")

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HyperCube Nano light from a config entry."""
    async_add_entities([HyperCubeNanoLight(entry)])