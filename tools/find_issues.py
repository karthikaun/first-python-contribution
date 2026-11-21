"""List beginner-friendly issues that nobody seems to be working on (Lesson 07).

Usage::

    python3 tools/find_issues.py
    python3 tools/find_issues.py --label "help wanted" --days 30 --min-stars 500
    python3 tools/find_issues.py --repo pallets/flask

Uses the GitHub CLI (``gh``, logged in: Lesson 02). First it finds active
Python repositories with enough stars and open good-first issues. Then, in
those repositories, it searches for open issues that are labelled for
newcomers, unassigned, not linked to a pull request and recently active. It
drops issues that an open PR mentions, and flags issues where a comment
already says someone is on it.

These are *candidates*. Always read the whole issue thread before claiming one.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys

QUERY = """
query($q: String!, $n: Int!) {
  search(query: $q, type: ISSUE, first: $n) {
    nodes {
      ... on Issue {
        title
        url
        createdAt
        comments(last: 10) { totalCount nodes { body } }
        repository {
          nameWithOwner
          stargazerCount
          pushedAt
          isArchived
          contributingGuidelines { url }
        }
        timelineItems(itemTypes: [CROSS_REFERENCED_EVENT], last: 20) {
          nodes { ... on CrossReferencedEvent { source { ... on PullRequest { state } } } }
        }
      }
    }
  }
}
"""

REPO_QUERY = """
query($q: String!, $n: Int!) {
  search(query: $q, type: REPOSITORY, first: $n) {
    nodes { ... on Repository { nameWithOwner } }
  }
}
"""
MAX_QUERY_CHARS = 250  # GitHub rejects search queries over 256 characters

CLAIM_RE = re.compile(
    r"\b(i'?d like to|i want to|i'?ll|i will|can i|could i|may i|let me)\b[^.?!\n]{0,40}"
    r"\b(work on|take|tackle|pick up|fix|handle)\b|\bassign (this|it) to me\b|\bworking on (this|it)\b",
    re.IGNORECASE,
)


def build_repo_query(language: str, min_stars: int, today: dt.date) -> str:
    since = (today - dt.timedelta(days=30)).isoformat()
    return (
        f"language:{language} stars:>={min_stars} good-first-issues:>=1 "
        f"pushed:>={since} archived:false sort:updated-desc"
    )


def build_query(label: str, repos: list[str], days: int, today: dt.date) -> str:
    since = (today - dt.timedelta(days=days)).isoformat()
    parts = ["is:issue", "is:open", f'label:"{label}"', "no:assignee", "-linked:pr", f"updated:>={since}"]
    parts.extend(f"repo:{r}" for r in repos)
    return " ".join(parts)


def looks_claimed(comment_bodies: list[str]) -> bool:
    return any(CLAIM_RE.search(body or "") for body in comment_bodies)


def has_open_pr(issue: dict) -> bool:
    for node in issue.get("timelineItems", {}).get("nodes", []):
        if (node.get("source") or {}).get("state") == "OPEN":
            return True
    return False


def summarise(issue: dict, today: dt.date) -> dict:
    repo = issue["repository"]
    created = dt.date.fromisoformat(issue["createdAt"][:10])
    pushed = dt.date.fromisoformat(repo["pushedAt"][:10]) if repo.get("pushedAt") else None
    bodies = [c.get("body", "") for c in issue["comments"]["nodes"]]
    return {
        "repo": repo["nameWithOwner"],
        "stars": repo["stargazerCount"],
        "title": issue["title"],
        "url": issue["url"],
        "age_days": (today - created).days,
        "comments": issue["comments"]["totalCount"],
        "repo_pushed_days": (today - pushed).days if pushed else None,
        "contributing": bool(repo.get("contributingGuidelines")),
        "claimed": looks_claimed(bodies),
        "open_pr": has_open_pr(issue),
        "archived": repo.get("isArchived", False),
    }


def keep(row: dict, min_stars: int, show_claimed: bool) -> bool:
    if row["archived"] or row["open_pr"] or row["stars"] < min_stars:
        return False
    if row["repo_pushed_days"] is not None and row["repo_pushed_days"] > 90:
        return False
    return show_claimed or not row["claimed"]


def _graphql(query: str, q: str, n: int) -> list[dict]:
    if not shutil.which("gh"):
        sys.exit("This needs the GitHub CLI (gh). See Lesson 02.")
    proc = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"q={q}", "-F", f"n={n}"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"gh couldn't search GitHub:\n{proc.stderr.strip()}\nIs gh logged in? Try: gh auth status")
    nodes = json.loads(proc.stdout)["data"]["search"]["nodes"]
    return [node for node in nodes if node]  # empty dicts are other result types


def find_repos(language: str, min_stars: int, count: int, today: dt.date) -> list[str]:
    return [r["nameWithOwner"] for r in _graphql(REPO_QUERY, build_repo_query(language, min_stars, today), count)]


def batches(repos: list[str], label: str, days: int, today: dt.date) -> list[list[str]]:
    """Group repositories so each issue search query stays under GitHub's length limit."""
    groups: list[list[str]] = []
    for repo in repos:
        if groups and len(build_query(label, [*groups[-1], repo], days, today)) <= MAX_QUERY_CHARS:
            groups[-1].append(repo)
        else:
            groups.append([repo])
    return groups


def format_row(row: dict) -> str:
    flags = []
    if not row["contributing"]:
        flags.append("no CONTRIBUTING file")
    if row["claimed"]:
        flags.append("someone may be on it")
    extra = f"  [{'; '.join(flags)}]" if flags else ""
    return (
        f"{row['repo']} (★{row['stars']})  {row['title']}\n"
        f"    {row['url']}\n"
        f"    opened {row['age_days']} days ago, {row['comments']} comments{extra}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find beginner-friendly issues nobody seems to be working on.")
    parser.add_argument("--label", default="good first issue")
    parser.add_argument("--language", default="python")
    parser.add_argument("--repo", help="search one repository, e.g. pallets/flask")
    parser.add_argument("--days", type=int, default=180, help="only issues updated in the last N days")
    parser.add_argument("--min-stars", type=int, default=500)
    parser.add_argument("--repos", type=int, default=30, help="how many active repositories to search")
    parser.add_argument("--per-batch", type=int, default=20, help="issues to fetch per batch of repositories")
    parser.add_argument("--show-claimed", action="store_true", help="include issues where someone may be on it")
    args = parser.parse_args(argv)

    today = dt.date.today()
    if args.repo:
        repos, min_stars = [args.repo], 0
    else:
        print(f"Finding active {args.language} projects with {args.min_stars}+ stars and good first issues...")
        repos, min_stars = find_repos(args.language, args.min_stars, args.repos, today), args.min_stars
    rows = []
    for group in batches(repos, args.label, args.days, today):
        rows.extend(
            summarise(i, today)
            for i in _graphql(QUERY, build_query(args.label, group, args.days, today), args.per_batch)
        )
    print(f"Searched {len(repos)} repositories.\n")
    kept = [r for r in rows if keep(r, min_stars, args.show_claimed)]
    kept.sort(key=lambda r: (not r["contributing"], r["comments"], r["age_days"]))
    for row in kept:
        print(format_row(row) + "\n")
    print(f"{len(kept)} of {len(rows)} issues look free. Read each thread fully before you claim one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
