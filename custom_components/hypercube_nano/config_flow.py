"""Config flow for HyperCube Nano."""
from __future__ import annotations

import logging
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Optional("port", default=DEFAULT_PORT): int,
})

class HyperCubeNanoFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a HyperCube Nano config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(
                    f"http://{user_input[CONF_HOST]}:{user_input.get('port', DEFAULT_PORT)}/json",
                    timeout=5
                ) as response:
                    await response.json()

                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=user_input,
                )
            except Exception as err:
                _LOGGER.error("Connection error: %s", err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )