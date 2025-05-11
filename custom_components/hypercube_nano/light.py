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
    "Mode: Sound Reactive",
    "Hyper-Rainbow",
    "Supernova",
    "Entropy Engine",
    "Photonic Accelerator",
    "Grand Prismatic",
    "Orbital Loop",
    "Strange Attractor",
    "Warp Core",
    "Chromatic Precession",
    "Singularity",
    "Time Warp",
    "Gamma Ray Burst",
    "Gravitational Wave",
    "Divergence",
    "Superconductor",
    "Achromatic Shift",
    "Prismatic Pulse",
    "Dazzle Blaster",
    "Hyperbolic Manifold",
    "Core Collapse",
    "Atomic Generator",
    "Flux Capacitor",
    "Quasar",
    "Stellar Reactor",
    "Rainbow Cannon",
    "Solar Flare",
    "Cosmic Rays",
    "Ionization",
    "Fusion Core",
    "Hypernova",
    "Superluminal",
    "Superposition",
    "Chromatic Wave",
    "Pulsar",
    "Quantum Instability",
    "Dielectric Breakdown",
    "Photonic Pulse",
    "Luminous Scatter",
    "Magnetar",
    "Scintillation",
    "Breathing",
    "Continuum",
    "Dynamo",
    "Comets",
    "Synchrotron",
    "Phase Wipe",
    "Nucleus",
    "Twinkle",
    "Prismatic Alignment",
    "Stable Isotope",
    "Luminous Ether",
    "Photonic Core",
    "Equilibration",
    "Plasma Field",
    "Serenity",
    "Chromatic Flux",
    "Convergence",
    "Shimmer",
    "Celestial",
    "Zenith",
    "Ignition",
    "Pacifica",
    "Spectral Shift",
    "Solid",
    "Harmonic Accelerator",
    "Sonic Superposition",
    "Sonic Sparkle",
    "Spectrogram Alpha",
    "Resonant Precession",
    "Aural Dynamo",
    "Hypersonic",
    "Resonance Engine",
    "Rainbow Symphony",
    "Melodic Fusion",
    "Spectrogram Beta",
    "Ultrasonic Arc",
    "Rhythmic Orbital",
    "Tonal Entanglement",
    "Synesthesia",
    "Spectrogram Delta",
    "Chromatic Soundwave",
    "Harmonic Ripple",
    "Sonic Superconductor",
    "Spectrogram Gamma",
    "Dynamic Precession",
    "Light Sound Dance",
    "Beat Shift",
    "Phase Helix",
    "Symphonic Wave",
    "Sound Smash",
    "Hypersonic Orbit",
    "Achromatic Harmony",
    "Acoustic Ignition",
    "Ultra Sound",
    "Spectral Resonator",
]

PALETTE_LIST: Final[list[str]] = [
    "Default",
    "Custom",
    "Aurora",
    "Aurora II",
    "C9",
    "Chromatic",
    "Chromatic II",
    "Forest",
    "Green Giant",
    "Harmonious",
    "Kaleidoscope I",
    "Kaleidoscope II",
    "Lava",
    "Luminous",
    "Molten Sea",
    "Nebula",
    "Neptune",
    "Ocean",
    "Pastel",
    "Red Titan",
    "Solar Skys",
    "Spectral",
    "Stellar Flare",
    "Sunset",
    "Tiamat",
    "Ultraviolet",
    "Yelblu"
]

class HyperCubeNanoLight(LightEntity):
    """Representation of a HyperCube Nano light."""

    _attr_has_entity_name = True
    _attr_supported_color_modes = {COLOR_MODE_RGB}
    _attr_supported_features = LightEntityFeature.TRANSITION | LightEntityFeature.EFFECT
    _attr_effect_list = EFFECT_LIST

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the light."""
        self._entry = entry
        self._host = entry.data[CONF_HOST]
        self._port = entry.data.get("port", DEFAULT_PORT)
        self._attr_name = entry.data.get(CONF_NAME, DEFAULT_NAME)
        self._attr_unique_id = f"hypercube_{self._host}_{self._port}"
        self._state = False
        self._brightness = 254  # Default to max brightness
        self._effect = None
        self._rgb_color = [255, 255, 255]  # Default to white
        self._session = aiohttp.ClientSession()
        self._available = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            manufacturer="Hyperspace",
            model="HyperCube Nano",
            name=self._attr_name,
            sw_version="hs-1.6",
            configuration_url=f"http://{self._host}:{self._port}",
        )

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

    async def _send_command(self, data: dict) -> bool:
        """Send command to the HyperCube device."""
        url = f"http://{self._host}:{self._port}/json"
        _LOGGER.debug("Sending command to %s: %s", url, data)
        
        try:
            async with self._session.post(
                url,
                json=data,
                timeout=5
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    _LOGGER.error("Command failed with status %s: %s", response.status, error_text)
                    return False
                
                result = await response.json()
                _LOGGER.debug("Command response: %s", result)
                return True
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error sending command: %s", err)
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout sending command to device")
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
        
        self._available = False
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on or control the light."""
        data = {"on": True, "bri": self._brightness}
        
        if ATTR_BRIGHTNESS in kwargs:
            data["bri"] = kwargs[ATTR_BRIGHTNESS]
        
        if ATTR_EFFECT in kwargs:
            effect = kwargs[ATTR_EFFECT]
            if effect in EFFECT_LIST:
                data["seg"] = [{"fx": EFFECT_LIST.index(effect)}]
        
        if ATTR_TRANSITION in kwargs:
            data["transition"] = kwargs[ATTR_TRANSITION]
        
        if await self._send_command(data):
            self._state = True
            if ATTR_BRIGHTNESS in kwargs:
                self._brightness = kwargs[ATTR_BRIGHTNESS]
            if ATTR_EFFECT in kwargs:
                self._effect = kwargs[ATTR_EFFECT]
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        data = {"on": False}
        
        if ATTR_TRANSITION in kwargs:
            data["transition"] = kwargs[ATTR_TRANSITION]
        
        if await self._send_command(data):
            self._state = False
            self.async_write_ha_state()

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
                _LOGGER.debug("State updated: %s", data)
        except Exception as ex:
            _LOGGER.error("Error updating state: %s", ex)
            self._available = False

    async def async_will_remove_from_hass(self) -> None:
        """Clean up resources."""
        await super().async_will_remove_from_hass()
        if hasattr(self, '_session') and self._session:
            await self._session.close()
        _LOGGER.debug("Cleanup completed for HyperCube Nano")

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HyperCube Nano light from a config entry."""
    async_add_entities([HyperCubeNanoLight(entry)])