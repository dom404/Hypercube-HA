"""Support for HyperCube Nano lights."""
from __future__ import annotations

import logging
import aiohttp
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
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_PORT

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

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the light platform."""
    # Create the device outside the entity constructor
    host = entry.data[CONF_HOST]
    port = entry.data.get("port", DEFAULT_PORT)
    
    # Initialize the light entity
    light = HyperCubeNanoLight(entry, host, port)
    async_add_entities([light])

class HyperCubeNanoLight(LightEntity):
    """Representation of a HyperCube Nano light."""

    _attr_has_entity_name = True
    _attr_supported_color_modes = {COLOR_MODE_RGB}
    _attr_supported_features = LightEntityFeature.TRANSITION | LightEntityFeature.EFFECT
    _attr_effect_list = EFFECT_LIST

    def __init__(self, entry: ConfigEntry, host: str, port: int) -> None:
        """Initialize."""
        self._entry = entry
        self._host = host
        self._port = port
        self._attr_name = entry.data.get("name", "HyperCube Nano")
        self._attr_unique_id = f"hypercube_{host}_{port}"
        self._state = False
        self._brightness = 150
        self._effect = None
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
        )

    async def async_update(self) -> None:
        """Fetch new state data."""
        try:
            async with self._session.get(
                f"http://{self._host}:{self._port}/json",
                timeout=5
            ) as response:
                data = await response.json()
                self._state = data["state"]["on"]
                self._brightness = data["state"]["bri"]
                # ... [rest of state update] ...
        except Exception as ex:
            _LOGGER.error("Update failed: %s", ex)
            self._available = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        # ... [implementation] ...

    async def async_will_remove_from_hass(self) -> None:
        """Clean up resources."""
        await self._session.close()