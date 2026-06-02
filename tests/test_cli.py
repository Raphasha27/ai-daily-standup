def test_get_daily_commits_no_repo():
    from aids.cli import get_daily_commits
    result = get_daily_commits("/nonexistent/path", "2026-06-02")
    assert result == ""
