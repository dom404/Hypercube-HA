"""Constants for HyperCube Nano integration."""
from typing import Final
from homeassistant.const import CONF_HOST, CONF_NAME

DOMAIN: Final = "hypercube_nano"
PLATFORMS: Final = ["light"]

DEFAULT_NAME: Final = "HyperCube Nano"
DEFAULT_PORT: Final = 80

# Configuration keys
CONF_PORT: Final = "port"

# Attributes
ATTR_EFFECT: Final = "effect"
ATTR_BRIGHTNESS: Final = "brightness"
ATTR_TRANSITION: Final = "transition"