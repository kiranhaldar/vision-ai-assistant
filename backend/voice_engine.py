"""Thread-safe speech recognition (STT) and text-to-speech (TTS)."""
import queue
import subprocess
import sys
import threading
from typing import Callable

import speech_recognition as sr

from backend.utils.logger import get_logger

log = get_logger(__name__)


class VoiceEngine:
    """Continuous background listening + non-blocking TTS."""

    def __init__(self, command_callback: Callable[[str], None]) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command_callback = command_callback
        self.stop_listening: Callable | None = None

        # TTS worker
        self.tts_queue: queue.Queue[str | None] = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()

        # Calibrate ambient noise once
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            log.info("Microphone calibrated.")
        except Exception as e:
            log.error("Mic calibration failed: %s", e)

    # ------------------------------------------------------------- listening
    def start_listening(self) -> None:
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, self._audio_callback
        )
        log.info("Background listening started.")

    def _audio_callback(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
        try:
            text = recognizer.recognize_google(audio).lower()
            log.info("Heard: %s", text)
            self.command_callback(text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            log.error("STT API error: %s", e)
        except Exception as e:
            log.error("Unexpected STT error: %s", e)

    # ------------------------------------------------------------ speaking
    def speak(self, text: str) -> None:
        """Queue text for non-blocking TTS."""
        self.tts_queue.put(text)

    def _tts_worker(self) -> None:
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            try:
                # Subprocess avoids pyttsx3 GIL/thread issues
                subprocess.run(
                    [sys.executable, "-c",
                     f"import pyttsx3; e=pyttsx3.init(); e.say({text!r}); e.runAndWait()"],
                    check=False, timeout=15,
                )
            except Exception as e:
                log.error("TTS error: %s", e)
            finally:
                self.tts_queue.task_done()

    def stop(self) -> None:
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.tts_queue.put(None)