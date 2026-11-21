import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import find_issues as fi  # noqa: E402

TODAY = dt.date(2026, 11, 21)


def issue(comments=(), pr_states=(), stars=1000, pushed="2026-11-20", contributing=True, archived=False):
    return {
        "title": "Fix the thing",
        "url": "https://github.com/o/r/issues/1",
        "createdAt": "2026-11-01T10:00:00Z",
        "comments": {"totalCount": len(comments), "nodes": [{"body": c} for c in comments]},
        "repository": {
            "nameWithOwner": "o/r",
            "stargazerCount": stars,
            "pushedAt": f"{pushed}T00:00:00Z",
            "isArchived": archived,
            "contributingGuidelines": {"url": "u"} if contributing else None,
        },
        "timelineItems": {"nodes": [{"source": {"state": s}} for s in pr_states]},
    }


def test_issue_query_has_all_filters():
    q = fi.build_query("good first issue", ["a/b", "c/d"], 60, TODAY)
    for part in [
        'label:"good first issue"',
        "no:assignee",
        "-linked:pr",
        "updated:>=2026-09-22",
        "repo:a/b",
        "repo:c/d",
    ]:
        assert part in q


def test_repo_query():
    q = fi.build_repo_query("python", 500, TODAY)
    assert "language:python" in q and "stars:>=500" in q and "good-first-issues:>=1" in q


def test_batches_respect_query_length():
    repos = [f"owner{i}/{'r' * 30}" for i in range(12)]
    groups = fi.batches(repos, "good first issue", 60, TODAY)
    assert sum(groups, []) == repos
    assert len(groups) > 1
    for group in groups:
        assert len(fi.build_query("good first issue", group, 60, TODAY)) <= fi.MAX_QUERY_CHARS


@pytest.mark.parametrize(
    "text",
    [
        "Hi, I'd like to work on this!",
        "Can I take this one?",
        "please assign this to me",
        "I'm working on it now",
        "I'll fix it",
    ],
)
def test_claims_detected(text):
    assert fi.looks_claimed([text])


@pytest.mark.parametrize("text", ["This also happens on 3.12.", "Thanks for the report", "Is this still a problem?"])
def test_ordinary_comments_not_claims(text):
    assert not fi.looks_claimed([text])


def test_summarise_and_keep():
    row = fi.summarise(issue(), TODAY)
    assert row["age_days"] == 20 and row["contributing"] and not row["claimed"]
    assert fi.keep(row, 500, show_claimed=False)


def test_open_pr_or_closed_pr():
    assert not fi.keep(fi.summarise(issue(pr_states=["OPEN"]), TODAY), 0, False)
    assert fi.keep(fi.summarise(issue(pr_states=["CLOSED", "MERGED"]), TODAY), 0, False)


def test_filters_stars_stale_archived_claimed():
    assert not fi.keep(fi.summarise(issue(stars=10), TODAY), 500, False)
    assert not fi.keep(fi.summarise(issue(pushed="2026-01-01"), TODAY), 0, False)
    assert not fi.keep(fi.summarise(issue(archived=True), TODAY), 0, False)
    claimed = fi.summarise(issue(comments=["can I work on this?"]), TODAY)
    assert not fi.keep(claimed, 0, False)
    assert fi.keep(claimed, 0, True)


def test_format_row_flags():
    text = fi.format_row(fi.summarise(issue(contributing=False, comments=["I'd like to take this"]), TODAY))
    assert "no CONTRIBUTING file" in text and "someone may be on it" in text
