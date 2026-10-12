"""Mock-based tests for the voice engine (no actual mic/audio)."""
from unittest.mock import MagicMock, patch

from backend.voice_engine import VoiceEngine


@patch("backend.voice_engine.sr.Microphone")
@patch("backend.voice_engine.sr.Recognizer")
def test_speak_enqueues_text(mock_rec, mock_mic):
    engine = VoiceEngine(command_callback=MagicMock())
    engine.speak("hello")
    # Queue should contain the text
    assert engine.tts_queue.qsize() >= 1
    engine.stop()