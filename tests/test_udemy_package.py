import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import udemy_package as up  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def test_real_landing_page_meets_udemy_limits():
    landing = up.parse_landing(up.LANDING.read_text())
    assert up.landing_problems(landing) == []
    assert isinstance(landing["What you'll learn"], list)


def test_landing_problems_reported():
    landing = {
        "Title": "x" * 61 + " Udemy",
        "Subtitle": "y" * 121,
        "Description": "too short",
        "What you'll learn": ["one"],
    }
    problems = up.landing_problems(landing)
    for expected in ("title is", "Udemy", "subtitle is", "description is", "at least 4", "missing section"):
        assert any(expected in p for p in problems), (expected, problems)


def test_sections_follow_the_curriculum():
    sections = up.parse_sections((ROOT / "CURRICULUM.md").read_text(), ROOT / "lessons")
    assert [s.title for s in sections][0] == "Your first PR, today"
    lectures = [lec for s in sections for lec in s.lectures]
    assert len(lectures) == 14
    assert lectures[0].title == "What counts as a contribution"
    assert lectures[-1].folder == "A-troubleshooting"
    assert all(len(lec.title) <= up.LECTURE_TITLE_MAX for lec in lectures)


def test_lecture_file_names_are_safe():
    lec = up.Lecture(13, "13-capstone", "Capstone: your first external contribution")
    assert lec.stem == "13 - Capstone - your first external contribution"


def test_srt_to_vtt():
    vtt = up.srt_to_vtt("1\r\n00:00:00,000 --> 00:00:03,420\r\nHello\r\n")
    assert vtt.startswith("WEBVTT\n\n1\n00:00:00.000 --> 00:00:03.420\nHello")
