"""ElevenLabs Ghost Voice synthesis: renders spectral code monologues into eerie audio."""

import hashlib
import logging
import os
from typing import Optional
import requests

logger = logging.getLogger("git-necromancer.voice")


def get_audio_cache_path(text: str, cache_dir: str = "audio_cache") -> str:
    """Compute a deterministic cache file path based on MD5 text hash."""
    text_hash = hashlib.md5(text.strip().encode("utf-8")).hexdigest()
    return os.path.join(cache_dir, f"ghost_{text_hash}.mp3")


def synthesize_ghost_voice(
    text: str,
    api_key: Optional[str] = None,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Default Rachel / atmospheric voice
    cache_dir: str = "audio_cache",
    timeout: float = 15.0
) -> Optional[str]:
    """Synthesize ghost voice using ElevenLabs TTS API with local disk caching."""
    if not api_key or not api_key.strip():
        logger.debug("ElevenLabs API key not configured; skipping audio synthesis")
        return None

    if not text or not text.strip():
        return None

    os.makedirs(cache_dir, exist_ok=True)
    cache_path = get_audio_cache_path(text, cache_dir=cache_dir)

    # Return cached audio if already generated
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        return cache_path

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.75,
            "style": 0.45,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        if response.status_code == 200 and response.content:
            with open(cache_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Ghost audio saved to {cache_path}")
            return cache_path
        else:
            logger.warning(f"ElevenLabs TTS failed with status {response.status_code}: {response.text[:200]}")
            return None
    except Exception as exc:
        logger.warning(f"Failed to generate ghost voice audio: {exc}")
        return None
