"""Maps recognized voice phrases to system actions."""
from backend.utils.logger import get_logger
from backend.utils.system_actions import open_url, shutdown_system

log = get_logger(__name__)


class CommandRouter:
    """Routes voice commands to callbacks."""

    def __init__(self) -> None:
        # Ordered list: (keyword, response_text, action_callable)
        self.routes = [
            ("open workplace", "Opening workplace.",
             lambda: open_url("https://www.google.com")),
            ("open browser", "Launching browser.",
             lambda: open_url("https://www.google.com")),
            ("open youtube", "Opening YouTube.",
             lambda: open_url("https://www.youtube.com")),
            ("open github", "Opening GitHub.",
             lambda: open_url("https://www.github.com")),
            ("shutdown", "Shutting down.", shutdown_system),
            ("close", "Shutting down.", shutdown_system),
        ]

    def route(self, text: str) -> tuple[str, bool]:
        """Return (spoken_response, was_matched)."""
        for keyword, response, action in self.routes:
            if keyword in text:
                try:
                    action()
                    return response, True
                except SystemExit:
                    raise
                except Exception as e:
                    log.error("Action for '%s' failed: %s", keyword, e)
                    return f"Command failed: {keyword}", False
        return "", False