"""Configure direct discovery without replacing existing Gree entities."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_HOSTS, DOMAIN, parse_hosts


class GreeDirectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure the AC addresses used for unicast discovery."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Create a single direct-discovery helper."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        return await self._async_form(user_input, "user")

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Update addresses after a network or DHCP change."""
        return await self._async_form(user_input, "reconfigure")

    async def _async_form(
        self, user_input: dict[str, Any] | None, step_id: str
    ) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                hosts = parse_hosts(user_input[CONF_HOSTS])
            except ValueError:
                errors[CONF_HOSTS] = "invalid_hosts"
            else:
                data = {CONF_HOSTS: ", ".join(str(host) for host in hosts)}
                if step_id == "reconfigure":
                    return self.async_update_reload_and_abort(
                        self._get_reconfigure_entry(), data_updates=data
                    )
                return self.async_create_entry(title="Gree Direct Discovery", data=data)

        default = ""
        if step_id == "reconfigure":
            default = self._get_reconfigure_entry().data[CONF_HOSTS]
        if user_input is not None:
            default = user_input[CONF_HOSTS]
        return self.async_show_form(
            step_id=step_id,
            data_schema=vol.Schema({vol.Required(CONF_HOSTS, default=default): str}),
            errors=errors,
        )
