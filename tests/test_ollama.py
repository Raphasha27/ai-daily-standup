def test_find_git_repos_not_in_git():
    from aids.cli import get_daily_commits
    result = get_daily_commits("/", "2026-06-01")
    assert result == ""
