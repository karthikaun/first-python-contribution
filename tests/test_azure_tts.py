"""Azure narration: no network here. The service calls are replaced with fakes."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import azure_tts  # noqa: E402

VOICE = "en-IN-Arjun:DragonHDLatestNeural"


def test_azure_voices_are_told_from_macos_voices():
    assert azure_tts.is_azure_voice(VOICE)
    assert azure_tts.is_azure_voice("en-IN-AaravNeural")
    assert not azure_tts.is_azure_voice("Aman")
    assert not azure_tts.is_azure_voice("Samantha")


def test_ssml_escapes_the_text_and_uses_the_voices_locale():
    xml = azure_tts.ssml("Fix <it> & commit", VOICE)
    assert "Fix &lt;it&gt; &amp; commit" in xml
    assert "xml:lang='en-IN'" in xml and f"name='{VOICE}'" in xml


@pytest.mark.parametrize(
    ("text", "heard", "close"),
    [
        ("A contributor to C Python.", "a contributor to cpython", True),
        ("Minus linked P R means no pull request.", "minus linked pr means no pull request", True),
        ("Within a minute or two.", "within a minute or two", True),
        ("Never opened a pull request?", "never opened a poll request", True),
        ("Fix it in your fork, and commit.", "fix it in your fork", False),
        ("Give it a week.", "give it a wink", False),
        ("It updates automatically, and the check runs again.", "it updates and the check runs again", False),
        ("Give it a week.", "the weather is nice", False),
        ("Anything at all.", "", False),
    ],
)
def test_match_ignores_spacing_and_punctuation_but_not_missing_words(text, heard, close):
    assert azure_tts.acceptable(text, heard) is close


def test_key_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("AZURE_SPEECH_KEY", " abc123 ")
    assert azure_tts.speech_key() == "abc123"


def test_no_key_stops_with_instructions(monkeypatch):
    monkeypatch.delenv("AZURE_SPEECH_KEY", raising=False)
    monkeypatch.setattr(azure_tts.sys, "platform", "linux")
    with pytest.raises(SystemExit) as stop:
        azure_tts.speech_key()
    assert "--voice Aman" in str(stop.value)


@pytest.fixture
def fake_service(monkeypatch):
    """speak() returns numbered clips; transcribe() says what the test queued."""
    calls = {"speak": 0, "heard": []}

    def speak(text, voice):
        calls["speak"] += 1
        return b"RIFF" + bytes(40) + bytes([calls["speak"]]) * 96000  # a 1-second clip

    def transcribe(wav, voice):
        return calls["heard"].pop(0)

    monkeypatch.setattr(azure_tts, "speak", speak)
    monkeypatch.setattr(azure_tts, "transcribe", transcribe)
    return calls


def test_a_matching_clip_is_kept_and_cached(fake_service, tmp_path):
    fake_service["heard"] = ["give it a week"]
    clip = azure_tts.synthesize("Give it a week.", tmp_path / "a.wav", VOICE, tmp_path / "cache")
    assert clip.match == 1.0 and clip.attempts == 1

    again = azure_tts.synthesize("Give it a week.", tmp_path / "b.wav", VOICE, tmp_path / "cache")
    assert fake_service["speak"] == 1, "the second render must come from the cache"
    assert again == clip
    assert (tmp_path / "b.wav").read_bytes() == (tmp_path / "a.wav").read_bytes()


def test_a_garbled_clip_is_made_again(fake_service, tmp_path):
    fake_service["heard"] = ["give it a wink wink", "give it a week"]
    clip = azure_tts.synthesize("Give it a week.", tmp_path / "a.wav", VOICE, tmp_path / "cache")
    assert clip.attempts == 2 and clip.match == 1.0
    assert (tmp_path / "a.wav").read_bytes()[44] == 2, "the second, matching clip is the one kept"


def test_when_no_clip_matches_the_best_one_is_kept_and_reported(fake_service, tmp_path):
    fake_service["heard"] = ["nothing like it", "give it a wink", "something else"]
    clip = azure_tts.synthesize("Give it a week.", tmp_path / "a.wav", VOICE, tmp_path / "cache")
    assert clip.attempts == azure_tts.ATTEMPTS
    assert clip.heard == "give it a wink" and clip.match < 1.0
    assert (tmp_path / "a.wav").read_bytes()[44] == 2


def test_different_text_or_voice_is_a_different_clip(fake_service, tmp_path):
    fake_service["heard"] = ["one", "two", "one"]
    azure_tts.synthesize("One.", tmp_path / "a.wav", VOICE, tmp_path / "cache")
    azure_tts.synthesize("Two.", tmp_path / "b.wav", VOICE, tmp_path / "cache")
    azure_tts.synthesize("One.", tmp_path / "c.wav", "en-IN-AaravNeural", tmp_path / "cache")
    assert fake_service["speak"] == 3


def test_busy_service_is_retried(monkeypatch):
    import io
    import urllib.error

    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")
    monkeypatch.setattr(azure_tts.time, "sleep", lambda s: None)
    replies = [urllib.error.HTTPError("u", 429, "Too Many Requests", {"Retry-After": "1"}, io.BytesIO(b"")), b"audio"]

    class Reply:
        def __init__(self, data):
            self.data = data

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return self.data

    def urlopen(request, timeout):
        assert request.get_header("Ocp-apim-subscription-key") == "k"
        reply = replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return Reply(reply)

    monkeypatch.setattr(azure_tts.urllib.request, "urlopen", urlopen)
    assert azure_tts.speak("Hello", VOICE) == b"audio"


def test_a_refused_request_fails_clearly(monkeypatch):
    import io
    import urllib.error

    monkeypatch.setenv("AZURE_SPEECH_KEY", "k")

    def urlopen(request, timeout):
        raise urllib.error.HTTPError("u", 401, "Unauthorized", {}, io.BytesIO(b"bad key"))

    monkeypatch.setattr(azure_tts.urllib.request, "urlopen", urlopen)
    with pytest.raises(RuntimeError, match="HTTP 401"):
        azure_tts.speak("Hello", VOICE)
