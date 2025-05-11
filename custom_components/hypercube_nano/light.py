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
    "Spectral Resonator"
]

PALETTE_LIST = [
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
    """Set up HyperCube Nano light from a config entry."""
    async_add_entities([HyperCubeNanoLight(entry)])

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
        self._port = entry.data.get("port", 80)
        self._name = entry.data.get(CONF_NAME, "HyperCube Nano")
        self._state = False
        self._brightness = 150
        self._effect = None
        self._rgb_color = [179, 23, 158]
        self._transition = 500
        self._speed = 123
        self._intensity = 9
        self._palette = 20
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
            configuration_url=f"http://{self._host}:{self._port}",
        )

    # ... [rest of the light.py implementation remains the same as previous]