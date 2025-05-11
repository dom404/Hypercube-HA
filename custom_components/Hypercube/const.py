"""Constants for HyperCube Nano integration."""
from typing import Final

DOMAIN: Final = "hypercube_nano"

# Default configuration
DEFAULT_NAME: Final = "HyperCube Nano"
DEFAULT_PORT: Final = 80  # Place holder for port
DEFAULT_TRANSITION: Final = 500  # Default transition time in ms

# Configuration keys
CONF_HOST: Final = "host"
CONF_PORT: Final = "port"
CONF_NAME: Final = "name"

# Attribute keys
ATTR_EFFECT: Final = "effect"
ATTR_PALETTE: Final = "palette"
ATTR_BRIGHTNESS: Final = "brightness"
ATTR_TRANSITION: Final = "transition"
ATTR_SEGMENT: Final = "segment"
ATTR_SPEED: Final = "speed"        # Effect speed (ix in JSON)
ATTR_INTENSITY: Final = "intensity" # Effect intensity (sx in JSON)
ATTR_PALETTE_ID: Final = "palette_id"  # Actual palette ID used in commands

# Service names
SERVICE_SET_EFFECT: Final = "set_effect"
SERVICE_SET_PALETTE: Final = "set_palette"

# API endpoints
API_JSON_ENDPOINT: Final = "/json"
API_STATE_ENDPOINT: Final = "/state"

# Device info constants
MANUFACTURER: Final = "Hyperspace"
MODEL: Final = "HyperCube Nano"
SW_VERSION: Final = "hs-1.6"

# Default effect/palette values
DEFAULT_EFFECT: Final = "Solid"
DEFAULT_PALETTE: Final = "Default"

# Timeouts
API_TIMEOUT: Final = 5  # seconds