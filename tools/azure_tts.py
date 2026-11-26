"""Narration with Azure AI Speech voices, checked by transcribing each clip back.

``render_video.py`` uses this for voices named like Azure's
(``en-IN-Arjun:DragonHDLatestNeural``); other names go to macOS ``say``.

Every clip is transcribed with Azure speech-to-text and compared with the
text it was made from. HD voices are generative, so a clip can come out with
a slurred or invented word; a clip that doesn't match is made again. Clips
are cached by voice and text, so a re-render only makes the beats that
changed and a checked clip never changes under you.

Setup (once): create a Speech resource in the Azure portal, then store its
key where this module looks for it, either in the environment::

    export AZURE_SPEECH_KEY=...      # and AZURE_SPEECH_REGION if not eastus

or, on macOS, in the Keychain (the command asks for the key)::

    security add-generic-password -s azure-speech-key -a "$USER" -w
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.sax.saxutils import escape

VOICE_RE = re.compile(r"^[a-z]{2,3}-[A-Za-z]{2,4}-\S+$")
KEYCHAIN_SERVICE = "azure-speech-key"
DEFAULT_REGION = "eastus"
OUTPUT_FORMAT = "riff-48khz-16bit-mono-pcm"
ALLOWED_ERRORS = 0.03  # letters of a clip's transcript that may differ from its text (at least 1)
ATTEMPTS = 4  # tries to get a clip that matches
MAX_CHECK_SECONDS = 55  # the transcription endpoint takes clips up to 60 s
RETRY_STATUS = {429, 500, 502, 503, 504}


def is_azure_voice(voice: str) -> bool:
    """True for Azure voice names (``en-IN-AaravNeural``), False for ``say`` voices (``Aman``)."""
    return bool(VOICE_RE.match(voice))


def speech_key() -> str:
    key = os.environ.get("AZURE_SPEECH_KEY", "").strip()
    if not key and sys.platform == "darwin":
        found = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"], capture_output=True, text=True
        )
        key = found.stdout.strip() if found.returncode == 0 else ""
    if not key:
        sys.exit(
            "No Azure Speech key. Set AZURE_SPEECH_KEY, or on macOS run:\n"
            f'  security add-generic-password -s {KEYCHAIN_SERVICE} -a "$USER" -w\n'
            "Or render with a macOS voice: --voice Aman"
        )
    return key


def region() -> str:
    return os.environ.get("AZURE_SPEECH_REGION", DEFAULT_REGION)


def ssml(text: str, voice: str) -> str:
    locale = "-".join(voice.split("-")[:2])
    return (
        f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{locale}'>"
        f"<voice name='{voice}'>{escape(text)}</voice></speak>"
    )


def _post(url: str, data: bytes, headers: dict[str, str]) -> bytes:
    """POST with the key, waiting and retrying when the service is busy or throttling."""
    headers = {"Ocp-Apim-Subscription-Key": speech_key(), "User-Agent": "first-python-contribution", **headers}
    for attempt in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as err:
            if err.code not in RETRY_STATUS or attempt == 7:
                raise RuntimeError(f"Azure Speech said HTTP {err.code}: {err.read()[:300]!r}") from err
            wait = float(err.headers.get("Retry-After") or 0) or min(5 * (attempt + 1), 30)
        except (urllib.error.URLError, TimeoutError) as err:
            if attempt == 7:
                raise RuntimeError(f"Azure Speech is unreachable: {err}") from err
            wait = min(5 * (attempt + 1), 30)
        time.sleep(wait)
    raise AssertionError("unreachable")


def speak(text: str, voice: str) -> bytes:
    """One narration clip as 48 kHz mono WAV bytes."""
    url = f"https://{region()}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {"Content-Type": "application/ssml+xml", "X-Microsoft-OutputFormat": OUTPUT_FORMAT}
    return _post(url, ssml(text, voice).encode("utf-8"), headers)


def transcribe(wav: Path, voice: str) -> str:
    """What the clip says, in words (numbers spelled out), from Azure speech-to-text."""
    small = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", str(wav), "-ar", "16000", "-ac", "1", "-f", "wav", "-"],
        check=True,
        capture_output=True,
    ).stdout
    locale = "-".join(voice.split("-")[:2])
    url = (
        f"https://{region()}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        f"?language={locale}&format=detailed"
    )
    reply = json.loads(_post(url, small, {"Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000"}))
    best = reply.get("NBest") or [{}]
    return best[0].get("Lexical", "") if reply.get("RecognitionStatus") == "Success" else ""


def letters(text: str) -> str:
    """Lower-case letters only, so "C Python" and "CPython", or "P R" and "PR", compare equal."""
    return re.sub(r"[^a-z]", "", text.lower())


def match(text: str, heard: str) -> float:
    """How closely the transcript matches the text: 1.0 is letter for letter."""
    return difflib.SequenceMatcher(None, letters(text), letters(heard), autojunk=False).ratio()


def wrong_letters(text: str, heard: str) -> int:
    """How many letters of the longer of text and transcript have no partner in the other."""
    a, b = letters(text), letters(heard)
    same = sum(block.size for block in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks())
    return max(len(a), len(b)) - same


def words(text: str) -> list[str]:
    return [w for w in (re.sub(r"[^a-z0-9']", "", part) for part in text.lower().replace("-", " ").split()) if w]


def dropped_words(text: str, heard: str) -> list[str]:
    """Words of the text that the transcript has nothing for, or far too little.

    A transcriber swaps words that sound alike ("ruff" and "rough"), and that
    isn't the voice's mistake. A word with no counterpart at all, or a phrase
    that shrank by three letters or more ("dot p y" heard as "py"), is: the
    voice skipped or clipped it. Clipped sentence endings are the usual case.
    """
    spoken, got = words(text), words(heard)
    dropped = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, spoken, got, autojunk=False).get_opcodes():
        said, heard_as = "".join(spoken[i1:i2]), "".join(got[j1:j2])
        if op == "delete" and len(letters(said)) >= 3:
            dropped.append(" ".join(spoken[i1:i2]))
        elif op == "replace" and len(letters(said)) - len(letters(heard_as)) >= 3:
            dropped.append(" ".join(spoken[i1:i2]))
    return dropped


def acceptable(text: str, heard: str) -> bool:
    """True if the transcript is the text, give or take what a transcriber mishears.

    "poll request" for "pull request" is one letter and fine. More than a
    few wrong letters, or any dropped word, isn't.
    """
    close = wrong_letters(text, heard) <= max(1, round(ALLOWED_ERRORS * len(letters(text))))
    return close and not dropped_words(text, heard)


def wav_seconds(wav: Path) -> float:
    return max(wav.stat().st_size - 44, 0) / (48000 * 2)


@dataclass
class Clip:
    """A checked narration clip, as recorded in the cache and in narration-check.json."""

    voice: str
    text: str
    heard: str
    match: float
    attempts: int
    seconds: float


def synthesize(text: str, out: Path, voice: str, cache: Path) -> Clip:
    """Write the clip for ``text`` to ``out``, from the cache when it's there.

    A new clip is transcribed and compared with the text. If it isn't
    ``acceptable`` it's made again, up to ``ATTEMPTS`` times, and the best
    one is kept. The returned ``Clip`` has the transcript, so the caller can
    report clips that never matched.
    """
    cache.mkdir(parents=True, exist_ok=True)
    name = hashlib.sha256(f"{voice}\n{text}".encode()).hexdigest()[:32]
    wav, meta = cache / f"{name}.wav", cache / f"{name}.json"
    if wav.is_file() and meta.is_file():
        out.write_bytes(wav.read_bytes())
        return Clip(**json.loads(meta.read_text(encoding="utf-8")))

    best: Clip | None = None
    best_audio = b""
    for attempt in range(1, ATTEMPTS + 1):
        audio = speak(text, voice)
        out.write_bytes(audio)
        seconds = wav_seconds(out)
        heard = transcribe(out, voice) if seconds <= MAX_CHECK_SECONDS else ""
        score = match(text, heard) if seconds <= MAX_CHECK_SECONDS else 0.0
        if best is None or score > best.match:
            best, best_audio = Clip(voice, text, heard, round(score, 3), attempt, round(seconds, 2)), audio
        if acceptable(text, heard):
            break
    assert best is not None
    best.attempts = attempt
    out.write_bytes(best_audio)
    wav.write_bytes(best_audio)
    meta.write_text(json.dumps(asdict(best), ensure_ascii=False, indent=1), encoding="utf-8")
    return best
