"""Tests for ai_daily_standup."""
import pytest
from unittest.mock import patch, MagicMock
from ai_daily_standup import query_ollama, get_git_activity

class TestGetGitActivity:
    def test_returns_string(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "abc1234 feat: add feature"
            mock_run.return_value.returncode = 0
            result = get_git_activity(24)
            assert "abc1234" in result

    def test_empty_activity(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = ""
            mock_run.return_value.returncode = 0
            result = get_git_activity(1)
            assert isinstance(result, str)

class TestQueryOllama:
    def test_generates_standup(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"response": "Yesterday I worked on..."}
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.return_value = mock_resp
            result = query_ollama("activity log")
            assert "Yesterday" in result

    def test_handles_error(self):
        with patch("httpx.Client") as mock_client:
            mock_client.return_value.__enter__.return_value.post.side_effect = Exception
            result = query_ollama("activity")
            assert "Error" in result
