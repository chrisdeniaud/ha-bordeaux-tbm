"""Config flow for Bordeaux TBM."""
from __future__ import annotations

from typing import Any
from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, CONF_LINE, CONF_STOP, CONF_DIRECTION, CONF_PREDICTIONS, CONF_SCAN_INTERVAL, DEFAULT_PREDICTIONS, DEFAULT_SCAN_INTERVAL
from .tbm_api import get_lines, get_stops_for_line

class BordeauxTBMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bordeaux TBM."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_LINE]}_{user_input[CONF_STOP]}_{user_input[CONF_DIRECTION]}")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=f"TBM {user_input[CONF_LINE]} - {user_input[CONF_STOP]}",
                data=user_input
            )

        lines = await self.hass.async_add_executor_job(get_lines)
        line_options = {line['LineRef']['value']: f"{line['LineRef']['value']} - {line['LineName'][0]['value']}" 
                       for line in lines}
        
        stops = await self.hass.async_add_executor_job(get_stops_for_line)
        stop_options = {stops['StopAreaRef']['value']: f"{stops['StopAreaRef']['value']} - {stops['StopName']['value']}" 
                       for stop in stops}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LINE): vol.In(line_options),
                vol.Required(CONF_STOP): vol.In(stop_options), # str,
                vol.Required(CONF_DIRECTION, default="1"): vol.In({
                    "0": "Direction 0",
                    "1": "Direction 1"
                }),
                vol.Required(CONF_PREDICTIONS, default=DEFAULT_PREDICTIONS): 
                    vol.All(vol.Coerce(int), vol.Range(min=1, max=5)),
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL):
                    vol.All(vol.Coerce(int), vol.Range(min=10, max=3600))
            }),
            errors=errors
        )