import logging
import requests
import re
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry

DOMAIN = "ha_zalo_tts"
SERVICE_SAY = "say"

_LOGGER = logging.getLogger(__name__)

def limit_message_size(message: str) -> str:
    message = re.sub(r"\s+", " ", message).replace("\n", " ")
    return message[:1980]

def zalo_tts(api_key, speed, voice, message):
    api_url = "https://api.zalo.ai/v1/tts/synthesize"
    headers = {"apikey": api_key}
    payload = {
        "input": limit_message_size(message),
        "speed": str(speed),
        "encode_type": "1",
        "speaker_id": str(voice),
    }
    response = requests.post(api_url, headers=headers, data=payload, timeout=10)
    data = response.json()
    return data.get("data", {}).get("url")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    api_key = entry.data["api_key"]

    async def handle_say(call: ServiceCall):
        message = call.data.get("message")
        entity_id = call.data.get("entity_id")
        voice = call.data.get("voice", 1)
        speed = call.data.get("speed", 1.0)

        audio_url = await hass.async_add_executor_job(
            zalo_tts, api_key, speed, voice, message
        )

        if not audio_url:
            _LOGGER.error("Zalo TTS failed")
            return

        hass.services.call(
            "media_player",
            "play_media",
            {
                "entity_id": entity_id,
                "media_content_id": audio_url,
                "media_content_type": "music",
            },
        )

    hass.services.async_register(DOMAIN, SERVICE_SAY, handle_say)
    return True
