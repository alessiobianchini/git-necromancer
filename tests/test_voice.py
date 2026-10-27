import os
from unittest import mock
import pytest
from app.voice import synthesize_ghost_voice, get_audio_cache_path


def test_synthesize_ghost_voice_no_api_key():
    # If no API key is provided, should gracefully return None
    path = synthesize_ghost_voice("I am the ghost of forgotten commits.", api_key=None)
    assert path is None


def test_get_audio_cache_path():
    path = get_audio_cache_path("Sample ghost text", cache_dir="audio_cache")
    assert path.startswith("audio_cache")
    assert path.endswith(".mp3")


@mock.patch("requests.post")
def test_synthesize_ghost_voice_with_api_key(mock_post, tmp_path):
    mock_post.return_value.status_code = 200
    mock_post.return_value.content = b"fake-mp3-audio-bytes"

    cache_dir = str(tmp_path / "audio_cache")
    audio_path = synthesize_ghost_voice(
        "I was abandoned on a rainy Monday.",
        api_key="valid-test-key",
        voice_id="test-voice",
        cache_dir=cache_dir
    )

    assert audio_path is not None
    assert os.path.exists(audio_path)
    with open(audio_path, "rb") as f:
        assert f.read() == b"fake-mp3-audio-bytes"


@mock.patch("requests.post")
def test_synthesize_ghost_voice_cache_hit(mock_post, tmp_path):
    cache_dir = str(tmp_path / "audio_cache")
    os.makedirs(cache_dir, exist_ok=True)
    expected_path = get_audio_cache_path("Cached text", cache_dir=cache_dir)
    with open(expected_path, "wb") as f:
        f.write(b"cached-bytes")

    # When already cached, requests.post should NOT be called
    res = synthesize_ghost_voice("Cached text", api_key="valid-key", cache_dir=cache_dir)
    assert res == expected_path
    mock_post.assert_not_called()
