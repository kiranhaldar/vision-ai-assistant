"""Safe wrappers for OS-level actions (browser, subprocess)."""
import subprocess
import webbrowser
from typing import Sequence

from backend.utils.logger import get_logger

log = get_logger(__name__)


def open_url(url: str) -> bool:
    """Open a URL in the default browser."""
    try:
        webbrowser.open(url)
        log.info("Opened URL: %s", url)
        return True
    except Exception as e:
        log.error("Failed to open URL %s: %s", url, e)
        return False


def launch_app(command: Sequence[str] | str, shell: bool = False) -> bool:
    """Launch a desktop app via subprocess."""
    try:
        subprocess.Popen(command, shell=shell)
        log.info("Launched: %s", command)
        return True
    except Exception as e:
        log.error("Failed to launch %s: %s", command, e)
        return False


def shutdown_system() -> None:
    """Gracefully terminate the Vision process."""
    log.warning("Shutdown requested.")
    raise SystemExit(0)