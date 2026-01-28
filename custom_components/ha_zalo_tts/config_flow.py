from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "ha_zalo_tts"

class ZaloTTSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Zalo TTS",
                data={"api_key": user_input["api_key"]},
            )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("api_key"): str}),
        )
