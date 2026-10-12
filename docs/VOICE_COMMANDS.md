# Voice Commands

| Phrase              | Action                       | Response                |
|---------------------|------------------------------|-------------------------|
| "Open workplace"    | Opens google.com             | "Opening workplace."    |
| "Open browser"      | Opens google.com             | "Launching browser."    |
| "Open YouTube"      | Opens youtube.com            | "Opening YouTube."      |
| "Open GitHub"       | Opens github.com             | "Opening GitHub."       |
| "Shutdown" / "Close"| Terminates the assistant     | "Shutting down."        |

## Adding a Command

1. Open `backend/command_router.py`.
2. Add an entry to `self.routes`:
   ```python
   ("your phrase", "Your response.", lambda: your_action())