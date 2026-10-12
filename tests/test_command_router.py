"""Tests for voice-command routing (actions mocked)."""
from unittest.mock import patch

from backend.command_router import CommandRouter


def test_router_matches_open_browser():
    r = CommandRouter()
    with patch("backend.command_router.open_url") as mock_open:
        response, matched = r.route("please open browser now")
    assert matched
    assert "browser" in response.lower()
    mock_open.assert_called_once()


def test_router_no_match():
    r = CommandRouter()
    response, matched = r.route("random gibberish")
    assert not matched
    assert response == ""